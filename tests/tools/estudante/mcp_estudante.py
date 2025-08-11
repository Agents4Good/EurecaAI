from mcp.server.fastmcp import FastMCP
from .obter_dados_gerais_de_todos_estudantes import obter_dados_gerais_de_todos_estudantes
from .obter_ingressantes_sisu import obter_ingressantes_sisu
from .get_estudante import estudante_info
from ..utils.mcp_scraping import get_tools_formatted

mcp_campus = FastMCP("estudante")

tools = [
    obter_dados_gerais_de_todos_estudantes,
    obter_ingressantes_sisu,
    estudante_info
]

for func in tools:
    decorated = mcp_campus.tool()(func)
    mcp_campus.add_tool(decorated)

formatted_tools = get_tools_formatted(tools)

if __name__ == "__main__":
    mcp_campus.run(transport="stdio")