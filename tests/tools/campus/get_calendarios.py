import json
import requests
from ..utils.base_url import URL_BASE

def get_calendarios() -> list:
    """_summary_
    Busca todos os calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    
    Returns:
        list: Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    
    print(f"Tool get_calendarios chamada")
    
    params = { 'campus': '1' }
    response = requests.get(f'{URL_BASE}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]