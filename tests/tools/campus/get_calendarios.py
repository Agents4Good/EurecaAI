import json
import requests
from ..utils.base_url import URL_BASE
from typing import Any

def get_calendarios(periodo: Any = "") -> list:
    """_summary_
    Busca todos os calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    
    Args:
        periodo (Any, optional): O periodo letivo que se deseja buscar. Se não for passado, busca todos os periodos letivos. Defaults to "".
    
    Returns:
        list: Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    
    print(f"Tool get_calendarios chamada")
    
    params = { 'campus': '1', 'periodo-de': periodo , 'periodo-ate': periodo }

    response = requests.get(f'{URL_BASE}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]