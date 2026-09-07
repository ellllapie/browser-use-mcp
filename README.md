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

### Option 1: Use with relay service (e.g., 灵眸)
```bash
OPENAI_API_KEY=your_relay_api_key
OPENAI_BASE_URL=https://your-relay-service.com/v1
```

### Option 2: Use official OpenAI API
```bash
OPENAI_API_KEY=your_openai_api_key
# OPENAI_BASE_URL not needed
```

### Option 3: Use Browser Use Cloud
```bash
BROWSER_USE_API_KEY=your_browser_use_api_key
```

### Option 4: Use other providers
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
# or
GOOGLE_API_KEY=your_google_api_key
```

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
