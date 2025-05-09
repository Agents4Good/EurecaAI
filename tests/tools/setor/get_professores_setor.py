from typing import Any
from .utils import get_setor_most_similar
import requests
from ..utils.base_url import URL_BASE
import json

def get_professores_setor(nome_do_centro_setor: Any, nome_do_campus: Any = "") -> list:
    """
    _summary_
    Busca as informações de professores ativos nos setores(centros) da UFCG ou de toda a UFCG. Ou seja, busca quais são os professores.
    
    Args:
        nome_do_centro_setor: nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        nome_do_campus: nome do campus. O parametro campus é o nome da cidade e ela pode ser Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Caso queira de toda a UFCG passe o parâmetro com string vazia '').

    Returns:
        Lista com as informações relevantes de professores do(s) setor(es) (centro(s)).
    """

    nome_do_campus=str(nome_do_campus)
    nome_do_centro_setor=str(nome_do_centro_setor)
    print(f"Tool get_professores chamada com nome_do_centro_setor={nome_do_centro_setor} e nome_do_campus={nome_do_campus}")
    
    params = { "status": "ATIVO" }
    
    if (nome_do_centro_setor != ""):
        dados_setor = get_setor_most_similar(nome_do_centro_setor=nome_do_centro_setor, nome_do_campus=nome_do_campus, filtro="UNID")
        params["setor"] = dados_setor["setor"]["codigo"]
    
    response = requests.get(f'{URL_BASE}/professores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
