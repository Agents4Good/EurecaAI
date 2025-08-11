from mcp.server.fastmcp import FastMCP
from .get_estagios import get_estagios
from .get_professores_setor import get_professores_setor
from get_todos_setores import get_todos_setores
from ..utils.mcp_scraping import get_tools_formatted

mcp_campus = FastMCP("disciplina")

tools = [
    get_estagios,
    get_professores_setor,
    get_todos_setores
]

for func in tools:
    decorated = mcp_campus.tool()(func)
    mcp_campus.add_tool(decorated)

formatted_tools = get_tools_formatted(tools)

if __name__ == "__main__":
    mcp_campus.run(transport="stdio")