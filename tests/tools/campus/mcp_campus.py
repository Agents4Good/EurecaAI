from mcp.server.fastmcp import FastMCP
from .get_campi import get_campi
from ..utils.mcp_scraping import get_tools_formatted

mcp_campus = FastMCP("campus")

tools = [
    get_campi
]

for func in tools:
    decorated = mcp_campus.tool()(func)
    mcp_campus.add_tool(decorated)

formatted_tools = get_tools_formatted(tools)

if __name__ == "__main__":
    mcp_campus.run(transport="stdio")