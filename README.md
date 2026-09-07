# browser-use-mcp

🌐 MCP server wrapping [browser-use](https://github.com/browser-use/browser-use) — let AI browse the web autonomously.

## What it does

Exposes browser-use's AI web agent as MCP tools, allowing AI assistants to:
- Browse websites and extract information
- Fill forms and interact with pages
- Navigate complex web workflows
- Execute multi-step web tasks

## Installation

```bash
# Clone the repo
git clone https://github.com/ellllapie/browser-use-mcp.git
cd browser-use-mcp

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env and add your API key
```

## Environment Variables

- `BROWSER_USE_API_KEY`: Your Browser Use API key (get from [Browser Use Cloud](https://cloud.browser-use.com))
- Or use provider keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`

## Usage

### As MCP Server (for Kelivo, Claude Desktop, etc.)

Add to your MCP client config:

```json
{
  "mcpServers": {
    "browser-use": {
      "command": "python",
      "args": ["/path/to/browser-use-mcp/server.py"]
    }
  }
}
```

### Available Tools

- `browse_web`: Execute a web browsing task and return results

## Deployment

Deploy to Railway, Render, or any Python hosting platform. Set environment variables in your hosting dashboard.

## License

MIT
