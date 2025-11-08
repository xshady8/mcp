# mcp_llm_wrapper.py
import asyncio
import json
from mcp import ClientSession, types
from mcp.client.stdio import stdio_client

class MCPClientWrapper:
    def __init__(self, llm_chain, mcp_command="python", mcp_args=["server.py"]):
        self.llm_chain = llm_chain
        self.mcp_command = mcp_command
        self.mcp_args = mcp_args

    async def _setup_session(self):
        server_params = types.StdioServerParameters(
            command=self.mcp_command,
            args=self.mcp_args,
        )
        self.client = stdio_client(server_params)
        self.reader_writer = await self.client.__aenter__()
        self.session = ClientSession(*self.reader_writer)
        await self.session.__aenter__()
        await self.session.initialize()

    async def _teardown(self):
        await self.session.__aexit__(None, None, None)
        await self.client.__aexit__(None, None, None)

    async def query(self, user_query: str):
        """Send a query to the LLM and use MCP tools if required."""
        await self._setup_session()

        # Discover available capabilities
        tools = await self.session.list_tools()
        resources = await self.session.list_resources()
        prompts = await self.session.list_prompts()

        # Create reasoning context for LLM
        context = f"""
Available tools: {tools}
Available resources: {resources}
Available prompts: {prompts}

User query: "{user_query}"

Decide what to do.
Output JSON with one of:
  - {{"action": "call_tool", "name": "tool_name", "args": {{...}}}}
  - {{"action": "read_resource", "uri": "resource://..." }}
  - {{"action": "answer", "text": "..." }}
"""
        plan = self.llm_chain.run(question=context)
        print("\n🧠 LLM plan:", plan)

        # Try to parse JSON output
        try:
            plan_data = json.loads(plan)
        except json.JSONDecodeError:
            await self._teardown()
            return f"Invalid LLM output: {plan}"

        # Execute based on plan
        if plan_data["action"] == "call_tool":
            result = await self.session.call_tool(plan_data["name"], plan_data["args"])
        elif plan_data["action"] == "read_resource":
            result, _ = await self.session.read_resource(plan_data["uri"])
        elif plan_data["action"] == "answer":
            result = plan_data["text"]
        else:
            result = "Unknown action"

        # Send result back to LLM for summarization
        summary = self.llm_chain.run(
            question=f"Tool result: {result}\nSummarize in user-friendly language."
        )

        await self._teardown()
        return summary

