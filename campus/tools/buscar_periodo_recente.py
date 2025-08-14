from typing import Any
from helpers.make_request import make_request
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_periodo_recente(campus: Any) -> list[dict]:
    """
    Retorna o calendário acadêmico mais recente (período atual) da UFCG,
    considerando o campus informado.

    Args:
        campus (Any): Código do campus.

    Returns:
        list[dict]: Lista contendo um ou mais calendários no formato:
            {
                "id": int,                           # Identificador do período
                "periodo": str,                       # Ex.: "2024.1"
                "campus": int,                        # Código do campus
                "inicio_das_matriculas": str,         # Data/hora início das matrículas
                "inicio_das_aulas": str,              # Data/hora início das aulas
                "um_terco_do_periodo": str,           # Data/hora que marca 1/3 do período
                "ultimo_dia_para_registro_de_notas": str,  # Data limite para registro de notas
                "um_quarto_do_periodo": str | null,   # Data/hora que marca 1/4 do período
                "numero_de_semanas": int | null       # Quantidade de semanas do período
            }
    """

    params = {
        "campus": campus
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/calendarios/periodo-corrente"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return f"Não foi possível obter informações sobre o período mais recente do campus {campus} da UFCG."
        return data

    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise