"""
MCP Server for browser-use

Wraps browser-use AI web agent as MCP tools.
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from browser_use import Agent, ChatBrowserUse

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
                        "description": "LLM model to use (default: 'openai/gpt-5.5'). Examples: 'anthropic/claude-opus-4-8', 'bu-2-0-mini-preview'",
                        "default": "openai/gpt-5.5"
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
        model = arguments.get("model", "openai/gpt-5.5")
        max_steps = arguments.get("max_steps", 100)
        
        if not task:
            return [TextContent(type="text", text="Error: task parameter is required")]
        
        try:
            # Create agent
            agent = Agent(
                task=task,
                llm=ChatBrowserUse(model=model),
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
