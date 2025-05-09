import requests
import json

from ...tools.utils.base_url import URL_BASE

def obter_disciplina_codigo(codigo: int):
    """
    Obtém informações sobre uma disciplina a partir do seu código.

    Args:
        codigo (str): Código da disciplina.

    Returns:
        dict: Informações sobre a disciplina.
    """

    params = {
        'disciplina': codigo
    }

    url = f"{URL_BASE}/disciplinas"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}




   
    