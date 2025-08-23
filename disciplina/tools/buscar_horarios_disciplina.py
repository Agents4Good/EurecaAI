from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_horarios_disciplina(campus: Any, curso: Any, disciplina: Any, periodo_de: Any, periodo_ate: Any) -> list[dict]:
    """
    Retorna os horários das aulas de uma disciplina específica de um curso da UFCG, 
    dentro de um intervalo de períodos.

    Args:
        campus (Any): Código do campus.
        curso (Any): Código do curso.
        disciplina (Any): Código da disciplina.
        periodo_de (Any): Período inicial (ex.: "2024.1").
        periodo_ate (Any): Período final (ex.: "2024.2").

    Returns:
        list[dict]: Lista de horários no formato:
            {
                "turma": int,                         # Número da turma
                "codigo_da_disciplina": int,           # Código da disciplina
                "nome_da_disciplina": str,             # Nome da disciplina
                "codigo_do_setor": int,                # Código do setor responsável
                "nome_do_setor": str,                  # Nome do setor responsável
                "campus": int,                         # Código do campus
                "nome_do_campus": str,                 # Nome do campus
                "quantidade_de_creditos": int,         # Quantidade de créditos da disciplina
                "carga_horaria": int,                  # Carga horária total da disciplina
                "periodo": str,                        # Período da disciplina (ex.: "2024.2")
                "dia": int,                             # Dia da semana (1=Segunda, 2=Terça, ...)
                "hora_de_inicio": str,                  # Hora de início da aula (formato HH:MM)
                "hora_de_termino": str,                 # Hora de término da aula (formato HH:MM)
                "codigo_da_sala": str                   # Código da sala onde a aula ocorrerá
            }
    """

    params = {
        "campus": campus, 
        "curso": curso,
        "disciplina": disciplina,
        "periodo-de": periodo_de,
        "periodo-ate": periodo_ate
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/horarios"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter os horarios ou nenhum horario foi encontrada"
 
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        
