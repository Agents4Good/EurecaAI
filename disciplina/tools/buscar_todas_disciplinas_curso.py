from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
import inspect

@mcp.tool()
async def buscar_todas_disciplinas_curso(campus: Any = 1, curso: Any = 14102100) -> str | list[dict]:
    """
    Busca todas as disciplinas de um curso de um determinado campus

    Args:
        campus: código do campus. Default = 1.
        curso: código do curso. Default = 14102100.
    
    Returns:
        Resposta da tool
    """

    params = {
        "status": 'ATIVOS',
        "campus": campus, 
        "curso": curso
    }

    try:

        logging.info(f"Chamando a API com campus={campus}, curso={curso}")
        url = f"{BASE_URL}/disciplinas"
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter as disciplinas ou nenhuma disciplina foi encontrada"
        
 
        return data[0:10]
    except Exception as e:
        import traceback
        func_name = inspect.currentframe().f_code.co_name
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        

