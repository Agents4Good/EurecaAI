import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_curriculo_mais_recente_curso(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    _summary_
    Buscar o currículo mais recente de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Lista com informações relevantes do currículo mais recente do curso específico.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_curriculo_mais_recente_curso chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso, nome_do_campus)
    print(f"Dados do curso mais similar: {dados_curso}")

    response = requests.get(f'{URL_BASE}/curriculos?curso={dados_curso["curso"]["codigo"]}')

    if response.status_code == 200:
        result = json.loads(response.text)[-1]
        print(f"O currículo mais recente do curso {nome_do_curso} do campus de {nome_do_campus} foi de: {result['codigo_do_curriculo']}")
        return result
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]