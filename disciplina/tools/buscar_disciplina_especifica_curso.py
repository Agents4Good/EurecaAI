from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info
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
        Dicionário com as informações da disciplina.
    """

    params = {
        "status": "ATIVOS",
        "campus": campus,
        "curso": curso, 
        "disciplina": disciplina
    }

    
    func_name, parametros_str = get_func_info()

    try:

        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        url = f"{BASE_URL}/disciplinas"
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter a disciplina"
        
        return data
        
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise