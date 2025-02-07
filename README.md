# Code Analysis MCP Server

A Model Context Protocol (MCP) server that enables AI models to understand and analyze codebases through natural language conversations.

## ✨ Highlights

- **Natural Code Exploration**: Ask high-level questions about your codebase
  ```
  "What are all the different payment providers integrated in the system?"
  ```

- **Deep Code Understanding**: Extract insights about data models and system architecture
  ```
  "How does the user authentication flow work from frontend to database?"
  ```

- **Dynamic Analysis**: Trace data flows and understand system relationships
  ```
  "Show me all the places where we calculate transaction fees"
  ```

## Limitations

This tool is a simpler alternative to more sophisticated code analysis tools / copilot like [Aider](https://aider.chat/). While it lacks the advanced code analysis capabilities and robustness of tools like Aider, it offers a lightweight solution for codebase exploration if you already have a Claude Pro subscription. The main advantages are:

- **Cost-Effective**: Using your existing Claude Pro subscription means no additional API costs, unlike tools that can get expensive when analyzing large codebases
- **Simple Setup**: Quick to get started with minimal configuration
- **Basic Analysis**: Good for high-level code understanding and exploration

Note that due to its simpler approach to code analysis, it may make more errors or provide less detailed insights compared to more specialized tools.

## 🚀 Quick Start

1. Install the server:
```bash
git clone https://github.com/saiprashanths/code-analysis-mcp.git
cd code-analysis-mcp
```

2. Install [Claude Desktop App](https://claude.ai/download). For more instructions on setting up an MCP Server with Claude Desktop app, [see docs](https://modelcontextprotocol.io/quickstart/user)

3. Configure the server in Claude Desktop's configuration file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "code-analysis": {
      "command": "uv",
      "args": [
        "--directory",
        "/PATH/TO/YOUR/REPO",
        "run",
        "code_analysis.py"
      ]
    }
  }
}
```

4. Restart Claude Desktop and start analyzing your code!

5. Ensure the tool is correctly setup
- Clicking the tools icon should display the `code-analysis` tools
![tools icon](./docs/images/tools.png | width=100)
![Available MCP Tools](./docs/images/mcptools.png | width=100)

- Clicking the integrations button should display the `analyze_code_repository` prompt
![Integrations icon](./docs/images/integrations.png | width=100)
![Analyze code repo prompt](./docs/images/prompt.png | width=100)
## 💡 Example Usage

Here's how you might use the tool to understand a complex codebase:

Start by clicking on the `analyze_code_repository` prompt shown below. That will guide you through the process 
to initialize the repo and get started.

![Analyze code repo prompt](./docs/images/prompt.png | width=100)

```text
You: How does the transaction processing work in this system?

Claude: Let me analyze the data flow for transactions. 
Looking at the codebase, I can see that transaction processing happens through several key components:

1. Raw transaction data is captured in the `TransactionEvent` model with fields for:
   - Payment status
   - Amount
   - Fee calculations
   - Processing timestamps

2. This data is then processed through the PaymentSummary model, which:
   - Validates payment provider responses
   - Calculates processing fees
   - Records transaction status

Would you like me to explain any part of this in more detail?

You: What are the key database tables involved?

Claude: The main tables in the transaction processing pipeline are:

1. transaction_events: Stores raw payment events
2. payment_summary: Processed transaction records
3. payment_providers: Provider configuration
4. merchant_accounts: Account-specific settings

Let me know if you'd like to see the schema for any of these tables!
```

## 🔧 Available Tools

### initialize_repository
Initialize a code repository for analysis:
```python
initialize_repository("/path/to/repo")
# Output: Successfully initialized code repository at: /path/to/repo
```

### get_repo_info
Retrieve information about the initialized repository:
```python
get_repo_info()
# Output:
# Code Repository Information:
# Path: /path/to/repo
# Exists: True
# Is Directory: True
# Found .gitignore file
```

### get_repo_structure
Examine repository file structure:
```python
get_repo_structure(depth=2)
# Output:
# 📁 src/
#   📁 api/
#     📄 routes.py
#     📄 models.py
#   📁 utils/
#     📄 helpers.py
#   📄 main.py
```

### read_file
Read and analyze specific files:
```python
read_file("src/api/models.py")
# Output:
# File: src/api/models.py
# Language: python
# Size: 2.3 KB
# 
# [File contents...]
```

## ⚙️ Technical Details

- Default scanning depth: 3 levels
- Maximum file size: 1MB
- Maximum lines per file: 1000
- Ignores paths listed in .gitignore
- Local file system access only
- Validates file paths to prevent directory traversal

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
