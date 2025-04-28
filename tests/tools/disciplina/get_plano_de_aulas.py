import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_plano_de_aulas(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, periodo: Any = "", numero_da_turma: Any = "", curriculo: Any = "") -> list:
    """
    Busca o plano de aulas de uma turma de uma disciplina. 
    Use essa ferramenta quando quiser informações sobre:
    - período;
    - número da aula;
    - data em que a aula irá ocorrer;
    - número de horas de aula.
    - assunto abordado durante a aula.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        periodo: periodo do curso (se não souber ou não foi informado, então passe a string vazia '').
        numero_da_turma: valor numérico da turma (se não souber, use a turma '01' como a turma padrão).
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo", se não souber use a string vazia '' para usar o currículo mais recente).

    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    curriculo=str(curriculo)
    numero_da_turma=str(numero_da_turma)
    periodo=str(periodo)
    print(f"Tool get_plano_de_aulas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, periodo={periodo}, numero_turma={numero_da_turma} e curriculo={curriculo}.")
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        'disciplina': dados_disciplina["disciplina"]["codigo"],
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': numero_da_turma
    }

    response = requests.get(f'{URL_BASE}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]