# server.py
import asyncio
from mcp.server import Server
from mcp import types

server = Server("demo-server")

# --- Define Tools -----------------------------------------------------------

@server.tool()
async def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@server.tool()
async def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

# --- Define Resources -------------------------------------------------------

@server.resource("resource://greeting")
async def greeting_resource() -> str:
    """A simple static resource."""
    return "Hello from MCP server!"

# --- Optional Prompt Templates ---------------------------------------------

@server.prompt("summarize")
async def summarize_prompt(context: str) -> str:
    """Prompt template that summarizes text."""
    return f"Summary of: {context}"

# --- Run the server over stdio ---------------------------------------------

if __name__ == "__main__":
    asyncio.run(server.run_stdio())
