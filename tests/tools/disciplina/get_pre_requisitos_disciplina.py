import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso

def get_disciplina_for_tool(codigo_da_disciplina):
    params = { 'disciplina': codigo_da_disciplina }
    response = requests.get(f'{URL_BASE}/disciplinas', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def get_pre_requisitos_disciplina(nome_da_disciplina:Any, nome_do_curso:Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """_summary_
    Retorna os pré-requisitos de uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - disciplinas que devem ser cursadas antes;
    - requisitos formais de matrícula.
    
    Args:
        nome_da_disciplina (Any): Nome da disciplina.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        curriculo (Any, optional): Ano do currículo. Defaults to "".

    Returns:
        list: Uma lista com as disciplinas que são pré-requisitos de outra.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    curriculo=str(curriculo)
    print(f"Tool pre_requisitos_disciplinas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}")
    
    if curriculo == "":
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)["codigo_do_curriculo"]

    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    if type(dados_disciplina) == list and type(dados_disciplina[0]) == dict and "error_status" in dados_disciplina[0]:
       return dados_disciplina[0]["msg"]
    
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