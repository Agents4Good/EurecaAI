import requests
import json
from .url_config import base_url


def get_disciplinas_curso(codigo_curriculo: str) -> list:
    """
    Buscar todas as disciplinas do curso de Ciência da Computação da UFCG.

    Args:
        codigo_curriculo: código do currículo.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
    """
    print(f"chamada a API com base_url={base_url}/disciplinas, codigo_curriculo={codigo_curriculo}.")
    params = {
        'curso': '14102100',
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
       # res = json.loads(response.text)
        return json.loads(response.text)
        #return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_disciplina(codigo_da_disciplina: str, codigo_curriculo: str) -> list:
    """
    Buscar as informações de uma disciplina do curso de Ciência da Computação da UFCG.

    Args:
        codigo_da_disciplina: código numérico em string da disciplina específica.
        codigo_curriculo: código do currículo.
    
    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, use o padrão que é '2023'.
        Para usar este método, se 'codigo_da_disciplina' não tiver sido informado pelo usuário, obtenha os parâmetros previamente com a `get_disciplinas_curso`.
    """
    print(f"chamada a API com base_url={base_url}/disciplinas, codigo_curriculo={codigo_curriculo}, codigo_da_disciplina={codigo_da_disciplina}")
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


def get_plano_de_curso(codigo_disciplina: str, periodo: str) -> list:
    """
    Plano de curso de uma disciplina (do curso de Ciência da Computação).

    Args:
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
    print(f"Chamada a API com url {base_url}/planos-de-curso com codigo_disciplina={codigo_disciplina} e periodo={periodo}.")
    response = requests.get(f'{base_url}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_plano_de_aulas(codigo_disciplina: str, periodo: str, turma: str) -> list:
    """
    Buscar plano de aulas de uma turma de uma disciplina.

    Args:
        codigo_disciplina: código da disciplina.
        periodo: período letivo (exemplo: '2024.1', '2023.2', ...).
        turma: número da turma (exemplo: '01', '02'...).
    
    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Para usar este método, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, informe ao supervisor para buscar o **período mais recente** com o agente 'Agente_Campus_Eureca'.
        E se a turma não for especificada, use a turma '01' como turma padrão.
    """
    print(f"Chamada a API com url {base_url}/aulas e codigo_disciplina={codigo_disciplina}, periodo={periodo} e turma={turma}.")
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': turma
    }

    response = requests.get(f'{base_url}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


def get_turmas(periodo: str, codigo_disciplina: str) -> list:
    """
    Buscar turmas.

    Args:
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
    
    print(f"Chamada a API com url {base_url}/turmas com codigo_disciplina={codigo_disciplina}, periodo={periodo}")
    response = requests.get(f'{base_url}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]


### esse não muda
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


def get_horarios_disciplinas(codigo_disciplina:str, turma:str, periodo:str):
    """
    Buscar os horários e a sala de uma disciplina de uma turma especificada (caso não seja, busca de todas as turmas).

    Args:
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
    print(f"Chamada a API com url {base_url}/turmas com codigo_disciplina={codigo_disciplina}, turma{turma} e periodo={periodo}")

    if response.status_code == 200:
        horarios = json.loads(response.text)
        
        
        # filtros_horarios = []
        # turmas_map = {}

        # for horario in horarios:
        #     turma = horario['turma']
        #     sala = horario['codigo_da_sala']
        #     dia = str(horario['dia'])
        #     horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

        #     if turma not in turmas_map:
        #         turmas_map[turma] = {
        #             'turma': turma,
        #             'sala': sala,
        #             'horarios': {}
        #         }
        #         filtros_horarios.append(turmas_map[turma])

        #     turmas_map[turma]['horarios'][dia] = horario_formatado

        return horarios
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

def get_disciplina_for_tool(codigo_disciplina: str):
  """
    Busca disciplina com base no código.

    Args:
        codigo_disciplina: codigo da disciplina

    Returns:
        Lista com json da disciplina desejada.
  """
  params = {
    'disciplina': codigo_disciplina,
  }

  response = requests.get(f'{base_url}/disciplinas', params=params)

  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

#não mudar esse aqui também
def pre_requisitos_disciplinas(codigo_disciplina: str, codigo_curriculo: str ="2023") -> dict:

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


