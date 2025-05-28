from typing import Any
from .utils import get_setor_most_similar
import requests
from ..utils.base_url import URL_BASE
import json

def get_professores_setor(nome_da_unidade_academica: Any, nome_do_centro: Any = "", nome_do_campus: Any = "") -> list:
    """_summary_
    Busca as informações de professores ativos nos setores(centros) da UFCG ou de toda a UFCG. Ou seja, busca quais são os professores.
    
    Args:
        nome_da_unidade_academica: nome da unidade, passe a informação completa como "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        nome_do_centro: nome do centro, passe a informação completa como "centro ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        nome_do_campus: nome do campus. O parametro campus é o nome da cidade e ela pode ser Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Caso queira de toda a UFCG passe o parâmetro com string vazia '').

    Returns:
        Lista com as informações relevantes de professores do(s) setor(es) (centro(s)).
    """

    nome_do_campus=str(nome_do_campus)
    nome_da_unidade_academica=str(nome_da_unidade_academica)
    nome_do_centro=str(nome_do_centro)
    print(f"Tool get_professores chamada com nome_da_unidade_academica={nome_da_unidade_academica}, nome_do_centro={nome_do_centro} e nome_do_campus={nome_do_campus}")
    
    params = { "status": "ATIVO" }
    if (nome_da_unidade_academica != ""):
        dados_setor = get_setor_most_similar(nome_da_unidade_academica=nome_da_unidade_academica, nome_do_campus=nome_do_campus, filtro="UNID")
        params["setor"] = dados_setor["setor"]["codigo"]        
    
    response = requests.get(f'{URL_BASE}/professores', params=params)

    if response.status_code == 200:
        professores = json.loads(response.text)

        if nome_do_centro != "" and not nome_da_unidade_academica:
            dados_setor = get_setor_most_similar(nome_da_unidade_academica=nome_da_unidade_academica, nome_do_campus=nome_do_campus, filtro="CENTRO")
            professores = [professor for professor in professores if str(professor["codigo_do_setor"])[0:2] == str(dados_setor["setor"]["codigo"])[0:2]]
        return professores, f"total de professores: {len(professores)}"
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]