from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
import requests
import json

def obter_dados_de_curso_especifico(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    _summary_
    Buscar informação de um curso específico da UFCG a partir do nome do curso.
    Use esta função APENAS quando a pergunta mencionar um ou mais cursos específicos pelo nome.
    
    Exemplos de uso:
        - "O curso de Engenharia Elétrica é oferecido em qual turno?"
        - "Qual o código do curso de Direito?"
        - "Francês e Inglês são oferecidos em que turno?"
    
    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus. Se o nome do campus não tiver sido fornecido, use 'campina grande' por padrão.
    
    Returns:
        Lista com informações relevantes do curso específico, como código do curso, código do inep, código e nome do setor desse curso, período de início, etc.
    """

    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    print(f"Tool `obter_dados_de_curso_especifico` chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")

    try:
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    except ValueError as e:
        return [{"Error": str(e)}]

    if 'AskHuman' in dados_curso:
        return dados_curso

    params = { 
        'status-enum': 'ATIVOS',
        'curso': dados_curso['curso']['codigo']
    }
    response = requests.get(f'{URL_BASE}/cursos', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]