import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_plano_de_aulas(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, periodo: Any = "", numero_da_turma: Any = "", curriculo: Any = "") -> list:
    """
    Retorna o plano de aulas de uma turma.

    Use esta função quando a pergunta envolver:
    - número, data ou duração das aulas;
    - conteúdo abordado em cada aula.

    Parâmetros:
    - nome_do_curso: Nome do curso.
    - nome_do_campus: Cidade do campus.
    - nome_da_disciplina: Nome da disciplina.
    - periodo: (Opcional) Período do curso.
    - numero_da_turma: (Opcional) Número da turma ("01" se não informado).
    - curriculo: (Opcional) Ano do currículo.

    Chame esta função se a pergunta for sobre o cronograma de aulas da disciplina.
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