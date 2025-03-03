from .get_professores_setor import get_professores_setor
from ..campus.utils import get_campus_most_similar
from .utils import get_setor_most_similar
from ..utils.base_url import URL_BASE
from datetime import datetime
from typing import Any
import numpy as np
import requests
import json

def extrair_insights_estagios(estagiarios, uf) -> dict:
    estagiarios_uf = ([
        est for est in estagiarios
        if (est['uf_concedente'] == uf)
    ])
  
    bolsas = [
        float(estagiario['bolsa_mensal']) if estagiario['bolsa_mensal'] is not None else 0 
        for estagiario in estagiarios_uf
    ]
    auxilio_transporte = [
        float(estagiario['auxilio_transporte_diario']) if estagiario['auxilio_transporte_diario'] is not None else 0 
        for estagiario in estagiarios_uf
    ]

    return {
        "total_estagiarios": len(estagiarios_uf),
        "bolsa_mensal_minima": float(f'{min(bolsas):.2f}'),
        "bolsa_mensal_maxima": float(f'{max(bolsas):.2f}'),
        "bolsa_mensal_media": float(f'{np.mean(bolsas):.2f}'),
        "auxilio_transporte_diario_minimo": float(f'{min(auxilio_transporte):.2f}'),
        "auxilio_transporte_diario_maximo": float(f'{max(auxilio_transporte):.2f}'),
        "auxilio_transporte_diario_medio": float(f'{np.mean(auxilio_transporte):.2f}')
    }


def get_estagios(nome_do_campus: Any, nome_do_centro_unidade: Any, ano: Any) -> list:
    """
    Buscar informações sobre estágios dos estudantes de uma centro da unidade de um curso.

    Args:
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se não foi informado ou se quiser saber sobre todos os centros, então passe a string vazia '').
        nome_do_centro_unidade: nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        ano: ano (use o ano perguntado).
    
    Returns:
        Lista com informações relevantes de estágio.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_centro_unidade=str(nome_do_centro_unidade)
    ano=str(ano)
    
    print(f"Tool get_estagios chamada com nome_do_campus={nome_do_campus}, nome_do_centro_unidade={nome_do_centro_unidade} e ano={ano}")
    
    dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
    setor_centro_unidade = get_setor_most_similar(nome_do_centro_setor=nome_do_centro_unidade, nome_do_campus=dados_campus["campus"]["nome"], filtro="UNID")
    
    if str(ano) == "":
        ano = str(datetime.now().year)
    
    params = {
        "inicio-de": str(ano),
        "fim-ate": str(ano)
    }

    response = requests.get(f'{URL_BASE}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)
        professores = get_professores_setor(nome_do_centro_setor=setor_centro_unidade["setor"]["nome"], nome_do_campus=dados_campus["campus"]["nome"])
        professores = [professor['matricula_do_docente'] for professor in professores]

        estagiarios_unidade = [
            estagiario for estagiario in estagiarios
            if (estagiario['matricula_do_docente'] in professores)
        ]
        estados = list({estagiario['uf_concedente'] for estagiario in estagiarios_unidade})
        estados_res = {}
        for uf in estados:
            estados_res[uf] = extrair_insights_estagios(estagiarios=estagiarios_unidade, uf=uf)
        return estados_res
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]