import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..utils.validacoes import valida_periodo_curriculo

def get_turmas_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, periodo: Any = "", curriculo: Any = "") -> list:
    """_summary_
    Retorna todas as turmas de uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - número da turma;
    - período, carga horária ou tipo da turma.
    
    Args:
        nome_da_disciplina (Any): Nome da disciplina.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        periodo (Any, optional): Período do curso. Defaults to "".
        curriculo (Any, optional): Ano do currículo. Defaults to "".

    Returns:
        list: Chame esta função se a pergunta for sobre quais turmas existem para a disciplina.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    curriculo=str(curriculo)
    periodo=str(periodo)
    print(f"Tool get_turmas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, periodo={periodo} e codigo_curriculo={curriculo}")
    
    periodo, curriculo, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, periodo=periodo, curriculo=curriculo)
    if mensagem != "": return mensagem

    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)

    if type(dados_disciplina) == list and type(dados_disciplina[0]) == dict and "error_status" in dados_disciplina[0]:
       return dados_disciplina[0]["msg"]

    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"]
    }
    
    response = requests.get(f'{URL_BASE}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da disciplina porque a disciplina não existe para esse período ou curriculo."}]