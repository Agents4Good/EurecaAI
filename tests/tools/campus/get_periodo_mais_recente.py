from ..utils.base_url import URL_BASE
import requests
import json

def get_periodo_mais_recente() -> str:
    """_summary_
    Busca pelo calendário(período) mais recente(atual) da universidade (período atual da UFCG). Ou seja, em que período estamos hoje.
    
    Returns:
        str: String com o período mais recente.
    """
    
    print("Tool get_periodo_mais_recente chamada")
    
    params = { 'campus': '1' }
    response = requests.get(f'{URL_BASE}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)[-1]["periodo"]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]