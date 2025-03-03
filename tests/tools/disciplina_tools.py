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


# Tool Call
def get_todas_disciplinas_curso(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = ""):
    """
    Busca todas as discplinas de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Retorna uma lista de disciplinas ofertadas pelo curso.
    """
    
    if (str(curriculo) == ""):
        codigo_curriculo = get_curriculo_mais_recente(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)

    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={codigo_curriculo}.")
    curso = get_codigo_curso(nome_do_curso=str(nome_do_curso), nome_do_campus=nome_do_campus)
    
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


def get_disciplinas_curso_por_codigo(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any) -> list:
    """
    Buscar todas as disciplinas de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    """
    
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e curriculo={curriculo}.")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': str(curriculo)
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina(nome_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> dict:
    """
    Buscar o nome e o código de uma disciplina.

    Args:
        nome_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """
    
    print(f"Tool get_disciplina chamada com nome_da_disciplina={nome_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e curriculo={curriculo}")
    
    nome_disciplina = remove_siglas(str(nome_disciplina)).lower()
    dados_curso = get_codigo_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
    disciplinas = get_disciplinas_curso_por_codigo(dados_curso["curso"]["codigo"], codigo_curriculo=str(curriculo))

    sentences = [disciplina["nome"].lower() for disciplina in disciplinas]
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


def get_informacoes_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:    
    """
    Buscar as informações específicas de uma disciplina do curso.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_disciplina: nome da disciplina específica.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    """
    
    print(f"Tool get_informacoes_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}")    
    
    nome_do_curso = str(nome_do_curso)
    dados_curso = get_codigo_curso(nome_do_curso, nome_do_campus=nome_do_campus)
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
        disciplina = get_disciplina(codigo_do_curso=codigo_do_curso, nome_disciplina=nome_da_disciplina, codigo_curriculo=codigo_do_curriculo)
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


def get_disciplinas_grade_curso(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """
    Buscar todas as disciplinas do curso que estão na grade do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    """
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso} e curriculo={curriculo}.")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    if (str(curriculo) == ""):
        curriculo = get_curriculo_mais_recente()
    
    params = {
        'curso': dados_curso["curso"]["codigo"],
        'curriculo': str(curriculo)
    }

    response = requests.get(f'{base_url}/disciplinas-por-curriculo', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


## ---------------------------------------------------------------
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


# Tool Call
def get_informacoes_disciplina_grade_curso(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:    
    """
    Buscar as informações de uma disciplina da grade do curso.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista com informações relevantes sobre apenas uma disciplica da grade do curso.
    """
    
    print(f"Tool get_informacoes_disciplina_grade_curso chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e curriculo={curriculo}")
    
    nome_do_curso = str(nome_do_curso)
    dados_curso = get_codigo_curso(nome_do_curso, nome_do_campus=nome_do_campus)
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
        disciplina = get_disciplina_grade_curso(codigo_do_curso, nome_da_disciplina, codigo_curriculo=codigo_do_curriculo)
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


def get_todos_curriculos(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    """
    
    print(f"Tool get_curriculos chamada com nome_do_curso={nome_do_curso}.")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    response = requests.get(f'{base_url}/curriculos?curso={str(dados_curso["curso"]["codigo"])}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_curriculos(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = ""): 
    """
    Busca os curriculos disponiveis de um curso.
     
    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Retorna o(s) curriculo(s) de um curso.
    """
    
    print(nome_do_curso, nome_do_campus, curriculo)
    
    curriculos = get_todos_curriculos(codigo_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    existe_curriculo = False
    todos_curriculos_disponiveis = []
        
    for curriculo_dict_i in curriculos:
        curriculo_i = curriculo_dict_i['codigo_do_curriculo']
        todos_curriculos_disponiveis.append(curriculo_i)
        if str(curriculo_i) == str(curriculo):
            existe_curriculo = True
    
    if (str(curriculo) == "" and existe_curriculo):
        return [curriculo]
    
    return todos_curriculos_disponiveis


def get_periodo_mais_recente() -> str:
    """
    Buscar o período mais recente da universidade.
        
    Returns:
        String com o período mais recente.
    """
    params = {
        'campus': '1'
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)[-1]['periodo']
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


# Tool Call
def get_plano_de_curso(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, curriculo: Any = "", periodo: Any = "") -> list:
    """
    Busca o plano de curso de uma disciplina.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
        periodo: periodo.
    
    Returns:
        Lista com informações relevantes do plano de curso de uma disciplina.
    """
    
    print(f"Tool get_plano_de_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, curriculo={curriculo} e periodo={periodo}")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    print(dados_curso)
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=str(nome_da_disciplina), codigo_curriculo=str(curriculo))
    print(disciplina)
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        'disciplina': disciplina['disciplina']['codigo'],
        'periodo-de': periodo,
        'periodo-ate': periodo
    }
    response = requests.get(f'{base_url}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{
            "error_status": response.status_code, 
            "msg": f"Não foi possível obter informação da disciplina de {nome_da_disciplina} por não existir para esse período ou por ser chamada de outro nome."
        }]


# Tool Call
def get_turmas(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, periodo: Any = "", curriculo: Any = "") -> list:
    """
    Busca todas as turmas de uma disciplina.
    
    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        periodo: período (se não souber não coloque nada aqui para obter o período mais recente).
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista com informações relevantes das turmas.
    """
    
    print(f"Tool get_turmas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, periodo={periodo} e codigo_curriculo={curriculo}")
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=nome_da_disciplina, codigo_curriculo=curriculo)

    params = {
        "periodo-de": str(periodo),
        "periodo-ate": str(periodo),
        "disciplina": disciplina["disciplina"]["codigo"]
    }
    
    response = requests.get(f'{base_url}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da disciplina porque a disciplina não existe para esse período."}]


# Tool Call
def get_plano_de_aulas(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, periodo: Any = "", numero_da_turma: Any = "", curriculo: Any = "") -> list:
    """
    Buscar plano de aulas de uma turma de uma disciplina. 
    Use quando quiser buscar informação do tema abordado na aula em um dia específico. 
    Essa ferramenta lhe dará uma lista de temas das aulas que irá ocorrer em cada dia.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        periodo: período letivo (passe a string vazia se não souber).
        numero_da_turma: valor numérico da turma (se não souber, use a turma '01' como turma padrão).
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    
    Nota:
        Se não souber o periodo, passe a string vazia "".
        Se não souber o curriculo, passe a string vazia "".
    """
    print(f"Tool get_plano_de_aulas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, periodo={periodo}, numero_turma={numero_da_turma} e curriculo={curriculo}.")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=str(nome_da_disciplina), codigo_curriculo=str(curriculo))
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()
        
    print(disciplina["disciplina"]["codigo"], periodo, numero_da_turma)
    
    params = {
        'disciplina': disciplina["disciplina"]["codigo"],
        'periodo-de': str(periodo),
        'periodo-ate': str(periodo),
        'turma': str(numero_da_turma)
    }

    response = requests.get(f'{base_url}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina_for_tool(codigo_da_disciplina):
    params = {
        'disciplina': codigo_da_disciplina
    }
    
    response = requests.get(f'{base_url}/disciplinas', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


# Tool Call
def pre_requisitos_disciplinas(nome_da_disciplina:Any, nome_do_curso:Any, nome_do_campus: Any, curriculo: Any = "") -> dict:
    """
    Busca as disciplinas que são pré-requisitos ou requisitos da disciplina perhguntada.
    
    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista contentdo o nome de cada disciplina que é requisito para a disciplina desejada. 
        Se o retorno for uma lista vazia, então informe que a disciplina em questão não possui requisitos.
    """
    
    print(f"Tool pre_requisitos_disciplinas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=str(nome_da_disciplina), codigo_curriculo=str(curriculo))

    print("disciplina", disciplina)
    curriculo = get_curriculos(dados_curso["curso"]["codigo"], curriculo)[-1]

    print("curriculo", curriculo)
    params = {
        'disciplina': disciplina["disciplina"]["codigo"],
        'curriculo': curriculo
    }

    response = requests.get(f'{base_url}/pre-requisito-disciplinas', params=params)

    if response.status_code == 200:
        requisitos = json.loads(response.text)
        disciplinas = []

        for requisito in requisitos:
            disciplina_req = get_disciplina_for_tool(
                requisito['condicao'],
            )

            disciplinas.append(disciplina_req[0]['nome'])

        return list(set(disciplinas))
    else:
        [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


# Tool Call
def get_horarios_disciplinas(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, turma: Any, periodo: Any = "", curriculo: Any = ""):
    """
    Busca os horários e a sala de uma disciplina de uma turma especificada (caso não seja, busca de todas as turmas).

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        turma: número da turma (se não souber usar o valor '01').
        periodo: período do curso (se não souber, então use a string vazia '').
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Retorna uma lista de horários das aulas da disciplina.
    """
    
    print(f"Tool get_horarios_disciplinas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, turma={turma} e curriculo={curriculo}")
    
    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    curriculo = get_curriculos(dados_curso["curso"]["codigo"], curriculo=curriculo)[-1]
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=str(nome_da_disciplina), codigo_curriculo=str(curriculo))
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()

    params = {
        "disciplina": disciplina["disciplina"]["codigo"],
        "turma": str(turma),
        "periodo-de": periodo,
        "periodo-ate": periodo
    }

    response = requests.get(f'{base_url}/horarios', params=params)

    if response.status_code == 200:
        horarios = json.loads(response.text)
            
        filtros_horarios = []
        turmas_map = {}

        for horario in horarios:
            turma = horario['turma']
            sala = horario['codigo_da_sala']
            dia = str(horario['dia'])
            horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

            if turma not in turmas_map:
                turmas_map[turma] = {
                    'turma': turma,
                    'sala': sala,
                    'horarios': {}
                }
                filtros_horarios.append(turmas_map[turma])

            turmas_map[turma]['horarios'][dia] = horario_formatado

        return filtros_horarios
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


# Tool Call
def get_media_notas_turma_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "", curriculo: Any = "") -> dict:
    """
    Busca as notas/desempenho dos estudantes em uma turma de uma disciplina.

    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Se o usuário não informou o campus de Campina Grande)
        turma: valor numérico da turma da disciplina (se não foi informada, então passe a strig vazia '').
        periodo: periodo do curso (se não foi informado, então passe a string vazia '').
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Dicionário com o intervalo das médias das notas de dada disciplina de uma turma.
    """
    
    print(f"Tool get_media_notas_turma_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")

    dados_curso = get_codigo_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    curriculo = get_curriculos(dados_curso["curso"]["codigo"], curriculo=curriculo)[-1]
    disciplina = get_disciplina(dados_curso["curso"]["codigo"], nome_disciplina=str(nome_da_disciplina), codigo_curriculo=str(curriculo))
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()

    params = {
        "periodo-de": str(periodo),
        "periodo-ate": str(periodo),
        "disciplina": disciplina["disciplina"]["codigo"],
        "turma": turma
    }

    response = requests.get(f'{base_url}/matriculas', params=params)

    if response.status_code == 200:
        matriculas = json.loads(response.text)
        
        medias = [
            matricula["media_final"] 
            if matricula["media_final"] is not None else 0
            for matricula in matriculas
        ]
        return {
            "medias_menores_que_5": 
            len([media for media in medias if float(media) < 5]),
            "medias_maior_ou_igual_a_5.0_e_menor_que_7.0": 
            len([media for media in medias if float(media) >= 5 and float(media) < 7]),
            "medias_maior_ou_igual_a_7.0_e_menor_que_8.5": 
            len([media for media in medias if float(media) >= 7 and float(media) < 8.5]),
            "medias_maior_ou_igual_a_8.5_e_menor_ou_igual_a_10": 
            len([media for media in medias if float(media) >= 8.5 and float(media) <= 10])
        }
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
