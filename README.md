# Code Analysis Tools

A Python-based toolkit for analyzing code repositories and providing structural insights.

## Features

- **Repository Structure Analysis**: Analyzes and visualizes the structure of code repositories
- **Smart File Reading**: Reads and processes code files with size limits and language detection
- **GitIgnore Integration**: Respects .gitignore patterns when analyzing repositories
- **FastMCP Integration**: Provides a server interface for code analysis operations

## Components

### RepoStructureAnalyzer

Analyzes repository structure with features like:
- Configurable depth and children limits
- Built-in ignore patterns
- GitIgnore support
- Hierarchical structure visualization

### FileReader

Handles file operations with:
- Size limit protection (1MB default)
- Language detection
- Safe file reading

### CodeAnalysisServer

FastMCP-based server providing:
- Repository initialization
- File reading capabilities
- Structure analysis endpoints

## Installation

```bash
# Install dependencies using your preferred package manager
pip install -r requirements.txt
```

## Usage

```python
# Initialize the analyzer
analyzer = RepoStructureAnalyzer(repo_path=Path("./your-repo"))

# Get repository structure
structure = analyzer.get_structure(analyzer.repo_path)

# Read file contents
reader = FileReader(repo_path=Path("./your-repo"))
file_content = reader.read_file("path/to/file.py")
```

## Configuration

- `MAX_DEPTH`: Configure maximum depth for repository scanning (default: 3)
- `MAX_CHILDREN`: Limit number of children per directory (default: 100)
- `MAX_SIZE`: File size limit for reading (default: 1MB)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
