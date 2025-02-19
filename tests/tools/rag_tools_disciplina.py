from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

import numpy as np
import requests
import json

model = ChatOllama(model="llama3.2:3b", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

format = """{'disciplina': {'codigo': '', 'nome': ''}}"""

def get_disciplinas_curso(codigo_curriculo: str) -> list:
    """
    Buscar todas as disciplinas do curso de Ciência da Computação da UFCG.

    Args:
        codigo_curriculo: código do currículo.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
    """
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}.")
    params = {
        'curso': '14102100',
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina(nome_disciplina: str, codigo_curriculo: str = "2023"): 
    """
        Retorna o código e o nome da disciplina

        Args:
            nome_disciplina: nome da disciplina
            codigo_curriculo: codigo do curriculo, por padrão, é 2023
        Returns:
            dicionário contendo nome e codigo da disciplina
    """

    disciplinas = get_disciplinas_curso(codigo_curriculo)

    sentences = [disciplina["nome"] for disciplina in disciplinas]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(nome_disciplina).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    top_5_disciplinas = [{"codigo": disciplinas[idx]["codigo_da_disciplina"], "nome": disciplinas[idx]["nome"], "similaridade": similarities[idx]} for idx in top_5_indices]

    print("TOP 5 ", top_5_disciplinas)

    possiveis_disciplinas = []
    for disciplina in top_5_disciplinas:
        if disciplina['similaridade'] >= 0.6:
            possiveis_disciplinas.append(f"{disciplina['codigo']} - {disciplina['nome']}")

    if len(possiveis_disciplinas) == 0:
        return "DISCIPLINA NÃO EXISTE"

    print(possiveis_disciplinas)

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?
    
        {possiveis_disciplinas}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).       
        """   
    )

    return response.content

print(get_disciplina("calculo avançado", "2023"))


