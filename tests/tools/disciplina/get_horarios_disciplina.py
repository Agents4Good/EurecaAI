import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE
from ..utils.validacoes import validar_periodo

def get_horarios_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, turma: Any = "01", periodo: Any = "") -> list:
    """_summary_
    Retorna os horários e sala de aula de uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - dia, horário ou sala da aula;
    - setor responsável ou período da disciplina.
    
    Args:
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        nome_da_disciplina (Any): Nome da disciplina.
        turma (Any): Número da turma. Defaults to "01".
        periodo (Any, optional): Número da turma ("" para todas). Defaults to "".

    Returns:
        list: Chame esta função se a pergunta for sobre quando e onde a disciplina ocorre.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    turma=str(turma)
    periodo=str(periodo)
    curriculo=str(curriculo)
    print(f"Tool get_horarios_disciplinas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, turma={turma} e curriculo={curriculo}")
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    else:
        validou_periodo, mensagem = validar_periodo(periodo=periodo)
        if not validou_periodo: return mensagem
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    
    params = {
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma,
        "periodo-de": periodo,
        "periodo-ate": periodo
    }
    response = requests.get(f'{URL_BASE}/horarios', params=params)

    if response.status_code == 200:
        horarios = json.loads(response.text)
            
        filtros_horarios = []
        turmas_map = {}

        for horario in horarios:
            turma = horario['turma']
            sala = horario['codigo_da_sala']
            dia = str(horario['dia'])
            horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

            if turma not in turmas_map:
                turmas_map[turma] = { 'turma': turma, 'sala': sala, 'horarios': {} }
                filtros_horarios.append(turmas_map[turma])

            turmas_map[turma]['horarios'][dia] = horario_formatado

        return filtros_horarios
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]