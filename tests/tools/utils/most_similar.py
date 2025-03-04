from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import numpy as np

model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

def get_most_similar(lista_a_comparar: list, dado_comparado: str, top_k: int, mapper: dict, limiar: float) -> tuple:
    descricao = [i[mapper["nome"]] for i in lista_a_comparar]
    embeddings = model_sentence.encode(descricao)
    embedding_query = model_sentence.encode(dado_comparado).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        
    top_k = [{"nome": lista_a_comparar[idx][mapper["nome"]], "codigo": lista_a_comparar[idx][mapper["codigo"]], "similaridade_cosseno": similarities[idx]} for idx in top_k_indices]

    possiveis_k = []
    for k in top_k:
        if k['similaridade_cosseno'] >= limiar:
            possiveis_k.append(f"nome: {k['nome']} - código: {k['codigo']}")
    
    def remover_acentos(texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    return [remover_acentos(item) for item in possiveis_k], top_k