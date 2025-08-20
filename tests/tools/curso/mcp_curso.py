from mcp.server.fastmcp import FastMCP
from .obter_dados_de_curso_especifico import obter_dados_de_curso_especifico
from .obter_dados_de_todos_os_cursos import obter_dados_de_todos_os_cursos
from ..utils.mcp_scraping import get_tools_formatted

mcp_campus = FastMCP("curso")

tools = [
    obter_dados_de_curso_especifico,
    obter_dados_de_todos_os_cursos
]

for func in tools:
    decorated = mcp_campus.toool()(func)
    mcp_campus.add_tool(decorated)

formatted_tools = get_tools_formatted(tools)

if __name__ == "__main__":
    mcp_campus.run(transport="streamable-http")