# Code Analysis MCP Server

A Python-based Model Context Protocol (MCP) server that helps AI models understand and analyze codebases. This server provides a standardized interface for code repository analysis through FastMCP.

## Features

- **Comprehensive Language Support**: Detects and handles 40+ programming languages and file types
- **Smart File Reading**: Size limits and encoding detection for safe file operations
- **GitIgnore Integration**: Respects .gitignore patterns and default ignore rules
- **Hierarchical Structure Analysis**: Visualizes repository structure with summaries
- **Safe Operations**: Path validation and symbolic link protection

## Available MCP Tools

1. `initialize_repository(path: str)`
   - Initializes the repository for analysis
   - Validates repository path and structure
   - Sets up GitIgnore patterns

2. `get_repo_info()`
   - Provides repository status and configuration
   - Shows path and GitIgnore information
   - Validates repository state

3. `get_repo_structure(sub_path: Optional[str], depth: Optional[int])`
   - Maps repository structure with customizable depth
   - Shows file sizes and directory summaries
   - Supports subfolder analysis
   - Respects GitIgnore patterns

4. `read_file(file_path: str)`
   - Retrieves and formats file contents
   - Includes language detection
   - Provides file metadata
   - Implements size limits (1MB default)
   - Handles binary file detection

## Components

### RepoStructureAnalyzer
- Configurable depth (default: 3) and children limits (default: 100)
- Built-in ignore patterns (.git, __pycache__, node_modules)
- GitIgnore integration
- Directory summaries for large folders

### FileReader
- 1MB size limit protection
- Extensive language detection (40+ types)
- Safe path validation
- Line limit controls (1000 lines default)

### CodeAnalysisServer
- FastMCP-based interface
- Stateful repository management
- Safe file operations
- Structured response formatting

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage with AI Models

Configure the MCP server in your AI model's settings:

```json
{
    "mcpServers": {
        "code-analysis": {
            "command": "python",
            "args": ["code_analysis.py"]
        }
    }
}
```

Example tool usage:
```python
# Initialize repository
await initialize_repository("/path/to/repo")

# Get repository structure
structure = await get_repo_structure(depth=3)

# Read specific file
content = await read_file("path/to/file.py")
```

## Configuration

Default limits that can be modified in the code:
- `MAX_DEPTH`: Repository scanning depth (default: 3)
- `MAX_CHILDREN`: Children per directory (default: 100)
- `MAX_SIZE`: File size limit (default: 1MB)
- `MAX_LINES`: Maximum lines to read (default: 1000)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
