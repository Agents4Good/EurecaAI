
from strawberry_demo.main import schema
from .default_data import *


def get_cursos_ativos(data: str = default_curso_info):
    """
    Buscar todos os cursos ativos da UFCG.
    """
    try:
        query = f"""
            query {{
                allCursosAtivos {{
                    {data}
                }}
            }}
        """
        print(f"CHAMEIII Tool get_cursos_ativos com os args {data}")
        result = schema.execute_sync(query)
        return result.data["allCursosAtivos"]

    except Exception as e:
        return e

def get_curso(codigo_do_curso, data: str = default_curso_info): 
    """
    Buscar informação de um curso da UFCG a partir do código do curso.
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

        print(f"Tool get_curso com os args codigo_do_curso: {codigo_do_curso} e {data}")
        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curso"]

    except Exception as e:
        return e

def get_curriculos(codigo_do_curso: str, data: str = default_curriculo_info):
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.
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
        #print(f"Tool get_curriculos com o codigo_do_curso {codigo_do_curso} e {data}")
        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculos"]
    
    except Exception as e:
        return e
    

def get_curriculo_mais_recente(codigo_do_curso: str, data: str = default_curriculo_info):
    """
    Buscar o currículo mais recente de um curso.
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

        #print(f"Tool get_curriculo_mais_recente com o codigo_do_curso {codigo_do_curso} e {data}")

        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculoMaisRecente"]
    
    except Exception as e:
        return e
    
def get_estudantes(codigo_do_curso: str, periodo_de_ingresso: str, data: str = default_estudante_info_gerais_parciais):
    """
    Buscar informações gerais dos estudantes da UFCG com base no curso.
    """

    try:
        query = f"""  
            query {{
                estudantesGeraisPorCurso(codigoDoCurso: "{codigo_do_curso}", periodoDeIngresso: "{periodo_de_ingresso}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoDoCurso": codigo_do_curso,
            "periodoDeIngresso": periodo_de_ingresso
        }

        #print(f"Tool get_estudantes com args {data}")

        result = schema.execute_sync(query, variable_values=variables)
        return result.data["estudantesGeraisPorCurso"]
    
    except Exception as e:
        return e
    
def get_estudantes_formados(codigo_do_curso: str, periodo: str, data: str = default_estudante_info_gerais_parciais):
    """
    Buscar a quantidade de estudantes formados (egressos).
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
