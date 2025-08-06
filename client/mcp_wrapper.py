from langchain_core.tools import BaseTool
from typing import Any, Optional

class MCPToolWrapper(BaseTool):
    def __init__(self, tool_name: str, session):
        super().__init__(name=tool_name, description=f"Tool {tool_name} via MCP")
        self.tool_name = tool_name
        self.session = session

    async def _arun(self, **kwargs: Any) -> str:
        print(f"[MCPToolWrapper] Chamando tool '{self.tool_name}' com args: {kwargs}")
        result = await self.session.call_tool(self.tool_name, arguments=kwargs)
        return result.content[0].text
