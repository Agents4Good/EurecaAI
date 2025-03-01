import requests
import json
from langchain_core.tools import tool

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

def get_campi() -> list:
    """
    Buscar todos os campi/campus/polos da UFCG.
    
    Returns:
        Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos campi da UFCG."}]


def get_calendarios() -> list:
    """
    Buscar calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    
    Returns:
        Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    
    params = {
        'campus': '1'
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_periodo_mais_recente() -> str:
    """
    Busca pelo calendário(período) mais recente(atual) da universidade (período atual da UFCG).
    
    Returns:
        String com o período mais recente.
    """
    
    params = {
        'campus': '1'
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)[-1]['periodo']
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
