from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_matriculas_disciplinas(campus: Any, curso: Any, disciplina: Any, periodo_de: Any, periodo_ate: Any, turma: Any ) -> list[dict]:
    """
    Retorna informações sobre as matrículas de estudantes em uma disciplina específica de um curso da UFCG,
    dentro de um intervalo de períodos e para uma turma específica.

    Args:
        campus (Any): Código do campus.
        curso (Any): Código do curso.
        disciplina (Any): Código da disciplina.
        periodo_de (Any): Período inicial (ex.: "2020.1").
        periodo_ate (Any): Período final (ex.: "2024.2").
        turma (Any): Identificação da turma (ex: 01, 02...)

    Returns:
        list[dict]: Lista de matrículas no formato:
            {
                "matricula_do_estudante": str,      # Matrícula do estudante
                "codigo_da_disciplina": int,        # Código da disciplina
                "nome_da_disciplina": str,          # Nome da disciplina
                "periodo": str,                     # Período da matrícula (ex.: "2019.2")
                "turma": int,                        # Número da turma
                "status": str,                       # Status do aluno na disciplina (ex.: "Aprovado", "Reprovado")
                "tipo": str | None,                  # Tipo de matrícula/componente, se houver
                "media_final": float | None,         # Média final obtida na disciplina
                "dispensas": Any | None              # Dispensas concedidas, se houver
            }
    """

    params = {
        "campus": campus, 
        "curso": curso,
        "disciplina": disciplina,
        "periodo-de": periodo_de,
        "periodo_ate": periodo_ate,
        "turma": turma
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/matriculas"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter as matriculas ou nenhum matricula foi encontrada"
 
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        
