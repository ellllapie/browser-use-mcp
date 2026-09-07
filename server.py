"""
MCP Server for browser-use

Wraps browser-use AI web agent as MCP tools.
Uses OpenAI-compatible relay (灵眸) to call Claude models.
Uses Streamable HTTP transport for remote deployment.
"""
import asyncio
import os
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from browser_use import Agent, ChatOpenAI

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
        # Get API config from environment (OpenAI-compatible relay like 灵眸)
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            return "Error: OPENAI_API_KEY environment variable is not set"

        # Use ChatOpenAI with OpenAI-compatible relay endpoint
        # Even for Claude models, relay services use /v1/chat/completions format
        llm_kwargs = {
            "model": model,
            "api_key": api_key,
        }
        if base_url:
            llm_kwargs["base_url"] = base_url

        llm = ChatOpenAI(**llm_kwargs)

        # Create and run the browser agent
        agent = Agent(
            task=task,
            llm=llm,
        )

        history = await agent.run(max_steps=max_steps)

        # Try multiple ways to extract results
        results = []

        # Method 1: final_result()
        final_result = history.final_result()
        if final_result:
            results.append(f"Final Result:\n{final_result}")

        # Method 2: Scan all history items for extracted content
        for i, item in enumerate(history.history):
            if item.result:
                for r in item.result:
                    if r.extracted_content and "Navigated to" not in r.extracted_content:
                        results.append(f"Step {i} extracted:\n{r.extracted_content}")

        # Method 3: Collect model output memories
        memories = []
        for item in history.history:
            if item.model_output:
                state = item.model_output.current_state
                if hasattr(state, 'memory') and state.memory:
                    memories.append(state.memory)

        if results:
            result_text = "\n\n".join(results)
        elif memories:
            result_text = "No explicit result extracted, but the agent recorded:\n" + "\n".join(memories)
        else:
            actions_summary = []
            for i, item in enumerate(history.history):
                if item.model_output and item.model_output.action:
                    for action in item.model_output.action:
                        action_data = action.model_dump(exclude_unset=True)
                        action_name = next(iter(action_data.keys()), "unknown")
                        actions_summary.append(f"Step {i}: {action_name}")
            if actions_summary:
                result_text = "Task ran but no result was captured. Actions taken:\n" + "\n".join(actions_summary)
            else:
                result_text = "Task completed but no result was extracted."

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
