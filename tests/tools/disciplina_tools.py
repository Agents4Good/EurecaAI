from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from .utils.preprocess_text import remove_siglas
from typing import Any
from .curso_tools import *

import numpy as np
import requests
import json

model = ChatOllama(model="llama3.1", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

format = """{'disciplina': {'codigo': '', 'nome': ''}}"""

def get_disciplinas_curso(codigo_curriculo: Any = "2023") -> list:
    """
    Buscar todas as disciplinas do curso de Ciência da Computação da UFCG.

    Args:
        codigo_curriculo: String que representa o código do currículo ex: '2022'.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
    """
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}.")
    params = {
        'curso': '14102100',
        'curriculo': str(codigo_curriculo)
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_disciplina(nome_disciplina: Any, codigo_curriculo: str = "2023") -> dict:
    """
    Buscar o nome e o código de uma disciplina.

    Args:
        nome_disciplina: nome da disciplina.
        codigo_curriculo: codigo do curriculo, por padrão, é 2023.

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """
    
    nome_disciplina = remove_siglas(str(nome_disciplina))
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
        if disciplina['similaridade'] >= 0.65:
            possiveis_disciplinas.append(f"{disciplina['codigo']} - {disciplina['nome']}")

    if len(possiveis_disciplinas) == 0:
        return "Não foi encontrado uma disciplina com esse nome"

    format = """{'disciplina': {'codigo': '', 'nome': ''}}"""
    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        {possiveis_disciplinas}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    result = processar_json(response.content)
    return result


def processar_json(json_str: str):
    try:
        result = json.loads(json_str.replace("'", '"'))

        if 'disciplina' not in result or not isinstance(result['disciplina'], dict):
            return "Erro: Estrutura do JSON inválida. A chave 'disciplina' deve ser um dicionário."
        if 'codigo' not in result['disciplina'] or not result['disciplina']['codigo']:
            return "Erro: O campo 'codigo' está ausente ou vazio."
        if 'nome' not in result['disciplina'] or not result['disciplina']['nome']:
            return "Erro: O campo 'nome' está ausente ou vazio."
        return result
    except json.JSONDecodeError:
        raise ValueError("Erro: A string fornecida não é um JSON válido.")


def get_informacoes_disciplina(nome_da_discplina: Any) -> list:    
    """
    Buscar as informações específicas de uma disciplina do curso de Ciência da Computação da UFCG.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_discplina: nome da disciplina específica.
    
    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    """
    curso = "ciencia da computacao"
    dados_curso = get_codigo_curso(curso)
    curriculo = get_curriculo_mais_recente(dados_curso['curso']['codigo'])
    disciplina = get_disciplina(nome_disciplina=nome_da_discplina, codigo_curriculo=curriculo['codigo_do_curriculo'])
    print(f"Tool get_disciplina chamada com base_url={base_url}, curriculo={'2023'} nome_da_disciplina={disciplina['disciplina']['nome']}, codigo_da_disciplina={disciplina['disciplina']['codigo']}")
    params = {
        'curso': '14102100',
        'curriculo': "2023",
        'disciplina': disciplina['disciplina']['codigo']
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

