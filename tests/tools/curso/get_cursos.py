import json
import requests
from typing import Any
from ..utils.base_url import URL_BASE
from ..campus.get_campi import get_campi
from ..campus.utils import get_campus_most_similar

def get_cursos(nome_do_campus: Any = "") -> list:
    """
    Busca por todos os cursos da UFCG por campus.

    Args:
    nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''. 

    Returns:
        Lista de cursos com 'codigo_do_curso' e 'nome'.
    """
    
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_cursos chamada com nome_do_campus={nome_do_campus}")
    
    params = {
        'status-enum':'ATIVOS',
    }

    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]
    
    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'descricao': data['descricao']} for data in data_json]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]