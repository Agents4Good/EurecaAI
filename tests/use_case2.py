from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import numpy as np
import requests
import json
import asyncio

model = ChatOllama(model="llama3.1:8b", temperature=0)
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
    print("chamando a tool get_cursos_ativos.")
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'nome': data['descricao']} for data in data_json]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

async def get_informacoes_curso(nome: str) -> dict:
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
    
    #f"{curso['codigo_do_curso']} - {curso['descricao']} - Similaridade: {curso['similaridade']:.4f}
    return await model.ainvoke(
        f"""
        Para o curso perguntado de nome: "{nome}", quais desses cursos abaixo é mais similar ao curso da pergunta?
        
        {possiveis_cursos}
        """
    ).content
    

resposta = asyncio.run(get_informacoes_curso("COMPUTAÇÃO"))
print(resposta)