import requests
import json

import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .url_config import base_url

def get_cursos_ativos() -> list:
    """
    Buscar todos os cursos ativos da UFCG.

    Args:
    
    Returns:
        Lista de cursos com 'codigo_do_curso' e 'descricao'.
    """
    url_cursos = f'{base_url}/cursos'
    params = {
        'status-enum':'ATIVOS',
        'campus': '1'
    }
    print("chamando a tool get_cursos_ativos.")
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_curso(codigo_do_curso: str) -> list:
    """
    Buscar informação de um curso da UFCG a partir do código do curso.

    Args:
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
    """
    print(f"API_REQUESTS Tool get_curso chamada com codigo_do_curso={codigo_do_curso}.")
    params = {
        'status-enum': 'ATIVOS',
        'curso': codigo_do_curso
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

 
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_curriculos(codigo_do_curso: str) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Se a pergunta for o curriculo mais recente e tiver apenas um curriculo, traga as informações desse único curriculo como resposta.
    """
    print(f"Tool get_curriculos chamada com codigo_do_curso={codigo_do_curso}.")
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_curriculo_mais_recente(codigo_do_curso: str) -> list:
    """
    Buscar o currículo mais recente de um curso.

    Args:
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes do currículo mais recente do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
    """
    print(f"Tool get_curriculo_mais_recente chamada com codigo_do_curso={codigo_do_curso}.")
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)[-1]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_estudantes(codigo_do_curso: str, periodo_de_ingresso: str) -> dict:
    """
    Buscar informações gerais dos estudantes da UFCG com base no curso.

    Args:
        codigo_do_curso: o código do curso.
    
    Returns:
        Dicionário com informações como 'sexo', 'nacionalidades', 'idade' (míninma, máxima, média), 'estados' (siglas), renda_per_capita (quantidade de salário mínimo) e assim por diante.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` para recuperar o código do curso.
    """
    #print(f"Tool get_estudantes chamada com codigo_do_curso={codigo_do_curso}.")
    params = {
        "curso": codigo_do_curso,
        "situacao-do-estudante": "ATIVOS",
    }

    response = requests.get(f'{base_url}/estudantes', params=params)



    if response.status_code == 200:
        #estudantes = json.loads(response.text)

        # info = {
        #     "sexo": {
        #         "feminino": {
        #             "quantidade": 0,
        #             "estado_civil": {},
        #             "nacionalidades": {
        #                 "brasileira": 0,
        #                 "estrangeira": 0
        #             },
        #             "estados": {},
        #             "idade": {
        #                 "idade_minima": None,
        #                 "idade_maxima": None,
        #                 "media_idades": 0
        #             },
        #             "politica_afirmativa": {},
        #             'cor': {},
        #             "renda_per_capita_ate": {
        #                 "renda_minima": None,
        #                 "renda_maxima": None,
        #                 "renda_media": 0
        #             },
        #             "tipo_de_ensino_medio": {}
        #         },
        #         "masculino": {
        #             "quantidade": 0,
        #             "estado_civil": {},
        #             "nacionalidades": {
        #                 "brasileira": 0,
        #                 "estrangeira": 0
        #             },
        #             "estados": {},
        #             "idade": {
        #               "idade_minima": None,
        #               "idade_maxima": None,
        #               "media_idades": 0
        #             },
        #             "politica_afirmativa": {},
        #             'cor': {},
        #             "renda_per_capita_ate": {
        #                 "renda_minima": None,
        #                 "renda_maxima": None,
        #                 "renda_media": 0
        #             },
        #             "tipo_de_ensino_medio": {}
        #         }
        #     },
        # }

        # for estudante in estudantes:
        #     genero = estudante["genero"].lower()
        #     genero_key = "feminino" if genero == "feminino" else "masculino"

        #     genero_data = info["sexo"][genero_key]
        #     genero_data["quantidade"] += 1

        #     # Estado civil
        #     estado_civil = estudante["estado_civil"]
        #     if estado_civil is not None:
        #         genero_data["estado_civil"][estado_civil] = genero_data["estado_civil"].get(estado_civil, 0) + 1

        #     # Atualiza estados
        #     estado = estudante["naturalidade"]
        #     genero_data["estados"][estado] = genero_data["estados"].get(estado, 0) + 1

        #     # Idade mínima, máxima e soma para média
        #     idade = int(estudante["idade"])

        #     if genero_data["idade"]["idade_minima"] is None or idade < genero_data["idade"]["idade_minima"]:
        #         genero_data["idade"]["idade_minima"] = idade
        #     if genero_data["idade"]["idade_maxima"] is None or idade > genero_data["idade"]["idade_maxima"]:
        #         genero_data["idade"]["idade_maxima"] = idade

        #     genero_data["idade"]["media_idades"] = genero_data["idade"].get("media_idades", 0) + idade

        #     # Nacionalidades
        #     nacionalidades = estudante["nacionalidade"].lower()
        #     if "brasileira" in nacionalidades:
        #         genero_data["nacionalidades"]["brasileira"] += 1
        #     else:
        #         genero_data["nacionalidades"]["estrangeira"] += 1

        #     # Tipo de ensino médio
        #     ensino_medio = estudante["tipo_de_ensino_medio"]
        #     if (ensino_medio is not None):
        #         genero_data["tipo_de_ensino_medio"][ensino_medio] = genero_data["tipo_de_ensino_medio"].get(ensino_medio, 0) + 1

        #     # Atualiza renda per capita
        #     renda = estudante["prac_renda_per_capita_ate"]
        #     if genero_data["renda_per_capita_ate"]["renda_minima"] is None or (renda is not None and renda < genero_data["renda_per_capita_ate"]["renda_minima"]):
        #         genero_data["renda_per_capita_ate"]["renda_minima"] = renda
        #     if genero_data["renda_per_capita_ate"]["renda_maxima"] is None or (renda is not None and renda > genero_data["renda_per_capita_ate"]["renda_maxima"]):
        #         genero_data["renda_per_capita_ate"]["renda_maxima"] = renda

        #     if (renda is not None):
        #         genero_data["renda_per_capita_ate"]["renda_media"] += renda
            
        #     # Cor
        #     cor = estudante["cor"]
        #     if cor is not None:
        #         genero_data["cor"][cor] = genero_data["cor"].get(cor, 0) + 1

        #     # Cotas
        #     cota = estudante["politica_afirmativa"]
        #     if cota is not None:
        #         genero_data["politica_afirmativa"][cota] = genero_data["politica_afirmativa"].get(cota, 0) + 1

        # # Calcular médias finais
        # for genero_key in ["feminino", "masculino"]:
        #     genero_data = info["sexo"][genero_key]
        #     quantidade = genero_data["quantidade"]

        #     if quantidade > 0:
        #         # Média de idades
        #         genero_data["idade"]["media_idades"] = round(genero_data["idade"]["media_idades"] / quantidade, 2)

        #         # Média de renda
        #         genero_data["renda_per_capita_ate"]["renda_media"] = round(genero_data["renda_per_capita_ate"]["renda_media"] / quantidade, 2)

        #       # Imprimir resultado final
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_estudantes_formados(codigo_do_curso: str, periodo: str) -> str:
    """
    Buscar a quantidade de estudantes formados (egressos).

    Args:
        codigo_do_curso: código do curso.
        periodo: periodo: período letivo (exemplo: '2024.1', '2023.2', ...)
    
    Returns:
        String com o número de estudantes formados (egressos).
    
    Exemplo:
        "20 formados"
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente `Agente_Campus_Eureca`. 
    """
    #print(f"Tool get_estudantes_formados chamada com codigo_do_curso={codigo_do_curso} e periodo={periodo}.")
    params = {
        "curso": codigo_do_curso,
        "situacao-do-estudante": "EGRESSOS",
        "periodo-de-evasao-de": periodo,
        "periodo-de-evasao-ate": periodo
    }

    response = requests.get(f'{base_url}/estudantes', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    
