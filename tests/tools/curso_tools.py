from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from .utils.preprocess_text import remove_siglas
from typing import Any
from .campus_tools import * 

import numpy as np
import requests
import json, unicodedata

model = ChatOllama(model="llama3.1", temperature=0)
model_sentence = SentenceTransformer("all-MiniLM-L6-v2")

format = """{'curso': {'codigo': '', 'nome': ''}}"""
base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"

def get_cursos(nome_do_campus: Any = "") -> list:
    """
    Busca por todos os cursos da UFCG por campus.

    Args:
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''. 
    
    Returns:
        Lista de cursos com 'codigo_do_curso' e 'nome'.
    """
    
    print(f"Tool get_cursos chamada com nome_do_campus={nome_do_campus}")
    
    campus = get_campus_most_similar(str(nome_do_campus))
    
    url_cursos = f'{base_url}/cursos'
    params = {
        'status-enum':'ATIVOS',
        'campus': campus["campus"]["codigo"]
    }
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'nome': data['descricao']} for data in data_json]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def processar_json(json_str: str):
    try:
        result = json.loads(json_str.replace("'", '"'))

        if 'curso' not in result or not isinstance(result['curso'], dict):
            return "Erro: Estrutura do JSON inválida. A chave 'curso' deve ser um dicionário."
        if 'codigo' not in result['curso'] or not result['curso']['codigo']:
            return "Erro: O campo 'codigo' está ausente ou vazio."
        '''if 'nome' not in result['curso'] or not result['curso']['nome']:
            return "Erro: O campo 'nome' está ausente ou vazio."'''
        return result
    except json.JSONDecodeError:
        raise ValueError("Erro: A string fornecida não é um JSON válido.")


