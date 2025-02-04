import requests
import numpy as np
import json
from langchain_core.tools import tool
from datetime import datetime
from strawberry_demo.main import schema
from .default_data.default_setor_data import *
from .url_config import base_url

@tool
def get_setores(data: str = default_setor):
    """
    Busca as informações de setor (centro) do campus da UFCG.
    """
    try:
        query = f"""query{{
                    setores {{
                        {data}
                    }}
                }}"""
        
        print(f"Tool get_setores com data {data}")
        result = schema.execute_sync(query);
        return result.data["setores"]
    except Exception as e:
        return e

@tool
def get_professores(codigo_do_setor: str, data: str = default_professor):
    """
    Busca as informações de professores de um setor (centro).
    """
    try:
        query = f"""query{{
                    professores(codigoDoSetor: "{codigo_do_setor}") {{
                        {data}
                    }}
                }}"""
        
        variables = {
            "codigoDoSetor": codigo_do_setor
        }
        print(f"Tool get_professoes setor {codigo_do_setor} e data {data}")
        result = schema.execute_sync(query, variable_values=variables);
        return result.data["professores"]
    except Exception as e:
        return e
    
@tool
def get_total_professores(codigo_do_setor: str, data: str = default_professor):
    """
    Busca a quantidade total de professores de um setor (unidade).
    """

    try:
        query = f"""query{{
                    professores(codigoDoSetor: "{codigo_do_setor}") {{
                        {data}
                    }}
                }}"""
        
        variables = {
            "codigoDoSetor": codigo_do_setor
        }
        print(f"Tool get__total_professoes setor {codigo_do_setor} e data {data}")
        result = schema.execute_sync(query, variable_values=variables);
        return result.data["professores"]
    except Exception as e:
        return e

#função auxiliar
def extrair_insights_estagios(estagiarios, uf):
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

@tool
def get_estagios(ano: str, setor_centro_unidade: str) -> list:
    """
    Buscar informações sobre estágios.

    Args:
        base_url: URL base da API.
        ano: ano de estágio.
        setor_centro_unidade: 'código_setor' (centro ou unidade) do campus.
    
    Returns:
        Lista com informações relevantes de estágio.
    
    Nota:
        Para usar este método, se o 'setor_centro_unidade' (código do setor) não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_setores` baseado no nome do centro ou unidade fornecido pelo usuário.
        Da mesma forma, caso o ano de estágio não tiver sido informado pelo usuário, passe a string vazia.
    """
    if ano == "" or not ano:
        ano = str(datetime.now().year)
    params = {
        "inicio-de": ano,
        "fim-ate": ano
    }

    print(f"Tool get_estagios com ano {ano}, setor {setor_centro_unidade}")
    response = requests.get(f'{base_url}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)
        professores = get_professores(base_url, setor_centro_unidade)
        professores = [professor['matricula_do_docente'] for professor  in professores]

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
    

#DOCUMENTAÇÃO DAS TOOLS
get_setores.__doc__ = f"""   
    Args:
        data: campos a serem retornados, por padrão é {default_setor}
    
    Returns:
        Lista com informações desejadas do setores. Por padrão é {default_setor}
"""

get_professores.__doc__ = f""" 
    Args:
        setor_centro: 'código_setor' (centro) do campus.
        data: campos a serem retornados, por padrão é {default_professor}

    Returns:
        Lista com as informações desejadas de professores de um setor (centro). Por padrão é {default_professor}
"""

get_total_professores.__doc__ = f""" 
    Returns:
        String que representa o total de professores de um setor (unidade).
       
    Exemplo:
        "44 professores".
    Nota:
        Para usar este método, se o 'setor_unidade' (código do setor) não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_setores` baseado no nome da unidade fornecido pelo usuário.
        Se o nome da unidade não tiver sido informado, e tiver sido informado 'UFCG' use uma string vazia como entrada para 'setor_unidade'.
"""