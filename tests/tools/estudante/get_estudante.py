import requests, json
from typing import Any
from ..utils.base_url import URL_BASE
from langchain_core.tools import tool

@tool
def estudante_info(matricula: Any, token: Any) -> dict:
    """
    Use esta função quando a pergunta do usuário for sobre as informações acadêmicas dele mesmo. Como: métricas (CRA, IEA, MC, ...), dados pessoais, créditos, etc.
    """
    matricula = str(matricula)
    token = str(token)

    params = {"estudante": matricula}

    headers = {
        "accept": "application/json",
        "token-de-autenticacao": token
    }

    response = requests.get(f'{URL_BASE}/estudantes/estudante', params=params, headers=headers)
    
    if response.status_code == 200:
        dados = json.loads(response.text)
        return dados
    else:
        return {"erro_status": response.status_code, "msg": response.text}