from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_turmas_disciplina(curso: Any, disciplina: Any, turma: Any, periodo_de: Any, periodo_ate: Any) -> list[dict]:
    """
    Retorna informações sobre as turmas de uma disciplina específica de um curso da UFCG,
    incluindo período, carga horária e tipo de oferta.

    Args:
        curso (Any): Código do curso.
        disciplina (Any): Código da disciplina.
        turma (Any): Número da turma.
        periodo_de (Any): Período inicial (ex.: "2020.1").
        periodo_ate (Any): Período final (ex.: "2024.2").

    Returns:
        list[dict]: Lista de turmas no formato:
            {
                "turma": int,                        # Número da turma
                "codigo_da_disciplina": int,          # Código da disciplina
                "periodo": str,                        # Período da disciplina (ex.: "2020.1")
                "numero_de_notas": int,                # Quantidade de notas lançadas
                "quantidade_de_creditos": int,         # Número de créditos da disciplina
                "carga_horaria": int,                  # Carga horária total da disciplina
                "tipo": str                             # Tipo de oferta (ex.: "PRESENCIAL")
            }
    """

    params = { 
        "curso": curso,
        "disciplina": disciplina,
        "periodo-de": periodo_de,
        "periodo_ate": periodo_ate,
        "turma": turma
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/turmas"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter o plano de curso ou nenhum plano de curso foi encontrada"
 
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise