# main.py
import asyncio
from my_llm import chain
from mcp_llm_wrapper import MCPClientWrapper

async def main():
    wrapper = MCPClientWrapper(chain)
    answer = await wrapper.query("Add 5 and 7 using available tools")
    print("\n✅ Final answer:", answer)

if __name__ == "__main__":
    asyncio.run(main())

