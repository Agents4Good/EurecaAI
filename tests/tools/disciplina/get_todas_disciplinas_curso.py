import json
import requests
from typing import Any
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_todas_disciplinas_curso(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """
    Busca todas as discplinas ofertadas de um curso. Usar apenas quando for perguntado sobre apenas as disciplinas que o curso oferece.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Retorna uma lista de disciplinas ofertadas pelo curso.
    """

    curriculo = str(curriculo)
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)

    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo["codigo_do_curriculo"]
    }

    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    

def get_disciplinas_curso_por_codigo(codigo_do_curso: Any, curriculo: Any) -> list:
    """
    Buscar todas as disciplinas de um curso. Usar apenas se tiver o código da disciplina.

    Args:
        codigo_do_curso: codigo do curso.
        curriculo: valor inteiro do ano (se não tiver, use a string vazia '').
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    """
    
    codigo_do_curso = str(codigo_do_curso)
    curriculo = str(curriculo)
    
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={codigo_do_curso} e curriculo={curriculo}.")
    
    params = {
        'curso': codigo_do_curso,
        'curriculo': curriculo
    }

    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]