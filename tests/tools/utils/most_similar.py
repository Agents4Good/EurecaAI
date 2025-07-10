import json
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import numpy as np
import re

#model_sentence = SentenceTransformer("all-MiniLM-L6-v2")
model_sentence = SentenceTransformer("LeviLima/eureca-finetuned-all-MiniLM-L6-V2")

def get_most_similar(lista_a_comparar: list, dado_comparado: str, top_k: int, mapper: dict, limiar: float) -> tuple:
    """
    Faz a comparação entre uma lista contendo dicionários com informações relevantes com o dado a ser comparado e retorna os top K mais prováveis.

    Args:
        lista_a_comparar (list): Lista contendo dicionários com informações relevantes.
        dado_comparado (str): Dado a ser comparado.
        top_k (int): Número de informações mais similar.
        mapper (dict): Mapeamento da nomenclatura será recebida para retornar no padrão usado pelo RAG para a LLM.
        limiar (float): Nível de similaridade.

    Returns:
        tuple: Retorna os top K mais prováveis.
    """


    descricao = [re.sub(r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x)\b', '', i[mapper["nome"]].lower()).strip() for i in lista_a_comparar]
    embeddings = model_sentence.encode(descricao)
    embedding_query = model_sentence.encode(re.sub(r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x)\b', '', dado_comparado.lower()).strip()).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    
    top_k = [{"nome": lista_a_comparar[idx][mapper["nome"]], "codigo": lista_a_comparar[idx][mapper["codigo"]], "similaridade_cosseno": similarities[idx]} for idx in top_k_indices]
    
    possiveis_k = []
    for k in top_k:
        if k['similaridade_cosseno'] >= limiar:
            possiveis_k.append(f"nome: {k['nome']} - código: {k['codigo']}")
    
    print(f"top_k: {top_k}")
    possiveis_k = [remover_acentos(item) for item in possiveis_k]
    return top_k, possiveis_k # foi trocado a ordem


def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')


# url_disciplinas_computacao = "https://eureca.sti.ufcg.edu.br/das/v2/disciplinas?status=ATIVOS&curso=14102100&curriculo=2023"
# response = requests.get(url_disciplinas_computacao)
# lista_a_comparar = []

# if response.status_code == 200:
#     lista_a_comparar = json.loads(response.text)

# dado_comparado = "cdp"
# mapper = {"nome": "nome", "codigo": "codigo_da_disciplina"}
# print(get_most_similar(lista_a_comparar, dado_comparado, 5, mapper, 0.8))