import json
import requests
from ..utils.base_url import URL_BASE

def get_campi() -> list:
    """
    Busca todos os campi/campus/polos da UFCG.
    
    Returns:
        Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """
    response = requests.get(f'{URL_BASE}/campi')

    print("Tool get_campi chamada")

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos campi da UFCG."}]