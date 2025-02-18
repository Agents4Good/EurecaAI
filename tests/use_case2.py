from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import numpy as np
import requests
import json
import asyncio

model = ChatOllama(model="llama3.2:3b", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

def get_cursos_ativos() -> list:
    """
    Buscar todos os cursos da UFCG.

    Args:
    
    Returns:
        Lista de cursos com 'codigo_do_curso' e 'nome'.
    """
    url_cursos = f'{base_url}/cursos'
    params = {
        'status-enum':'ATIVOS',
        'campus': '1'
    }
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'nome': data['descricao']} for data in data_json]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_codigo_curso(nome: str) -> dict:
    """
    Retorna o código e nome do curso.

    Args:
        nome (str): nome do curso.

    Returns:
        dict: dicionário contendo código e nome do curso.
    """
    
    cursos = get_cursos_ativos()

    sentences = [curso["nome"] for curso in cursos]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(nome).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    top_5_cursos = [{"codigo_do_curso": cursos[idx]["codigo_do_curso"], "descricao": cursos[idx]["nome"], "similaridade": similarities[idx]} for idx in top_5_indices]

    possiveis_cursos = []
    for curso in top_5_cursos:
        possiveis_cursos.append(f"{curso['codigo_do_curso']} - {curso['descricao']}")
    
    print(possiveis_cursos)
    
    #f"{curso['codigo_do_curso']} - {curso['descricao']} - Similaridade: {curso['similaridade']:.4f}
    '''return model.invoke(
        f"""
        Para o curso perguntado de nome: "{nome}", quais desses cursos abaixo é mais similar ao curso da pergunta?
        
        {possiveis_cursos}
        
        responda no seguinte formato:
        
        {formato}
        """
    ).content'''
    response = model.invoke(
        f"""
        Para o curso de nome: '{nome}', quais desses possíveis cursos abaixo é mais similar ao curso do nome informado?
        
        {possiveis_cursos}
        
        Responda no seguinte formato:
        
        {formato}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        
        Observação:
        
        'Nome do Curso - M' = é um curso matutino.
        'Nome do Curso - D' = é um curso diurno.
        'Nome do Curso - N' = é um curso noturno.
        """
    )
    print({"messages": [response]})
    return response.content

formato = """{'curso': [{'codigo': '', 'nome': ''}]}"""

resposta = get_codigo_curso("ciências econômicas manhã")
print(resposta)