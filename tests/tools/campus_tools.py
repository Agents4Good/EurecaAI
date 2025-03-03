import requests
import json
from langchain_core.tools import tool

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from .utils.preprocess_text import remove_siglas
from typing import Any
from .curso_tools import *
import unicodedata

import numpy as np

model = ChatOllama(model="llama3.2:3b", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

format = """{'campus': {'codigo': '', 'nome': ''}}"""
base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

def processar_json_campus(json_str: str):
    try:
        result = json.loads(json_str.replace("'", '"'))

        if 'campus' not in result or not isinstance(result['campus'], dict):
            return "Erro: Estrutura do JSON inválida. A chave 'campus' deve ser um dicionário."
        if 'codigo' not in result['campus'] or not result['campus']['codigo']:
            return "Erro: O campo 'codigo' está ausente ou vazio."
        '''if 'nome' not in result['campus'] or not result['campus']['nome']:
            return "Erro: O campo 'nome' está ausente ou vazio."'''
        return result
    except json.JSONDecodeError:
        raise ValueError("Erro: A string fornecida não é um JSON válido.")


def get_campi() -> list:
    """
    Busca todos os campi/campus/polos da UFCG.
    
    Returns:
        Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """
    response = requests.get(f'{base_url}/campi')

    print("Tool get_campi chamada")

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos campi da UFCG."}]


def get_calendarios() -> list:
    """
    Busca todos os calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    
    Returns:
        Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    
    print(f"Tool get_calendarios chamada")
    
    params = { 'campus': '1' }
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
    
    print("Tool get_periodo_mais_recente chamada")
    
    params = { 'campus': '1' }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)[-1]['periodo']
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_campus_most_similar(campus: str):
    """
    Busca o código do campus pelo nome dele.

    Args:
        campus: nome do campus.

    Returns:
        dict: dicionário contendo código, representação e o nome do campus.
    """
    campi = get_campi()

    sentences = [campus["descricao"] for campus in campi]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(campus).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_3_indices = np.argsort(similarities)[-3:][::-1]
    
    top_3_cursos = [{
        "nome": campi[idx]["descricao"], 
        "codigo": campi[idx]["campus"], 
        "representacao": campi[idx]["representacao"], 
        "similaridade": similarities[idx]} 
        for idx in top_3_indices
    ]

    possiveis_cursos = []
    for curso in top_3_cursos:
        if curso['similaridade'] >= 0.65:
            possiveis_cursos.append(f"{curso['nome']} - código: {curso['codigo']}")
    
    def remover_acentos(texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    lista_tratada = [remover_acentos(item) for item in possiveis_cursos]
    
    if len(lista_tratada) == 0:
        return "Não foi encontrado um campus com esse nome"
        
    response = model.invoke(
        f"""
        Para o campus de nome: '{campus}', quais desses possíveis cursos abaixo é mais similar ao campus do nome informado?
        
        {lista_tratada}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    result = processar_json_campus(response.content)
    return result