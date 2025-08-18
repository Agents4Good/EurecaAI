from mcp.server.fastmcp import FastMCP
from .get_disciplinas import get_disciplinas
from .get_disciplina_ofertadas_periodo import get_disciplina_ofertadas_periodo
from .get_horarios_turmas_vagas_disciplina import get_horarios_turmas_vagas_disciplina
from .get_matriculas_disciplina import get_matriculas_disciplina
from .get_plano_de_aulas import get_plano_de_aulas
from .get_pre_requisitos_disciplina import get_pre_requisitos_disciplina
from .get_turmas_disciplina import get_turmas_disciplina
from .get_turmas_por_cursos import get_turmas_por_cursos
from ..utils.mcp_scraping import get_tools_formatted

mcp_campus = FastMCP("disciplina")

tools = [
    get_disciplinas, 
    get_disciplina_ofertadas_periodo,

]

for func in tools:
    decorated = mcp_campus.tool()(func)
    mcp_campus.add_tool(decorated)

formatted_tools = get_tools_formatted(tools)

print("Tools registradas:")
for tool_name, tool_obj in mcp_campus._tool_manager._tools.items():
    print(f"- {tool_name}")
    print(f"  doc: {tool_obj.description}")

    params = getattr(tool_obj, "parameters", None)
    if params:
        props = params.get("properties", {})
        if props:
            print("  parâmetros:")
            for param_name, param_info in props.items():
                tipo = param_info.get("type", "desconhecido")
                print(f"    • {param_name}: {tipo}")
        else:
            print("  parâmetros: Nenhum definido")
    else:
        print("  parâmetros: Não disponíveis")

    print()

if __name__ == "__main__":
    mcp_campus.run(transport="stdio")