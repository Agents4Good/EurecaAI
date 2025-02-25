from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from .utils.preprocess_text import remove_siglas

import numpy as np
import requests
import json

model = ChatOllama(model="llama3.2:3b", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

format = """{'disciplina': {'codigo': '', 'nome': ''}}"""

def get_disciplinas_curso(codigo_curriculo: str = "2023") -> list:
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
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina_por_codigo(codigo_da_disciplina: str, codigo_curriculo: str):
    """
    Buscar as informações de uma disciplina do curso de Ciência da Computação da UFCG.

    Args:
        codigo_da_disciplina: código numérico em string da disciplina específica.
        codigo_curriculo: código do currículo.
    
    Returns:
        Json com informações relevantes sobre uma disciplica específica.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
        Para usar este método, se 'codigo_da_disciplina' não tiver sido informado pelo usuário, obtenha os parâmetros previamente com a tool `get_disciplinas_por_nome`.
    """

    print(f"Tool get_disciplina chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}, codigo_da_disciplina={codigo_da_disciplina}")
    params = {
        'curso': '14102100',
        'curriculo': codigo_curriculo,
        'disciplina': codigo_da_disciplina
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_disciplinas_por_nome(nome_disciplina: str, codigo_curriculo: str = "2023"): 
    """
    Retorna o código e o nome da disciplina. Caso você precise do código da disciplina para algumo outra ferramenta você deve chamar esta ferramenta.

    Args:
        nome_disciplina: nome da disciplina
        codigo_curriculo: codigo do curriculo, por padrão, é 2023

    Returns:
        dict: Contendo a resposta gerada pelo que contém nome e código da disciplina ou uma mensagem de erro.
    
    Nota:
        Essa função é apenas um auxiliar para obter o código de uma disciplina com base no nome. Se forem desejadas todas as informações de uma disciplna específica, a função a ser chamada deverá ser get_disciplina_por_codigo após obter o código da disciplina.
    """
    nome_disciplina = remove_siglas(nome_disciplina)
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

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?
    
        {possiveis_disciplinas}

        ***OBSERVE SE O NOMES DAS DISCIPLINAS SÃO PRÓXIMOS AO NOME {nome_disciplina}*** 
        
        ***Responda no seguinte formato:***

        **SE OS NOMES FOREM PRÓXIMOS RESPONDA NO FORMATO**
        {format} e ADICIONE O CODIGO E NOME DA DISCIPLINA NOS CAMPOS ADEQUADOS**

        **Se o nome da disciplina for muito distinto de '{nome_disciplina}'*** responda que possivelmente não existe ou o nome está incorreto. (SOMENTE SE OS NOMES FOREM MUITO DIFERENTES)
        
        """   
    )


    return response.content
