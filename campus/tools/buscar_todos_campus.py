from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todos_campus() -> list[dict]:
    """
    Retorna todos os campi/polos da UFCG.

    Returns:
        list[dict]: Lista de campi no formato:
            {
                "campus": int,           # Código do campus
                "descricao": str,        # Nome do campus
                "representacao": str     # Número do campus em algarismo romano
            }
    """

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/campi"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url)

        if not data:
            return "Não foi possível obter informações sobre os campus da UFCG."
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise

