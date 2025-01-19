import requests
import json
from langchain_core.tools import tool

base_url = "https://eureca.sti.ufcg.edu.br/das/v2"

@tool
def get_disciplinas_curso(codigo_curriculo="2023") -> list:
    """
    Buscar todas as disciplinas do curso de Ciência da Computação da UFCG.

    Args:
        base_url: URL base da API.
        codigo_curriculo: código do currículo.
    
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
        print("Tool get_cursos_ativos retornou com sucesso.")
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        print("Tool get_cursos_ativos retornou com sucesso.")
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_disciplina(codigo_da_disciplina: str, codigo_curriculo="2023") -> list:
    """
    Buscar as informações de uma disciplina do curso de Ciência da Computação da UFCG.

    Args:
        base_url: URL base da API.
        codigo_da_disciplina: código numérico em string da disciplina específica.
        codigo_curriculo: código do currículo.
    
    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
        Para usar este método, se 'codigo_da_disciplina' não tiver sido informado pelo usuário, obtenha os parâmetros previamente com a tool `get_disciplinas_curso`.
    """
    print(f"Tool get_disciplinas_curso chamada com base_url={base_url}, codigo_curriculo={codigo_curriculo}, codigo_da_disciplina={codigo_da_disciplina}")
    params = {
        'curso': '14102100',
        'curriculo': codigo_curriculo,
        'disciplina': codigo_da_disciplina
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        print("Tool get_cursos_ativos retornou com sucesso.")
        return json.loads(response.text)
    else:
        print("Tool get_cursos_ativos retornou com sucesso.")
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_plano_de_curso(codigo_disciplina: str, periodo: str) -> list:
    """
    Plano de curso de uma disciplina (do curso de Ciência da Computação).

    Args:
        base_url: URL base da API.
        codigo_disciplina: código da disciplina.
        periodo: período letivo (exemplo: '2024.1', '2023.2', ...)
    
    Returns:
        Lista com informações relevantes do plano de curso de uma disciplina.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo,
        'periodo-ate': periodo
    }

    response = requests.get(f'{base_url}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_plano_de_aulas(codigo_disciplina: str, periodo: str, numero_turma: str) -> list:
    """
    Buscar plano de aulas de uma turma de uma disciplina.

    Args:
        base_url: URL base da API.
        codigo_disciplina: código da disciplina.
        periodo: período letivo (exemplo: '2024.1', '2023.2', ...).
        numero_turma: número da turma (exemplo: '01', '02'...).
    
    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
        E se a turma não for especificada, use a turma '01' como turma padrão.
    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': numero_turma
    }

    response = requests.get(f'{base_url}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_turmas(periodo: str, codigo_disciplina: str) -> list:
    """
    Buscar turmas.

    Args:
        base_url: URL base da API.
        periodo: o período em que a turma está.
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
    
    Returns:
        Lista com informações relevantes das turmas.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
    """
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": codigo_disciplina
    }
    
    response = requests.get(f'{base_url}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_media_notas_turma_disciplina(periodo: str, codigo_disciplina: str, turma: str) -> dict:
    """
    Buscar as notas de estudantes em uma turma de uma disciplina.

    Args:
        base_url: URL base da API.
        periodo: o período em que a turma está.
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        turma: a turma em questão.
    
    Returns:
        Dicionário com o intervalo das médias das notas de dada disciplina de uma turma.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, solicite que o `Agente_Campus_Eureca` forneça o período mais recente.
        E se a turma não for especificada, use a turma '01' como turma padrão.
    """
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
      return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_horarios_disciplinas(base_url, codigo_disciplina, turma, periodo):
    """
    Buscar os horários e a sala de uma disciplina de uma turma especificada (caso não seja, busca de todas as turmas).

    Args:
        base_url: URL base da API.
        codigo_disciplina: o código numérico em string da disciplina que a turma está.
        turma: a turma em questão.
        periodo: o período em que a turma está.
    
    Returns:
        Dicionário com o intervalo das médias das notas de dada disciplina de uma turma.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Além disso, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
        E se a 'turma' não for especificada, use uma string vazia para assim retornar todas as turmas.
    """
    params = {
        "disciplina": codigo_disciplina,
        "turma": turma,
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
        return [{"erro": "Não foi possível obter informação da UFCG."}]

def get_disciplina_for_tool(base_url, disciplina):
  params = {
    'disciplina': disciplina,
  }

  response = requests.get(f'{base_url}/disciplinas', params=params)

  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

@tool
def pre_requisitos_disciplinas(codigo_disciplina: str, codigo_curriculo="2023") -> dict:
    """
    Buscar os nomes da disciplinas que são requisitos da disciplina desejada.

    Args:
        base_url: URL base da API.
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
        disciplinas = []

        for requisito in requisitos:
            disciplina_req = get_disciplina_for_tool(
                base_url,
                requisito['condicao'],
            )

            disciplinas.append(disciplina_req[0]['nome'])

        return set(disciplinas)