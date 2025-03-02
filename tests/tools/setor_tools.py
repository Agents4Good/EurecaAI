import requests
import numpy as np
import json
from langchain_core.tools import tool
from datetime import datetime
from typing import Any
from .campus_tools import *

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"
format = """{'setor': {'codigo': '', 'nome': ''}}"""

def get_setores(campus: Any = "") -> list:
    """
    Busca as informações dos setores (centros) do campus da UFCG.
    O parametro campus é o nome da cidade e ela pode ser Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
    
    Args:
        campus: nome do campus (se não foi informado ou se quiser saber sobre todos os centros, então passe a string vazia '').

    Returns:
        Lista com informações relevantes do setor (centro) específico.
    """
    
    print(f"Tool get_setores chamada com campus={campus}")
    
    params = {}
    if (str(campus) != ""):
        campus = get_campus_most_similar(campus=str(campus))
        params = { "campus": campus["campus"]["codigo"] }
    
    response = requests.get(f'{base_url}/setores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def processar_json_setor(json_str: str):
    try:
        result = json.loads(json_str.replace("'", '"'))

        if 'setor' not in result or not isinstance(result['setor'], dict):
            return "Erro: Estrutura do JSON inválida. A chave 'setor' deve ser um dicionário."
        if 'codigo' not in result['setor'] or not result['setor']['codigo']:
            return "Erro: O campo 'codigo' está ausente ou vazio."
        '''if 'nome' not in result['setor'] or not result['setor']['nome']:
            return "Erro: O campo 'nome' está ausente ou vazio."'''
        return result
    except json.JSONDecodeError:
        raise ValueError("Erro: A string fornecida não é um JSON válido.")


def get_setor_most_similar(setor: Any, campus: Any, filtro: str = ""):
    """
    Busca o código do setor pelo nome dele.

    Args:
        setor: nome do setor.
        campus: nome do campus.

    Returns:
        dict: dicionário contendo código e o nome do setor.
    """
    campus_similar = get_campus_most_similar(str(campus))
    setores_campus = get_setores(campus=campus_similar["campus"]["nome"])
    setores_campus = [setor_ for setor_ in setores_campus if filtro.lower() in setor_["descricao"].lower()]
    sentences = [setor["descricao"] for setor in setores_campus]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(setor).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_5_indices = np.argsort(similarities)[-5:][::-1]
    
    print(top_5_indices)

    top_5_setores = [{
        "nome": setores_campus[idx]["descricao"], 
        "codigo": setores_campus[idx]["codigo_do_setor"], 
        "campus": setores_campus[idx]["campus"], 
        "similaridade": similarities[idx]} 
        for idx in top_5_indices
    ]

    print(top_5_setores)
    possiveis_cursos = []
    for curso in top_5_setores:
        if curso['similaridade'] >= 0.6:
            possiveis_cursos.append(f"{curso['nome']} - código: {curso['codigo']}")
    
    def remover_acentos(texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    lista_tratada = [remover_acentos(item) for item in possiveis_cursos]
    
    print(lista_tratada)
    if len(lista_tratada) == 0:
        return "Não foi encontrado um setor com esse nome"
        
    response = model.invoke(
        f"""
        Para o setor de nome: '{setor}', quais desses possíveis setores abaixo é mais similar ao setor do nome informado?
        
        {lista_tratada}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    result = processar_json_setor(response.content)
    print(result)
    return result


# Reportar esse problema a fubica
def get_professores(setor_centro: Any, campus: Any = "") -> list:
    """
    Busca as informações de professores ativos nos setores(centros) da UFCG ou de toda a UFCG. Ou seja, busca quais são os professores.
    
    Args:
        setor_centro: nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        campus: nome do campus. O parametro campus é o nome da cidade e ela pode ser Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Caso queira de toda a UFCG passe o parâmetro com string vazia '').

    Returns:
        Lista com as informações relevantes de professores do(s) setor(es) (centro(s)).
    """

    print(f"Tool get_professores chamada com setor_centro={setor_centro} e campus={campus}")

    params = {}
    
    if (str(setor_centro) != ""):
        campus = get_campus_most_similar(campus=str(campus))
        setor = get_setor_most_similar(setor=setor_centro, campus=campus["campus"]["nome"], filtro="UNID")
        
        params = {
            "status": "ATIVO",
            "setor": setor["setor"]["codigo"]
        }
    
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


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


def get_estagios(nome_do_campus: Any, nome_do_centro_unidade: Any, ano: Any = "") -> list:
    """
    Buscar informações sobre estágios dos estudantes de uma centro da unidade de um curso.

    Args:
        nome_do_campus: nome do campus.
        nome_do_centro_unidade: nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        ano: ano (se não foi informado, use a string vazia '' para obter informações do ano atual).
    
    Returns:
        Lista com informações relevantes de estágio.
    """
    
    print(f"Tool get_estagios chamada com nome_do_campus={nome_do_campus}, nome_do_centro_unidade={nome_do_centro_unidade} e ano={ano}")
    
    campus = get_campus_most_similar(campus=str(nome_do_campus))
    setor_centro_unidade = get_setor_most_similar(setor=nome_do_centro_unidade, campus=campus["campus"]["nome"], filtro="UNID")
    
    if str(ano) == "":
        ano = str(datetime.now().year)
    
    params = {
        "inicio-de": str(ano),
        "fim-ate": str(ano)
    }

    response = requests.get(f'{base_url}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)
        professores = get_professores(setor_centro_unidade["setor"]["nome"], campus=nome_do_campus)
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
    