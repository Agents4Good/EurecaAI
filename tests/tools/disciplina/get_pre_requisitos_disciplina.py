import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE

def get_disciplina_for_tool(codigo_da_disciplina):
    params = { 'disciplina': codigo_da_disciplina }
    response = requests.get(f'{URL_BASE}/disciplinas', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def get_pre_requisitos_disciplina(nome_da_disciplina:Any, nome_do_curso:Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """
    Busca as disciplinas que são pré-requisitos ou requisitos da disciplina perguntada.
    Essa ferramenta retorna todas as disciplinas que são pré-requisitos da disciplina.

    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo", se não souber use a string vazia '' para usar o currículo mais recente).
    
    Returns:
        Lista contentdo o nome de cada disciplina que é requisito para a disciplina desejada. 
        Se o retorno for uma lista vazia, então informe que a disciplina em questão não possui requisitos.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    curriculo=str(curriculo)
    
    print(f"Tool pre_requisitos_disciplinas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}")
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    params = {
        'disciplina': dados_disciplina["disciplina"]["codigo"],
        'curriculo': curriculo
    }

    response = requests.get(f'{URL_BASE}/pre-requisito-disciplinas', params=params)

    if response.status_code == 200:
        requisitos = json.loads(response.text)
        disciplinas = []
        for requisito in requisitos:
            disciplina_req = get_disciplina_for_tool(requisito['condicao'])
            disciplinas.append(disciplina_req[0]['nome'])

        return list(set(disciplinas))
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]