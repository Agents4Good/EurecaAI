import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_horarios_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, turma: Any, periodo: Any = "", curriculo: Any = "") -> list:
    """
    Busca os horários e a número da sala de uma disciplina de uma turma.
    Use essa ferramenta quando quiser informações sobre:
    - setor responsável;
    - período;
    - dia em que a aula ocorre;
    - horário de início e término da aula;
    - código da sala.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        turma: número da turma (se for para todas as turmas usar a string vazia '').
        periodo: período do curso (se não souber, então use a string vazia '' para usar o período mais recente).
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo", se não souber use a string vazia '' para usar o currículo mais recente).
    
    Returns:
        Retorna uma lista de horários das aulas da disciplina.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    turma=str(turma)
    periodo=str(periodo)
    curriculo=str(curriculo)
    print(f"Tool get_horarios_disciplinas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, turma={turma} e curriculo={curriculo}")
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
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