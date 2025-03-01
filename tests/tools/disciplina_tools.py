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

model = ChatOllama(model="llama3.2:3b", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

format = """{'disciplina': {'codigo': '', 'nome': ''}}"""

def get_curriculo(codigo_do_curso, curriculo_do_curso):
    curriculos = get_curriculos(codigo_do_curso=codigo_do_curso)
    
    existe_curriculo = False
    todos_curriculos_disponiveis = []
        
    for curriculo_dict_i in curriculos:
        curriculo_i = curriculo_dict_i['codigo_do_curriculo']
        todos_curriculos_disponiveis.append(curriculo_i)
        if curriculo_i == int(curriculo_do_curso):
            existe_curriculo = True

def get_todas_disciplinas_curso(nome_do_curso: Any, codigo_curriculo: Any):
    """
    Busca todas as discplinas de um curso.

    Args:
        nome_do_curso: nome do curso
        codigo_curriculo: valor inteiro do ano.
        
    Returns:
        Retorna uma lista de disciplinas ofertadas pelo curso.
    """
    
    curso = get_codigo_curso(nome_do_curso=str(nome_do_curso))
    
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}.")

    params = {
        'curso': curso['curso']['codigo'],
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

        
    

def get_disciplinas_curso(codigo_do_curso: Any, codigo_curriculo: Any) -> list:
    """
    Buscar todas as disciplinas de um curso.

    Args:
        codigo_do_curso: codigo do curso.
        codigo_curriculo: valor inteiro do ano.

    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    """
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}.")
    params = {
        'curso': str(codigo_do_curso),
        'curriculo': str(codigo_curriculo)
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_disciplina(codigo_do_curso: Any, nome_disciplina: Any, codigo_curriculo: Any = "") -> dict:
    """
    Buscar o nome e o código de uma disciplina.

    Args:
        nome_disciplina: nome da disciplina.
        codigo_curriculo: valor inteiro do ano.

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """
    
    nome_disciplina = remove_siglas(str(nome_disciplina))
    disciplinas = get_disciplinas_curso(str(codigo_do_curso), codigo_curriculo=str(codigo_curriculo))

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


def get_informacoes_disciplina(nome_da_discplina: Any, nome_do_curso: Any, curriculo: Any = "") -> list:    
    """
    Buscar as informações específicas de uma disciplina do curso.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_discplina: nome da disciplina específica.
        nome_do_curso: nome do curso.
        curriculo: valor inteiro do ano.

    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    """
    nome_do_curso = str(nome_do_curso)
    dados_curso = get_codigo_curso(nome_do_curso)
    codigo_do_curso = dados_curso['curso']['codigo']

    if (str(curriculo) == ""):
        curriculo = get_curriculo_mais_recente(codigo_do_curso)
        codigo_do_curriculo = curriculo['codigo_do_curriculo']
    else:
        curriculos = get_curriculos(codigo_do_curso=codigo_do_curso)
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{
            "error_status": "500",
            "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis}" 
            }]
            
        codigo_do_curriculo = curriculo
        
    try:
        disciplina = get_disciplina(codigo_do_curso=codigo_do_curso, nome_disciplina=nome_da_discplina, codigo_curriculo=codigo_do_curriculo)
    except Exception as e:
        return [{"error_status": response.status_code, "msg": str(e)}]

    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': codigo_do_curriculo,
        'disciplina': disciplina['disciplina']['codigo']
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
















def get_disciplinas_grade_curso(codigo_do_curso: Any, codigo_curriculo: Any) -> list:
    """
    Buscar todas as disciplinas do curso que estão na grade do curso.

    Args:
        codigo_do_curso: codigo do curso.
        codigo_curriculo: valor inteiro do ano.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Se você não souber, o código do curriculo, passe a string vazia.
    """
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, curso={str(codigo_do_curso)} codigo_curriculo={codigo_curriculo}.")
    params = {
        'curso': str(codigo_do_curso),
        'curriculo': str(codigo_curriculo)
    }

    response = requests.get(f'{base_url}/disciplinas-por-curriculo', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina_curriculo(codigo_do_curso: Any, curriculo: Any, codigo_da_disciplina: Any):
    params = {
        'curso': str(codigo_do_curso),
        'curriculo': str(curriculo),
        'disciplina': str(codigo_da_disciplina)
    }

    response = requests.get(f'{base_url}/disciplinas-por-curriculo?', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    

def get_disciplina_grade_curso(codigo_do_curso: Any, nome_disciplina: Any, codigo_curriculo: Any) -> dict:
    """
    Buscar o nome e o código de uma disciplina da grade do curso.

    Args:
        codigo_do_curso: codigo do curso.
        nome_disciplina: nome da disciplina.
        codigo_curriculo: valor inteiro do ano.

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """
    
    print(nome_disciplina, codigo_curriculo, "recebido")
    nome_disciplina = remove_siglas(str(nome_disciplina))
    disciplinas = get_disciplinas_grade_curso(codigo_do_curso=codigo_do_curso, codigo_curriculo=codigo_curriculo)

    sentences = [disciplina["nome"] for disciplina in disciplinas]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(nome_disciplina).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    top_5_disciplinas = [{
        "codigo": disciplinas[idx]["codigo_da_disciplina"], 
        "nome": disciplinas[idx]["nome"], 
        "similaridade": similarities[idx]} for idx in top_5_indices
    ]

    print("TOP 5 ", top_5_disciplinas)

    possiveis_disciplinas = []
    for disciplina in top_5_disciplinas:
        if disciplina['similaridade'] >= 0.65:
            possiveis_disciplinas.append(f"{disciplina['codigo']} - {disciplina['nome']}")

    if len(possiveis_disciplinas) == 0:
        raise Exception("Caro agente, informe que a disciplina é inválida e mande o usuário informar o nome correto (nome completo dela)")

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


def get_informacoes_disciplina_grade_curso(nome_da_discplina: Any, nome_do_curso: Any, curriculo: Any = "") -> list:    
    """
    Buscar as informações de uma disciplina da grade do curso.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_discplina: nome da disciplina.
        nome_do_curso: nome do curso.
        curriculo: valor inteiro do ano.
    
    Returns:
        Lista com informações relevantes sobre apenas uma disciplica da grade do curso.
    """
    nome_do_curso = str(nome_do_curso)
    dados_curso = get_codigo_curso(nome_do_curso)
    codigo_do_curso = dados_curso['curso']['codigo']
    
    if (str(curriculo) == ""):
        curriculo = get_curriculo_mais_recente(codigo_do_curso)
        codigo_do_curriculo = curriculo['codigo_do_curriculo']
    else:
        curriculos = get_curriculos(codigo_do_curso=codigo_do_curso)
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{
                "error_status": "500",
                "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis}" 
            }]
            
        codigo_do_curriculo = curriculo
        
    try:
        disciplina = get_disciplina_grade_curso(codigo_do_curso, nome_da_discplina, codigo_curriculo=codigo_do_curriculo)
    except Exception as e:
        return [{"error_status": response.status_code, "msg": str(e)}]
        
    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': codigo_do_curriculo,
        'disciplina': disciplina['disciplina']['codigo']
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        disciplina_json = json.loads(response.text)
        disciplina_curriculo = get_disciplina_curriculo(dados_curso["curso"]["codigo"], codigo_do_curriculo, disciplina['disciplina']['codigo'])
        disciplina_json[0]["tipo"] = f"Disciplina {disciplina_curriculo[0]['tipo']}"
        disciplina_json[0]["semestre_ideal"] = f"Disciplina do {disciplina_curriculo[0]['semestre_ideal']} período"
        return disciplina_json

    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
