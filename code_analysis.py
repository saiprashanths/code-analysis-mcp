from pathlib import Path
from typing import Optional, List, Dict, Union, Set
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

@dataclass
class Summary:
    file_count: int = 0
    dir_count: int = 0
    total_size: int = 0

@dataclass
class FileStructure:
    path: str
    type: str
    size: Optional[int] = None
    children: Optional[List['FileStructure']] = None
    summary: Optional[Summary] = None

class RepoStructureAnalyzer:
    def __init__(self, repo_path: Path, max_depth: int = 3, max_children: int = 100):
        self.repo_path = repo_path
        self.MAX_DEPTH = max_depth
        self.MAX_CHILDREN = max_children
        
        # Default patterns to always ignore
        self.default_ignore_patterns = ['.git', '__pycache__', 'node_modules']
        
        # Load .gitignore if it exists
        self.gitignore_spec = self._load_gitignore()

    def _load_gitignore(self) -> Optional[PathSpec]:
        """Load .gitignore patterns if the file exists."""
        gitignore_path = self.repo_path / '.gitignore'
        patterns = []
        
        # Add default patterns
        for pattern in self.default_ignore_patterns:
            patterns.append(GitWildMatchPattern(pattern))

        # Add patterns from .gitignore if it exists
        if gitignore_path.exists() and gitignore_path.is_file():
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            patterns.append(GitWildMatchPattern(line))
            except Exception as e:
                print(f"Error reading .gitignore: {e}")
        
        return PathSpec(patterns)

    def _is_safe_path(self, path: Path) -> bool:
        """Check if the given path is safe (no directory traversal)."""
        try:
            return path.resolve().is_relative_to(self.repo_path.resolve())
        except ValueError:
            return False

    def format_structure(self, structure: FileStructure) -> str:
        """Format the file structure into a readable string."""
        output = []

        def format_size(size: int) -> str:
            units = ['B', 'KB', 'MB', 'GB']
            value = float(size)
            index = 0
            while value >= 1024 and index < len(units) - 1:
                value /= 1024
                index += 1
            return f"{value:.1f} {units[index]}"

        def format_item(item: FileStructure, level: int = 0) -> None:
            indent = '  ' * level
            
            if item.type == 'directory':
                output.append(f"{indent}📁 {item.path}/")
                
                if item.summary:
                    summary = item.summary
                    output.append(
                        f"{indent}   Contains: {summary.file_count} files, "
                        f"{summary.dir_count} directories, "
                        f"{format_size(summary.total_size)}"
                    )
                elif item.children:
                    for child in item.children:
                        format_item(child, level + 1)
            else:
                output.append(f"{indent}📄 {item.path} ({format_size(item.size or 0)})")

        format_item(structure)
        return '\n'.join(output)

    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored based on gitignore patterns."""
        return self.gitignore_spec.match_file(path)

    def get_structure(
        self,
        current_path: Path,
        relative_path: str = '',
        current_depth: int = 0,
        max_depth: Optional[int] = None
    ) -> FileStructure:
        """Recursively get the structure of files and directories."""
        if max_depth is None:
            max_depth = self.MAX_DEPTH

        # Verify path safety
        if not self._is_safe_path(current_path):
            raise ValueError(f"Invalid path: {current_path}")

        # Skip symbolic links
        if current_path.is_symlink():
            raise ValueError(f"Symbolic links are not supported: {current_path}")

        stats = current_path.stat()
        rel_path = relative_path or current_path.name

        if relative_path and self.should_ignore(relative_path):
            raise ValueError(f"Path {relative_path} is ignored")

        if current_path.is_file():
            return FileStructure(
                path=rel_path,
                type="file",
                size=stats.st_size
            )

        if current_path.is_dir():
            children = []
            summary = Summary()

            if current_depth < max_depth:
                try:
                    entries = list(current_path.iterdir())
                    
                    for entry in entries:
                        if len(children) >= self.MAX_CHILDREN:
                            if entry.is_file() and not entry.is_symlink():
                                summary.file_count += 1
                                summary.total_size += entry.stat().st_size
                            elif entry.is_dir() and not entry.is_symlink():
                                summary.dir_count += 1
                            continue

                        entry_relative_path = str(entry.relative_to(self.repo_path))

                        try:
                            if self.should_ignore(entry_relative_path):
                                continue

                            if entry.is_symlink():
                                continue

                            entry_stats = entry.stat()
                            
                            if entry.is_file():
                                summary.file_count += 1
                                summary.total_size += entry_stats.st_size
                            elif entry.is_dir():
                                summary.dir_count += 1

                            child = self.get_structure(
                                entry,
                                entry_relative_path,
                                current_depth + 1,
                                max_depth
                            )
                            children.append(child)

                        except Exception as error:
                            print(f"Error processing {entry}: {error}")
                            continue

                except Exception as error:
                    print(f"Error reading directory {current_path}: {error}")

            return FileStructure(
                path=rel_path,
                type="directory",
                children=children if children else None,
                summary=summary if current_depth >= max_depth or len(children) >= self.MAX_CHILDREN else None
            )

        raise ValueError(f"Unsupported file type at {current_path}")

class CodeAnalysisServer(FastMCP):
    def __init__(self, name: str):
        super().__init__(name)
        self.repo_path: Optional[Path] = None
        self.analyzer: Optional[RepoStructureAnalyzer] = None

    def initialize_repo(self, path: str) -> None:
        """Initialize the repository path and structure analyzer."""
        repo_path = Path(path).resolve()
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        if not repo_path.is_dir():
            raise ValueError(f"Repository path is not a directory: {repo_path}")
        
        self.repo_path = repo_path
        self.analyzer = RepoStructureAnalyzer(self.repo_path)

# Initialize server
mcp = CodeAnalysisServer("code-analysis")

@mcp.tool()
async def initialize_repository(path: str) -> str:
    """Initialize the repository path for future code analysis operations.
    
    Args:
        path: Path to the repository root directory that contains the code to analyze
    """
    try:
        mcp.initialize_repo(path)
        gitignore_path = Path(path) / '.gitignore'
        gitignore_status = "Found .gitignore file" if gitignore_path.exists() else "No .gitignore file present"
        return f"Successfully initialized code repository at: {mcp.repo_path}\n{gitignore_status}"
    except ValueError as e:
        return f"Error initializing code repository: {str(e)}"

@mcp.tool()
async def get_repo_info() -> str:
    """Get information about the currently initialized code repository."""
    if not mcp.repo_path:
        return "No code repository has been initialized yet. Please use initialize_repository first."
    
    gitignore_path = mcp.repo_path / '.gitignore'
    gitignore_status = "Found .gitignore file" if gitignore_path.exists() else "No .gitignore file present"
    
    return f"""Code Repository Information:
Path: {mcp.repo_path}
Exists: {mcp.repo_path.exists()}
Is Directory: {mcp.repo_path.is_dir()}
{gitignore_status}"""

@mcp.tool()
async def get_repo_structure(sub_path: Optional[str] = None, depth: Optional[int] = None) -> str:
    """Get the structure of files and directories in the repository.
    
    Args:
        sub_path: Optional subdirectory path relative to repository root
        depth: Optional maximum depth to traverse (default is 3)
    """
    if not mcp.repo_path or not mcp.analyzer:
        return "No code repository has been initialized yet. Please use initialize_repository first."

    try:
        target_path = mcp.repo_path
        if sub_path:
            target_path = mcp.repo_path / sub_path
            if not mcp.analyzer._is_safe_path(target_path):
                return "Error: Invalid path - directory traversal not allowed"

        structure = mcp.analyzer.get_structure(
            target_path,
            sub_path or '',
            max_depth=depth
        )
        return mcp.analyzer.format_structure(structure)
    except Exception as e:
        return f"Error analyzing repository structure: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')