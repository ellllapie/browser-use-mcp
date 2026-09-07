"""
MCP Server for browser-use

Wraps browser-use AI web agent as MCP tools.
Supports custom OpenAI base_url for relay services like 灵眸.
Uses Streamable HTTP transport for remote deployment.
"""
import asyncio
import os
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

load_dotenv()

mcp = MCPServer("browser-use-mcp")

@mcp.tool()
async def browse_web(task: str, model: str = "claude-haiku-4-5-20251001", max_steps: int = 100) -> str:
    """Browse the web autonomously to complete a task. The AI agent will navigate pages, click elements, fill forms, and extract information as needed.

    Args:
        task: The task to complete (e.g., 'Find the latest news about AI', 'Go to example.com and extract pricing info')
        model: LLM model to use (default: 'claude-haiku-4-5-20251001'). Examples: 'claude-haiku-4-5-20251001', 'claude-sonnet-4-6', 'claude-sonnet-4-5'
        max_steps: Maximum number of steps to execute (default: 100)
    """
    if not task:
        return "Error: task parameter is required"

    try:
        # Get Anthropic config from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        base_url = os.getenv("ANTHROPIC_BASE_URL")

        if not api_key:
            return "Error: ANTHROPIC_API_KEY environment variable is not set"

        # Create LLM with custom base_url if provided (for relay services)
        llm_kwargs = {
            "model": model,
            "api_key": api_key,
        }
        if base_url:
            llm_kwargs["base_url"] = base_url

        llm = ChatAnthropic(**llm_kwargs)

        # Create and run the browser agent
        agent = Agent(
            task=task,
            llm=llm,
        )

        history = await agent.run(max_steps=max_steps)

        # Extract final result
        final_result = history.final_result()

        if final_result:
            result_text = f"Task completed.\n\nResult:\n{final_result}"
        else:
            result_text = "Task completed but no final result was extracted."

        result_text += f"\n\nCompleted in {len(history.history)} steps."
        return result_text

    except Exception as e:
        return f"Error executing browser task: {type(e).__name__}: {str(e)}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )
