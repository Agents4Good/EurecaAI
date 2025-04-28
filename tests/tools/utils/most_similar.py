from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import numpy as np

import re
from unidecode import unidecode

model_sentence = SentenceTransformer("all-MiniLM-L6-v2")
model_for_names = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

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

def get_sim_course_name(course1: str, course2: str) -> float:
    c1_normalized = normalize_text(course1)
    c2_normalized = normalize_text(course2)

    emb1 = model_for_names.encode(c1_normalized, convert_to_tensor=True)
    emb2 = model_for_names.encode(c2_normalized, convert_to_tensor=True)
    
    return util.cos_sim(emb1, emb2).item()

def normalize_text(text):
    text = unidecode(text.lower())
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text