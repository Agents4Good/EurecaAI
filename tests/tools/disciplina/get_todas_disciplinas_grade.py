import json
import requests
from typing import Any
from ..curso.utils import get_curso_most_similar
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..utils.base_url import URL_BASE

def get_todas_disciplinas_grade(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """
    Buscar todas as disciplinas do curso que estão na grade do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    curriculo=str(curriculo)
    
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso} e curriculo={curriculo}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
    
    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': curriculo["codigo_do_curriculo"]
    }

    response = requests.get(f'{URL_BASE}/disciplinas-por-curriculo', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina_curriculo(codigo_do_curso: Any, curriculo: Any, codigo_da_disciplina: Any) -> list:
    """
    Busca por todas as disciplinas da grade do curso.

    Args:
        codigo_do_curso: codigo do curso.
        curriculo: curriculo do curso.
        codigo_da_disciplina: codigo da disciplina

    Returns:
        Retorna todas as informações da disicplina daquela grade.
    """
    
    codigo_da_disciplina=str(codigo_da_disciplina)
    codigo_do_curso=str(codigo_do_curso)
    curriculo=str(curriculo)
    
    params = {
        'curso': codigo_do_curso,
        'curriculo': curriculo,
        'disciplina': codigo_da_disciplina
    }

    response = requests.get(f'{URL_BASE}/disciplinas-por-curriculo?', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]