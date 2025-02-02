
import json
import requests
from strawberry_demo.main import schema
from .default_data.default_disciplina_data import *
from langchain.tools import tool
from .url_config import base_url

@tool
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


@tool
def pre_requisitos_disciplinas(codigo_disciplina: str, codigo_curriculo="2023") -> dict:

    """
    Buscar os nomes da disciplinas que são requisitos da disciplina desejada.

    Args:
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        codigo_curriculo: código do currículo.
    
    Returns:
        Dicionário com o nome de cada disciplina que é requisito para a disciplina desejada. Se o retorno for vazio, informe que a disciplina em questão não possui requisitos.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
    """
    params = {
        'disciplina': codigo_disciplina,
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/pre-requisito-disciplinas', params=params)

    if response.status_code == 200:
        requisitos = json.loads(response.text)

        print(requisitos)
        disciplinas = []

        for requisito in requisitos:
            disciplina_req = get_disciplina_for_tool(
                requisito['condicao'],
            )

            disciplinas.append(disciplina_req[0]['nome'])

        return set(disciplinas)
    else:
        [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


@tool
def get_media_notas_turma_disciplina(periodo: str = '2024.1', codigo_disciplina: str = '', turma: str = '01') -> dict:
    """
    Buscar as notas de estudantes em uma turma de uma disciplina.

    Args:
        periodo: o período em que a turma está.
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        turma: a turma em questão.
    
    Returns:
        Dicionário com o intervalo das médias das notas de dada disciplina de uma turma.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Caso o 'periodo' não tiver sido informado, use o '2024.1' como periodo padrão.
        E se a turma não for especificada, use a turma '01' como turma padrão.
    """
    print(f"Tool get_media_notas_turma_disciplina chamada com periodo={periodo}, codigo_disciplina={codigo_disciplina} e turma={turma}.")
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": codigo_disciplina,
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
    


@tool
def get_disciplinas_curso(codigo_curriculo: str, data: str = default_disciplina):
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

        print(f"Tool get_disciplinas_curso com codigo_curriculo {codigo_curriculo} e data {data}")
        result = schema.execute_sync(query,variables)
        return result.data["disciplinaPorCursoCurriculo"]
    
    except Exception as e:
        return e

@tool
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

        print(f"Tool get_disciplina com codigo_disciplina {codigo_da_disciplina}, curriculo {codigo_curriculo} e data {data}")

        result = schema.execute_sync(query,variables)
        return result.data["disciplinaPorCodigoCurriculo"]
    
    except Exception as e:
        return e
    

@tool
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

        print(f"Tool get_plano_curso com codigo_disciplina {codigo_disciplina}, periodo {periodo} e data {data}")
        result = schema.execute_sync(query,variables)
        return result.data["planoDeCursoPorDisciplinaPeriodo"]
    
    except Exception as e:
        return e
    

@tool
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

        print(f"Tool get_plano_de_aulas com codigo_disciplina {codigo_disciplina}, periodo {periodo}, turma {turma} e data {data}")
        result = schema.execute_sync(query,variables)
        return result.data["planoDeAula"]
    
    except Exception as e:
        return e


@tool
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

        print(f"Tool get_turmas com codigo_disciplina {codigo_disciplina}, periodo {periodo}, e data {data}")

        result = schema.execute_sync(query,variables)
        return result.data["Turma"]
    
    except Exception as e:
        return e
    
#get_media_notas_turma_disciplina não pode ser mudado

@tool
def get_horarios_disciplinas(codigo_disciplina:str, periodo:str, data: str = default_horario_disciplina,turma:str = "1"):
    """
    Buscar os horários e a sala de uma disciplina de uma turma especificada (caso     não  seja, busca de todas as turmas).
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

        print(f"Tool get_horarios_disciplinas com codigo_disciplina {codigo_disciplina}, periodo {periodo},turma {turma} e data {data}")

        result = schema.execute_sync(query,variables)
        print("RES ", result)
        return result.data["horarioDisciplinas"]
    
    
    except Exception as e:
        return e
    


#DOCUMENTAÇÃO DAS TOOLS
get_disciplinas_curso.__doc__ = f""" 

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


        