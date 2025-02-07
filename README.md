# Code Analysis MCP Server

A Python-based Model Context Protocol (MCP) server that helps AI models understand and analyze codebases. This server provides a standardized interface for code repository analysis through FastMCP.

## Features

This MCP allows you to ask questions against a codebase (repo). You can invoke this MCP server from your client (e.g. Claude Desktop app). 

Example tool usage using Claude:
```
I want to analyze the repo is at /ABSOLUTE/PATH/TO/REPO using code-analysis mcp
```
Claude then initializes this tool and gets some basic information about to repo to understand the general properties of the codebase.

Now you can ask questions against this repo. Provide as much or as little context as you want to the LLM
```
I am seeing this URL in the browser <INSERT_URL>

In this view, I see a table named "Daily Revenue Summary". Please analyze the code and help me figure out where the data for this is coming from the backend.
```

```
In this URL, I see a table named "Publisher Report"  <ANOTHER_URL>

I want to figure out where this data is coming from the backend. In particular, I need the data model and what database table it is being fetched from.
```

You can ask it to retrieve relevant code snippets.
```
Yes, please show me the SQL query and any specific calculations being performed. I want to see all the code related to this table, from fetching data from the backend, all the way to what is displayed in the table in the browser. Please show the relevant file names and code snippets to get a full understanding of what is happening.
```
## Installation

1. Clone this Github repo locally

2. Configure MCP Client app (e.g. Claude Desktop) to use this MCP Server

For using with Claude Desktop app, add this to `~/Library/Application Support/Claude/claude_desktop_config.json`
```json
{
  "mcpServers": {
    "code-analysis": {
        "command": "uv",
        "args": [
            "--directory",
            "/ABSOLUTE/PATH/TO/REPO",
            "run",
            "code_analysis.py"
        ]
    }
  }
}
```

3. Restart MCP Client
4. Start using it with any codebase you want (see example usage above) 

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
  
## Technical Details

- **Hierarchical Structure Analysis**: Visualizes repository structure with summaries
- **Smart File Reading**: Size limits and encoding detection for safe file operations
- **Comprehensive Language Support**: Detects and handles 40+ programming languages and file types
- **GitIgnore Integration**: Respects .gitignore patterns and default ignore rules
- **Safe Operations**: Path validation and symbolic link protection

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

## Configuration

Default limits that can be modified in the code:
- `MAX_DEPTH`: Repository scanning depth (default: 3)
- `MAX_CHILDREN`: Children per directory (default: 100)
- `MAX_SIZE`: File size limit (default: 1MB)
- `MAX_LINES`: Maximum lines to read (default: 1000)
