import requests
import json
import sys
#configuração pra não dar problema na importação
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#base_url = "https://eureca.sti.ufcg.edu.br/das/v2"
base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"


def get_campi() -> list:
    """
    Buscar todos os campi.

    Args:
        base_url: URL base da API.
    
    Returns:
        Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

def get_calendarios() -> list:
    """
    Buscar calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.

    Args:
        base_url: URL base da API.

    Returns:
        Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    #print(f"Tool get_calendarios chamada com base_url={base_url}")
    params = {
        'campus': '1'
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]


def get_periodo_mais_recente() -> str:
    """
    Buscar o período mais recente da universidade.

    Args:
        base_url: URL base da API.

    Returns:
        String com o período mais recente (como '2010.1').
    """
    params = {
        'campus': '1'
    }
    #print(f"Tool get_periodo_mais_recente chamada com base_url={base_url}")
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)[-1]
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]
    

