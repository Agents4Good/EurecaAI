from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todos_calendarios(periodo_de:Any, periodo_ate: Any, campus:Any = 1):
    """
    Retorna todos os calendários acadêmicos da UFCG dentro de um intervalo de períodos.

    Args:
        periodo_de (Any): Período inicial no formato "AAAA.X" (ex.: "2020.1").
        periodo_ate (Any): Período final no formato "AAAA.X".
        campus (Any, opcional): Código do campus. Padrão é 1.

    Returns:
        list[dict]: Lista de calendários no formato:
            {
                "id": int,                           # Identificador do período
                "periodo": str,                       # Ex.: "2020.1"
                "campus": int,                        # Código do campus
                "inicio_das_matriculas": str,         # Data início das matrículas
                "inicio_das_aulas": str,              # Data início das aulas
                "um_terco_do_periodo": str,           # Data que marca 1/3 do período
                "ultimo_dia_para_registro_de_notas": str,  # Data limite registro de notas
                "um_quarto_do_periodo": str,          # Data que marca 1/4 do período
                "numero_de_semanas": int              # Quantidade de semanas do período
            }
    """

    params = {
        "periodo_de": periodo_ate,
        "periodo_ate": periodo_ate,
        "campus": campus
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/calendarios"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter informações sobre os calendários da UFCG."
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise




