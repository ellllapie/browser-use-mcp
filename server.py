"""
MCP Server for browser-use

Wraps browser-use AI web agent as MCP tools.
Supports custom OpenAI base_url for relay services like 灵眸.
"""
import asyncio
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from browser_use import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

app = Server("browser-use-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="browse_web",
            description="Browse the web autonomously to complete a task. The AI agent will navigate pages, click elements, fill forms, and extract information as needed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to complete (e.g., 'Find the latest news about AI', 'Extract pricing from example.com', 'Fill this form with my info')"
                    },
                    "model": {
                        "type": "string",
                        "description": "LLM model to use (default: 'gpt-4o'). Examples: 'gpt-4o', 'gpt-4o-mini', 'claude-opus-4-8'",
                        "default": "gpt-4o"
                    },
                    "max_steps": {
                        "type": "integer",
                        "description": "Maximum number of steps to execute (default: 100)",
                        "default": 100
                    }
                },
                "required": ["task"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "browse_web":
        task = arguments.get("task")
        model = arguments.get("model", "gpt-4o")
        max_steps = arguments.get("max_steps", 100)
        
        if not task:
            return [TextContent(type="text", text="Error: task parameter is required")]
        
        try:
            # Get OpenAI config from environment
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            
            if not api_key:
                return [TextContent(
                    type="text",
                    text="Error: OPENAI_API_KEY environment variable is not set"
                )]
            
            # Create LLM with custom base_url if provided
            llm_kwargs = {
                "model": model,
                "api_key": api_key,
            }
            if base_url:
                llm_kwargs["base_url"] = base_url
            
            llm = ChatOpenAI(**llm_kwargs)
            
            # Create agent
            agent = Agent(
                task=task,
                llm=llm,
            )
            
            # Run the agent and get history
            history = await agent.run(max_steps=max_steps)
            
            # Extract final result from history
            final_result = history.final_result()
            
            if final_result:
                result_text = f"Task completed.\n\nResult:\n{final_result}"
            else:
                result_text = "Task completed but no final result was extracted."
            
            # Add step count info
            result_text += f"\n\nCompleted in {len(history.history)} steps."
            
            return [TextContent(
                type="text",
                text=result_text
            )]
            
        except Exception as e:
            error_msg = f"Error executing browser task: {type(e).__name__}: {str(e)}"
            return [TextContent(
                type="text",
                text=error_msg
            )]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
