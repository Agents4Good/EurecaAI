from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_professores_por_setor(campus:Any, setor:Any) -> list[dict]:
    """
    Retorna todos os professores de um setor específico de um campus da UFCG.

    Args:
        campus (Any): Código do campus.
        setor (Any): Código do setor.

    Returns:
        list[dict]: Lista de professores no formato:
            {
                "matricula_do_docente": int,   # Matrícula do docente
                "nome": str,                    # Nome completo do professor
                "codigo_do_setor": int,         # Código do setor ao qual pertence
                "email": str | None,            # E-mail institucional
                "status": str,                  # Status do docente (ex.: "ATIVO")
                "cpf": str,                     # CPF do docente
                "siape": int,                    # Número SIAPE
                "titulacao": str                 # Código da titulação
            }
    """

    params = {
        "status": "ATIVO",
        "campus": campus, 
        "setor": setor
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/professores"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter os professores ou nenhum professor foi encontrado"
 
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        