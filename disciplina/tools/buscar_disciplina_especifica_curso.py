from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
import inspect

@mcp.tool()
async def buscar_disciplina_especifica_curso(disciplina: Any, curso: Any, campus:Any) -> dict:
    """
    Busca informações sobre uma determinada disciplina de um curso específico

    Args:
        disciplina: código da disciplina.
        curso: código do curso.
        campus: código do campus.
    
    Returns:
        Dict 
    """

    params = {
        "status": "ATIVOS",
        "campus": campus,
        "curso": curso, 
        "disciplina": disciplina
    }

    try:
        logging.info(f"Chamando a API com campus={campus}, curso={curso}, disciplina={disciplina}")
        url = f"{BASE_URL}/disciplinas"
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter a disciplina"
        
        return data
        
    except Exception as e:
        import traceback
        func_name = inspect.currentframe().f_code.co_name
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise