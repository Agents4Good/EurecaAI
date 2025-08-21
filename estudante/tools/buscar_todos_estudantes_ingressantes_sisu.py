from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todos_estudantes_ingressos_sisu(campus: Any, curso: Any, periodo_de: Any, periodo_ate: Any) ->  list[dict]:
    """
    Buscar informações sobre as vagas dos ingressos pelo SISU em um curso/campus da UFCG,
    considerando um intervalo de períodos.

    Args:
        campus (Any): Código do campus onde o curso está localizado.
        curso (Any): Código do curso.
        periodo_de (Any): Período inicial de ingresso (ex.: "2017.1").
        periodo_ate (Any): Período final de ingresso (ex.: "2019.2").

    Returns:
        list[dict]: Lista com os dados agregados de ingressos SISU por período no formato:
            {
                "periodo": str,              # Período de ingresso (ex.: "2017.1")
                "codigo_do_curso": int,      # Código do curso
                "a0": int,                   # Quantidade de ingressos pela modalidade A0
                "l1": int,                   # Quantidade de ingressos pela modalidade L1
                "l2": int,                   # Quantidade de ingressos pela modalidade L2
                "l5": int,                   # Quantidade de ingressos pela modalidade L5
                "l6": int,                   # Quantidade de ingressos pela modalidade L6
                "l9": int,                   # Quantidade de ingressos pela modalidade L9
                "l10": int,                  # Quantidade de ingressos pela modalidade L10
                "l13": int,                  # Quantidade de ingressos pela modalidade L13
                "l14": int,                  # Quantidade de ingressos pela modalidade L14
                "total": int                 # Total de ingressos no período
            }
    """
    params = {
        "campus": campus,
        "curso": curso,
        "periodo-de": periodo_de,
        "periodo-ate": periodo_ate
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/vagas-sisu"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return f"Não foi possível obter os dados dos vagas-sisu do curso {curso} do campus {campus}"
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise


