import json
import requests
from typing import Any
from ..curso.utils import get_curso_most_similar
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..utils.base_url import URL_BASE

def get_todas_disciplinas(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """
    Busca por todas as disciplinas ofertadas do curso que estão na grade do curso.

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
    print(f"Tool get_todas_disciplinas chamada com nome_do_campus={nome_do_campus} nome_do_curso={nome_do_curso} e curriculo={curriculo}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    if (curriculo == ""):
        dados_curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        curriculo = dados_curriculo["codigo_do_curriculo"]

    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': curriculo
    }
    
    response = requests.get(f'{URL_BASE}/disciplinas-por-curriculo', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]