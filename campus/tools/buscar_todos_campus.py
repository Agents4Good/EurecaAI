from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todos_campus() -> list[dict]:
    """
    Busca todos os campi/campus/polos da UFCG.

    Returns:
        list[dict]: Lista  de dicionários com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """

    func_name, parametros_str = get_func_info()

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        url = f"{BASE_URL}/campi"
        data = await make_request(url)

        if not data:
            return "Não foi possível obter informações sobre os campus da UFCG."
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise

