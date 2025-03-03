from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
import requests
import json

def get_curso(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar informação de um curso da UFCG a partir do nome do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus.

    Returns:
        Lista com informações relevantes do curso específico, como código do inep, código e nome do setor desse curso, período de início, etc.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    print(f"Tool get_informacoes_curso chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    print(dados_curso)

    params = {
        'status-enum': 'ATIVOS',
        'curso': dados_curso['curso']['codigo']
    }
    
    response = requests.get(f'{URL_BASE}/cursos', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]