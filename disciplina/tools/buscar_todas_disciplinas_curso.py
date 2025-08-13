from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todas_disciplinas_curso(campus: Any = 1, curso: Any = 14102100) -> list[dict]:
    """
    Busca todas as disciplinas de um curso de um determinado campus

    Args:
        campus: código do campus. Default = 1.
        curso: código do curso. Default = 14102100.
    
    Returns:
        Lista com as informações de todas as disciplinas do curso.
    """

    params = {
        "status": 'ATIVOS',
        "campus": campus, 
        "curso": curso
    }

    func_name, parametros_str = get_func_info()

    try:

        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        url = f"{BASE_URL}/disciplinas"
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter as disciplinas ou nenhuma disciplina foi encontrada"
 
        return data[0:10]
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        

