import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE


def get_todos_curriculos_do_curso(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    _summary_
    Buscar pelos currículos de um único curso.
    Chame essa ferramenta passando apenas um único curso por vez. Se houver mais de um curso, você deve chamar essa ferramenta para cada curso.
    Essa ferramenta tem informações sobre o número de créditos e carga horária das disciplinas para que possa estar cursando as disciplinas no período e o número de créditos e carga horária para que o estudante possa se formar no curso. 
    Além disso, essa ferramenta tem dados sobre a soma número de cŕeditos e carga horária necessárias nas disciplinas de cada período para poder estudar no período.
    
    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
    
    Returns:
        Lista com informações relevantes do currículo de um curso específico.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_todos_curriculos_do_curso chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso, nome_do_campus)

    response = requests.get(f'{URL_BASE}/curriculos?curso={dados_curso["curso"]["codigo"]}')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_todos_curriculos_do_curso_por_codigo(codigo_do_curso: Any) -> list:
    """
    Buscar o currículo mais recente de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Lista com informações relevantes do currículo mais recente do curso específico.
    """
    
    codigo_do_curso=str(codigo_do_curso)    
    response = requests.get(f'{URL_BASE}/curriculos?curso={codigo_do_curso}')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]