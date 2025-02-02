from .default_data import *
from strawberry_demo.main import schema

def get_disciplina_curso(codigo_curriculo: str, data: str = default_disciplina):
    """
    Buscar todas as disciplinas do curso de Ciência da Computação da UFCG.
    """
    try:
        query = f"""  
            query {{
                disciplinaPorCursoCurriculo(codigoCurriculo: "{codigo_curriculo}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoCurriculo": codigo_curriculo
        }

        result = schema.execute_sync(query,variables)
        return result.data["disciplinaPorCursoCurriculo"]
    
    except Exception as e:
        return e

def get_disciplina(codigo_da_disciplina: str, codigo_curriculo: str, data: str = default_disciplina):
    """
    Buscar as informações desejadas de uma disciplina do curso de Ciência da Computação da UFCG.
    """
    try:
        query = f"""  
            query {{
                disciplinaPorCodigoCurriculo(codigoDaDisciplina: "{codigo_da_disciplina}",codigoCurriculo: "{codigo_curriculo}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoDaDisciplina": codigo_da_disciplina,
            "codigoCurriculo": codigo_curriculo
        }

        result = schema.execute_sync(query,variables)
        return result.data["disciplinaPorCodigoCurriculo"]
    
    except Exception as e:
        return e
    

def get_plano_de_curso(codigo_disciplina: str, periodo: str, data: str = default_plano_de_curso):
    """
        Plano de curso de uma disciplina (do curso de Ciência da Computação).
    """
    try:
        query = f"""  
            query {{
                planoDeCursoPorDisciplinaPeriodo(codigoDisciplina: "{codigo_disciplina}",periodo: "{periodo}") {{
                    {data}
                }}   
            }}

        """
        variables = {
            "codigoDaDisciplina": codigo_disciplina,
            "periodo": periodo
        }

        result = schema.execute_sync(query,variables)
        return result.data["planoDeCursoPorDisciplinaPeriodo"]
    
    except Exception as e:
        return e
    

def get_plano_de_aulas(codigo_disciplina: str, periodo: str, turma: str, data: str = default_aula):
    """
    Buscar plano de aulas de uma turma de uma disciplina.
    """
    try:
        query = f"""  
            query {{
                planoDeAula(codigoDisciplina: "{codigo_disciplina}",periodo: "{periodo}", turma:"{turma}") {{
                    {data}
                }}   
            }}
        """
        variables = {
            "codigoDaDisciplina": codigo_disciplina,
            "periodo": periodo,
            "turma": turma
        }

        result = schema.execute_sync(query,variables)
        return result.data["planoDeAula"]
    
    except Exception as e:
        return e


def get_turmas(periodo: str, codigo_disciplina: str, data: str = default_turma):
    """
        Buscar turmas.
    """
    try:
        query = f"""  
            query {{
                Turma(codigoDisciplina: "{codigo_disciplina}",periodo: "{periodo}") {{
                    {data}
                }}   
            }}
        """
        variables = {
            "codigoDaDisciplina": codigo_disciplina,
            "periodo": periodo,
        }

        result = schema.execute_sync(query,variables)
        return result.data["Turma"]
    
    except Exception as e:
        return e
    
#get_media_notas_turma_disciplina não pode ser mudado

def get_horarios_disciplinas(codigo_disciplina:str, turma:str, periodo:str, data: str = default_horario_disciplina):
    """
    Buscar os horários e a sala de uma disciplina de uma turma especificada (caso não seja, busca de todas as turmas).
    """
    try:
        query = f"""  
            query {{
                horarioDisciplinas(codigoDisciplina: "{codigo_disciplina}",periodo: "{periodo}", turma: "{turma}") {{
                    {data}
                }}   
            }}
        """
        variables = {
            "codigoDaDisciplina": codigo_disciplina,
            "periodo": periodo,
            "turma": turma
        }

        result = schema.execute_sync(query,variables)
        return result.data["horarioDisciplinas"]
    
    except Exception as e:
        return e
    
def get_disciplina_for_tool(codigo_disciplina, data: str = default_disciplina):
    """
    Busca disciplina com base no código
    """
    try:
        query = f"""  
            query {{
                disciplina(codigoDisciplina: "{codigo_disciplina}") {{
                    {data}
                }}   
            }}
        """
        variables = {
            "codigoDaDisciplina": codigo_disciplina,
        }

        result = schema.execute_sync(query,variables)
        return result.data["disciplina"]
    
    except Exception as e:
        return e



# pre_requisitos_disciplinas não mudar


#print(get_horarios_disciplinas("1109049","1","2024.1"))
#print(get_disciplina_for_tool("1109049"))



#DOCUMENTAÇÃO DAS TOOLS
get_disciplina_curso.__doc__ = f""" 

    Args:
        codigo_curriculo: código do currículo.
        data: campos a serem retornados, por padrão é {default_disciplina}

    Returns:
        Lista com informações desejadas da disciplina. Por padrão é {default_disciplina}
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
"""

get_disciplina.__doc__ = f""" 
    
    Args:
        codigo_da_disciplina: código numérico em string da disciplina específica.
        codigo_curriculo: código do currículo.
        data: campos a serem retornados, por padrão é {default_disciplina}
    
    Returns:
        Lista com informações desejadas da disciplina. Por padrão é {default_disciplina}
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
        Para usar este método, se 'codigo_da_disciplina' não tiver sido informado pelo usuário, obtenha os parâmetros previamente com a `get_disciplinas_curso`.

"""

get_plano_de_curso.__doc__ = f""" 
    Args:
        codigo_disciplina: código da disciplina.
        periodo: período letivo (exemplo: '2024.1', '2023.2', ...)
         data: campos a serem retornados, por padrão é {default_plano_de_curso}
    
    Returns:
        Lista com informações desejadas do plano de curso de uma disciplina. Por padrão é
        {default_plano_de_curso}
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
"""

get_plano_de_aulas.__doc__ = f""" 
   Args:
        codigo_disciplina: código da disciplina.
        periodo: período letivo (exemplo: '2024.1', '2023.2', ...).
        turma: número da turma (exemplo: '01', '02'...).
        data: campos a serem retornados, por padrão é {default_aula}
    
    Returns:
        Lista com informações desejadas do plano de aulas da turma de uma disciplina. Por padrão é {default_aula}
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
        E se a turma não for especificada, use a turma '01' como turma padrão.
"""

get_turmas.__doc__ = f""" 
    

    Args:
        periodo: o período em que a turma está.
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        data: campos a serem retornados, por padrão é {default_turma}
    
    Returns:
        Lista com informações desejadas das turmas. Por padrão é {default_turma}
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
    
"""

get_horarios_disciplinas.__doc__ = f""" 
    Args:
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        turma: a turma em questão.
        periodo: o período em que a turma está.
        data: campos a serem retornados, por padrão é {default_horario_disciplina}
    
    Returns:
        Lista com informações desejadas do horário da disciplia. Por padrão é {default_horario_disciplina}
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Além disso, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
        E se a 'turma' não for especificada, use uma string vazia para assim retornar todas as turmas.

"""

get_disciplina_for_tool.__doc__ = f""" 
    Args:
        codigo_disciplina: codigo da disciplina.
        data: campos a serem retornados, por padrão é {default_disciplina}        

    Returns:
        Lista com json que contém as informações desejadas da disciplina. Por padrão é
        {default_disciplina}
"""


        