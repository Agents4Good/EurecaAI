import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_curriculos(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    """
    
    print(f"Tool get_curriculos chamada com nome_do_curso={str(nome_do_curso)} e nome_do_campus={nome_do_campus}.")
    
    dados_curso = get_curso_most_similar(str(nome_do_curso), str(nome_do_campus))
    response = requests.get(f'{URL_BASE}/curriculos?curso={dados_curso["curso"]["codigo"]}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]