def get_codigo_curso(nome_do_curso: Any, nome_do_campus: Any) -> dict:
    """
    Busca o código do curso pelo nome dele.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        dict: dicionário contendo código do curso e nome do curso.
    """
    
    print(f"Tool get_codigo_curso chamada com nome_do_curso {nome_do_curso} e nome_do_campus={nome_do_campus}")
    
    #nome_curso = remove_siglas(nome_do_curso)
    cursos = get_cursos(nome_do_campus=str(nome_do_campus))

    sentences = [curso["nome"] for curso in cursos]
    embeddings = model_sentence.encode(sentences)
    embedding_query = model_sentence.encode(str(nome_do_curso)).reshape(1, -1)

    similarities = cosine_similarity(embeddings, embedding_query).flatten()
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    top_5_cursos = [{"codigo_do_curso": cursos[idx]["codigo_do_curso"], "descricao": cursos[idx]["nome"], "similaridade": similarities[idx]} for idx in top_5_indices]

    #print(top_5_cursos)
    possiveis_cursos = []
    for curso in top_5_cursos:
        if curso['similaridade'] >= 0.65:
            possiveis_cursos.append(f"{curso['codigo_do_curso']} - {curso['descricao']}")
    
    def remover_acentos(texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    lista_tratada = [remover_acentos(item) for item in possiveis_cursos]
    
    if len(lista_tratada) == 0:
        return {"AskHuman": "Não foi encontrado um curso com o nome o informado", "choice": top_5_cursos}
        
    response = model.invoke(
        f"""
        Para o curso de nome: '{nome_do_curso}', quais desses possíveis cursos abaixo é mais similar ao curso do nome informado?
        
        {lista_tratada}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        
        Antes de responder por definitivo, considere essas observações abaixo:

        M significa que é um curso matutino;
        D significa que é um curso diurno;
        N significa que é um curso noturno.
        """
    )
    #print({"messages": [response]})
    result = processar_json(response.content)
    return result


def get_informacoes_curso(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar informação de um curso da UFCG a partir do nome do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
    
    Returns:
        Lista com informações relevantes do curso específico, como código do inep, código e nome do setor desse curso, período de início, etc.
    """
    
    print(f"Tool get_informacoes_curso chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    curso = get_codigo_curso(remove_siglas(nome_do_curso), str(nome_do_campus))

    params = {
        'status-enum': 'ATIVOS',
        'curso': curso['curso']['codigo']
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_curriculo_mais_recente(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar o currículo mais recente de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
    
    Returns:
        Lista com informações relevantes do currículo mais recente do curso específico.
    """
    
    print(f"Tool get_curriculo_mais_recente chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    
    curso = get_codigo_curso(remove_siglas(nome_do_curso), str(nome_do_campus))
    response = requests.get(f'{base_url}/curriculos?curso={curso["curso"]["codigo"]}')
    
    if response.status_code == 200:
        return json.loads(response.text)[-1]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_estudantes(nome_do_curso: Any = "", nome_do_campus: Any = "") -> dict:
    """
    Buscar informações gerais dos estudantes da UFCG com base no curso.

    Args:
        nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''. 
    
    Returns:
        Dicionário com informações como 'sexo', 'nacionalidades', 'idade' (míninma, máxima, média), 'estados' (siglas), renda_per_capita (quantidade de salário mínimo) e assim por diante.
    """

    print(f"Tool get_estudantes chamada com nome_do_curso={nome_do_curso} e nome_do_cmapus={nome_do_campus}.")    
    curso = get_codigo_curso(remove_siglas(nome_do_curso), nome_do_campus=str(nome_do_campus))
    
    params = {
        "situacao-do-estudante": "ATIVOS"
    }
    
    if (str(nome_do_curso) != "" and str(nome_do_campus != "")):
        curso = get_codigo_curso(remove_siglas(nome_do_curso), nome_do_campus=str(nome_do_campus))
        params["curso"] = curso['curso']['codigo']
    elif (str(nome_do_curso) == "" and str(nome_do_campus != "")):
        campus = get_campus_most_similar(campus=str(nome_do_campus))
        params["campus"] = campus['campus']['codigo']
    elif (str(nome_do_curso) != "" and str(nome_do_campus == "")):
        return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]

    response = requests.get(f'{base_url}/estudantes', params=params)

    if response.status_code == 200:
        estudantes = json.loads(response.text)

        info = {
            "sexo": {
                "feminino": {
                    "quantidade": 0,
                    "estado_civil": {},
                    "nacionalidades": {
                        "brasileira": 0,
                        "estrangeira": 0
                    },
                    "estados": {},
                    "idade": {
                        "idade_minima": None,
                        "idade_maxima": None,
                        "media_idades": 0
                    },
                    "politica_afirmativa": {},
                    'cor': {},
                    "renda_per_capita_ate": {
                        "renda_minima": None,
                        "renda_maxima": None,
                        "renda_media": 0
                    },
                    "tipo_de_ensino_medio": {}
                },
                "masculino": {
                    "quantidade": 0,
                    "estado_civil": {},
                    "nacionalidades": {
                        "brasileira": 0,
                        "estrangeira": 0
                    },
                    "estados": {},
                    "idade": {
                      "idade_minima": None,
                      "idade_maxima": None,
                      "media_idades": 0
                    },
                    "politica_afirmativa": {},
                    'cor': {},
                    "renda_per_capita_ate": {
                        "renda_minima": None,
                        "renda_maxima": None,
                        "renda_media": 0
                    },
                    "tipo_de_ensino_medio": {}
                }
            },
        }

        for estudante in estudantes:
            genero = estudante["genero"].lower()
            genero_key = "feminino" if genero == "feminino" else "masculino"

            genero_data = info["sexo"][genero_key]
            genero_data["quantidade"] += 1

            # Estado civil
            estado_civil = estudante["estado_civil"]
            if estado_civil is not None:
                genero_data["estado_civil"][estado_civil] = genero_data["estado_civil"].get(estado_civil, 0) + 1

            # Atualiza estados
            estado = estudante["naturalidade"]
            genero_data["estados"][estado] = genero_data["estados"].get(estado, 0) + 1

            # Idade mínima, máxima e soma para média
            idade = int(estudante["idade"])

            if genero_data["idade"]["idade_minima"] is None or idade < genero_data["idade"]["idade_minima"]:
                genero_data["idade"]["idade_minima"] = idade
            if genero_data["idade"]["idade_maxima"] is None or idade > genero_data["idade"]["idade_maxima"]:
                genero_data["idade"]["idade_maxima"] = idade

            genero_data["idade"]["media_idades"] = genero_data["idade"].get("media_idades", 0) + idade

            # Nacionalidades
            nacionalidades = estudante["nacionalidade"].lower()
            if "brasileira" in nacionalidades:
                genero_data["nacionalidades"]["brasileira"] += 1
            else:
                genero_data["nacionalidades"]["estrangeira"] += 1

            # Tipo de ensino médio
            ensino_medio = estudante["tipo_de_ensino_medio"]
            if (ensino_medio is not None):
                genero_data["tipo_de_ensino_medio"][ensino_medio] = genero_data["tipo_de_ensino_medio"].get(ensino_medio, 0) + 1

            # Atualiza renda per capita
            renda = estudante["prac_renda_per_capita_ate"]
            if genero_data["renda_per_capita_ate"]["renda_minima"] is None or (renda is not None and renda < genero_data["renda_per_capita_ate"]["renda_minima"]):
                genero_data["renda_per_capita_ate"]["renda_minima"] = renda
            if genero_data["renda_per_capita_ate"]["renda_maxima"] is None or (renda is not None and renda > genero_data["renda_per_capita_ate"]["renda_maxima"]):
                genero_data["renda_per_capita_ate"]["renda_maxima"] = renda

            if (renda is not None):
                genero_data["renda_per_capita_ate"]["renda_media"] += renda
            
            # Cor
            cor = estudante["cor"]
            if cor is not None:
                genero_data["cor"][cor] = genero_data["cor"].get(cor, 0) + 1

            # Cotas
            cota = estudante["politica_afirmativa"]
            if cota is not None:
                genero_data["politica_afirmativa"][cota] = genero_data["politica_afirmativa"].get(cota, 0) + 1

        # Calcular médias finais
        for genero_key in ["feminino", "masculino"]:
            genero_data = info["sexo"][genero_key]
            quantidade = genero_data["quantidade"]

            if quantidade > 0:
                # Média de idades
                genero_data["idade"]["media_idades"] = round(genero_data["idade"]["media_idades"] / quantidade, 2)

                # Média de renda
                genero_data["renda_per_capita_ate"]["renda_media"] = round(genero_data["renda_per_capita_ate"]["renda_media"] / quantidade, 2)

              # Imprimir resultado final
        return info
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_curriculos(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        
    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    """
    
    print(f"Tool get_curriculos chamada com nome_do_curso={str(nome_do_curso)} e nome_do_campus={nome_do_campus}.")
    
    curso = get_codigo_curso(remove_siglas(nome_do_curso), str(nome_do_campus))
    response = requests.get(f'{base_url}/curriculos?curso={str(curso["curso"]["codigo"])}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]