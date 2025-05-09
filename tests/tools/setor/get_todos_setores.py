from typing import Any
from ..campus.utils import get_campus_most_similar
import requests
from ..utils.base_url import URL_BASE
import json

def get_todos_setores(nome_do_campus: Any = "", filtro: str = "") -> list:
    """_summary_
    Busca as informações dos setores (centros) do campus da UFCG.
    O parametro nome_do_campus é o nome da cidade e ela pode ser Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
    
    Args:
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se não foi informado ou se quiser saber sobre todos os centros, então passe a string vazia '').
        filtro: passe 'UNID' parametro do filtro se perguntou pelas unidades ou passe 'CENTRO' se perguntou pelos centros. (se não foi informado, ou se perguntar pelo setor, então use a string vazia '').
    
    Returns:
        Lista com informações relevantes do setor (centro) específico.
    """
    
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_setores chamada com campus={nome_do_campus}")
    
    params = {}
    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params = { "campus": dados_campus["campus"]["codigo"] }
    
    response = requests.get(f'{URL_BASE}/setores', params=params)

    if response.status_code == 200:
        result = json.loads(response.text)
        return [setor for setor in result if filtro.lower() in setor["descricao"].lower()]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]