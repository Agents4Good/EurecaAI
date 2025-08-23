from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_plano_curso_disciplina(curso: Any, disciplina: Any, turma: Any, periodo_de: Any, periodo_ate: Any) -> list[dict]:
    """
    Retorna o plano de ensino (ementa, objetivos, conteúdo, metodologia, avaliação e referências) 
    de uma disciplina específica de um curso da UFCG, dentro de um intervalo de períodos e para uma turma.

    Args:
        curso (Any): Código do curso.
        disciplina (Any): Código da disciplina.
        turma (Any): Número da turma.
        periodo_de (Any): Período inicial (ex.: "2020.1").
        periodo_ate (Any): Período final (ex.: "2024.2").

    Returns:
        list[dict]: Lista com informações detalhadas do plano de curso, no formato:
            {
                "turma": int,                        # Número da turma
                "codigo_da_disciplina": int,          # Código da disciplina
                "nome_da_disciplina": str,            # Nome da disciplina
                "codigo_do_setor": int,               # Código do setor responsável
                "nome_do_setor": str,                 # Nome do setor responsável
                "periodo": str,                        # Período da disciplina (ex.: "2020.1")
                "ementa": str,                         # Ementa da disciplina
                "objetivos": str,                       # Objetivos de aprendizagem
                "conteudo": str,                        # Conteúdo programático detalhado
                "metodologia": str,                     # Metodologia de ensino utilizada
                "avaliacao": str,                       # Critérios de avaliação
                "referencias": str                      # Referências bibliográficas
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
    url = f"{BASE_URL}/planos-de-curso"

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
        
