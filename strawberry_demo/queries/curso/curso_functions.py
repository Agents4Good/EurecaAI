
from strawberry_demo.main import schema
from .default_data import *


def get_cursos_ativos(data: str = default_curso):
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
        print(f"Tool get_cursos_ativos com os args {data}")
        result = schema.execute_sync(query)
        return result.data["allCursosAtivos"]

    except Exception as e:
        return e

def get_curso(codigo_do_curso, data: str = default_curso): 
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

def get_curriculos(codigo_do_curso: str, data: str = default_curriculo):
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
        print(f"Tool get_curriculos com o codigo_do_curso {codigo_do_curso} e {data}")
        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculos"]
    
    except Exception as e:
        return e
    

def get_curriculo_mais_recente(codigo_do_curso: str, data: str = default_curriculo):
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

        print(f"Tool get_curriculo_mais_recente com o codigo_do_curso {codigo_do_curso} e {data}")

        result = schema.execute_sync(query, variable_values=variables)
        return result.data["curriculoMaisRecente"]
    
    except Exception as e:
        return e
    
def get_estudantes(codigo_do_curso: str):
    pass


#DOCUMENTAÇÃO DAS TOOLS
get_cursos_ativos.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_curso}
    
    Returns:
        Lista com informações desejadas dos cursos ativos. Por padrão é {default_curso}
"""

get_curso.__doc__ = f""" 
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curso}
    
    Returns:
        Lista com informações desejadas do curso. Por padrão é {default_curso}
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
"""

get_curriculos.__doc__ = f"""  
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curriculo}

    Returns:
        Lista com informações desejadas dos currículos. Por padrão é {default_curriculo}
"""

get_curriculo_mais_recente.__doc__ = f""" 
    Args:
        codigo_do_curso: código do curso.
        data: campos a serem retornados, por padrão é {default_curriculo}

    Returns:
        Lista com informações desejadas do currículo mais recente do curso. Por padrão é {default_curriculo}
"""
    
