
import json

import requests
from strawberry_demo.main import schema
from .default_data.default_cursos_data import *
from langchain.tools import tool
from .url_config import base_url

@tool
def get_cursos_ativos(data: str = default_curso_info):
    """
    Buscar todos os cursos ativos da UFCG. Fornece somente os campos informados.
    """
    try:
        query = f"""
            query {{
                allCursosAtivos {{
                    {data}
                }}
            }}
        """
        print(f"Tool get_cursos_ativos com data {data}")
        result = schema.execute_sync(query)
        return result.data["allCursosAtivos"]

    except Exception as e:
        return e
@tool
def get_curso(codigo_do_curso, data: str = default_curso_info): 
    """
    Buscar informação de um curso da UFCG a partir do código do curso.
    Fornece somente os campos informados.
    """
    try:
        query = f"""
            query {{
                curso(codigoDoCurso: "{codigo_do_curso}") {{
                    {data}
                }}
            }}
        """
        variables = {
            "codigoDoCurso": codigo_do_curso
        }

        print(f"Tool get_curso com os args codigo_do_curso: {codigo_do_curso} e data{data}")
        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curso"]

    except Exception as e:
        return e
@tool
def get_curriculos(codigo_do_curso: str, data: str = default_curriculo_info):
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.
    Fornece somente os campos informados.
    """
    try:
        query = f"""  
            query {{
                curriculos(codigoDoCurso: "{codigo_do_curso}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoDoCurso": codigo_do_curso
        }

        print(f"Tool get_curriculos com o codigo_do_curso {codigo_do_curso} e data {data}")
        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculos"]
    
    except Exception as e:
        return e
    
@tool
def get_curriculo_mais_recente(codigo_do_curso: str, data: str = default_curriculo_info):
    """
    Buscar o currículo mais recente de um curso. Fornece somente os campos informados.
    """
    try:
        query = f"""  
            query {{
                curriculoMaisRecente(codigoDoCurso: "{codigo_do_curso}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoDoCurso": codigo_do_curso
        }

        print(f"Tool get_curriculo_mais_recente com o codigo_do_curso {codigo_do_curso} e data {data}")

        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculoMaisRecente"]
    
    except Exception as e:
        return e
    
@tool    
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

    print(f"Tool get_estudantes com codigo_do_curso={codigo_do_curso}.")
    params = {
        "curso": codigo_do_curso,
        "situacao-do-estudante": "ATIVOS",
    }

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
    
#ver essa tool depois
@tool    
def get_estudantes_formados(codigo_do_curso: str, periodo: str, data: str = default_estudante_info_gerais_parciais):
    """
    Buscar a quantidade de estudantes formados (egressos).
    Fornece somente os campos informados.
    """
    try:
        query = f""" 
            query {{
                estudantesFormados(codigoDoCurso:"{codigo_do_curso}",periodo: "{periodo}") {{
                    {data}
                }}
            }}
        """

        variables = {
            "codigoDoCurso": codigo_do_curso,
            "periodo": periodo
        }

        print(f"Tool get_estudantes_formados com codigo_de_curso {codigo_do_curso}, periodo {periodo} e data {data}")

        result = schema.execute_sync(query, variable_values=variables)
        return len(result.data["estudantesFormados"]) #qtd de estudantes formados

    except Exception as e:
        return e


#DOCUMENTAÇÃO DAS TOOLS
get_cursos_ativos.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_curso_info}
    
    Returns:
        Lista com informações desejadas dos cursos ativos. Por padrão é {default_curso_info}
"""

get_curso.__doc__ = f""" 
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curso_info}
    
    Returns:
        Lista com informações desejadas do curso. Por padrão é {default_curso_info}
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
"""

get_curriculos.__doc__ = f"""  
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curriculo_info}

    Returns:
        Lista com informações desejadas dos currículos. Por padrão é {default_curriculo_info}
"""

get_curriculo_mais_recente.__doc__ = f""" 
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curriculo_info}

    Returns:
        Lista com informações desejadas do currículo mais recente do curso. Por padrão é {default_curriculo_info}
"""

get_estudantes.__doc__ = f""" 
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_estudante_info_gerais_parciais}

    Returns:
        Lista com informações desejadas do currículo mais recente do curso. Por padrão é {default_estudante_info_gerais_parciais}
"""
    
get_estudantes.__doc__ = f""" 

    Args:
        codigo_do_curso: código do curso.
        periodo: periodo: período letivo (exemplo: '2024.1', '2023.2', ...)
        data: campos a serem retornados, por padrão é {default_estudante_info_gerais_parciais}
    
    Returns:
        O número de estudantes formados (egressos).
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente `Agente_Campus_Eureca`. 

"""
