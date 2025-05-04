from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import numpy as np

model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

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
    
    descricao = [i[mapper["nome"]].lower() for i in lista_a_comparar]
    embeddings = model_sentence.encode(descricao)
    embedding_query = model_sentence.encode(dado_comparado.lower()).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    
    top_k = [{"nome": lista_a_comparar[idx][mapper["nome"]], "codigo": lista_a_comparar[idx][mapper["codigo"]], "similaridade_cosseno": similarities[idx]} for idx in top_k_indices]
    
    possiveis_k = []
    for k in top_k:
        if k['similaridade_cosseno'] >= limiar:
            possiveis_k.append(f"nome: {k['nome']} - código: {k['codigo']}")
    
    possiveis_k = [remover_acentos(item) for item in possiveis_k]
    return possiveis_k, top_k


def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')