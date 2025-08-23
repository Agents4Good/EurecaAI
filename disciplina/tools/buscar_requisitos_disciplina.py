from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_requisitos_disciplina(curso: Any, disciplina: Any, curriculo: Any) -> list[dict]:
    """
    Retorna os requisitos (disciplinas pré-requisito ou co-requisito) de uma disciplina específica
    de um curso e currículo da UFCG.

    Args:
        curso (Any): Código do curso.
        disciplina (Any): Código da disciplina.
        curriculo (Any): Código do currículo.

    Returns:
        list[dict]: Lista de requisitos no formato:
            {
                "codigo_do_curso": int,             # Código do curso
                "codigo_da_disciplina": int,         # Código da disciplina alvo
                "codigo_do_curriculo": str,          # Código do currículo
                "ordem_de_prioridade": int,          # Ordem de prioridade do requisito
                "condicao": int,                     # Código da disciplina exigida
                "operador": str                       # Operador lógico da condição ("E" ou "")
            }
    """

    params = {
        "curso": curso,
        "disciplina": disciplina,
        "curriculo": curriculo
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/pre-requisito-disciplinas"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter os requisitos ou nenhum requisito foi encontrada"
 
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        