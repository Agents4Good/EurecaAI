import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE

def get_turmas_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, periodo: Any = "", curriculo: Any = "") -> list:
    """
    Retorna todas as turmas de uma disciplina.

    Use esta função quando a pergunta envolver:
    - número da turma;
    - período, carga horária ou tipo da turma.

    Parâmetros:
    - nome_da_disciplina: Nome da disciplina.
    - nome_do_curso: Nome do curso.
    - nome_do_campus: Cidade do campus.
    - periodo: (Opcional) Período do curso.
    - curriculo: (Opcional) Ano do currículo.

    Chame esta função se a pergunta for sobre quais turmas existem para a disciplina.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    curriculo=str(curriculo)
    print(f"Tool get_turmas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, periodo={periodo} e codigo_curriculo={curriculo}")
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)

    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"]
    }
    
    response = requests.get(f'{URL_BASE}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da disciplina porque a disciplina não existe para esse período."}]