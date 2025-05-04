import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE
from ..utils.validacoes import validar_curriculo, validar_periodo, validar_turma

def get_plano_de_aulas(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, periodo: Any = "", turma: Any = "", curriculo: Any = "") -> list:
    """_summary_
    Retorna o plano de aulas de uma turma.
    
    Use esta função quando a pergunta envolver:
    - número, data da aula ou duração das aulas;
    - conteúdo abordado em cada aula.
    - conteúdo que já foi abordado ou que ainda será abordado.
    Por exemplo, 'Qual foi o conteúdo abordado na aula do dia 05/04/2024?', 'Qual foi o assunto abordado na primeira aula?' 'Qual foi o assunto abordado na aula 5?'
    
    Args:
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        nome_da_disciplina (Any): Nome da disciplina.
        periodo (Any, optional): Período do curso. Defaults to "".
        turma (Any, optional): Número da turma. Defaults to "".
        curriculo (Any, optional): Ano do currículo. Defaults to "".

    Returns:
        list: Lista dos cronograma de aulas da disciplina.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    curriculo=str(curriculo)
    turma=str(turma)
    periodo=str(periodo)
    print(f"Tool get_plano_de_aulas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, periodo={periodo}, numero_turma={turma} e curriculo={curriculo}.")
    
    validou_turma, mensagem = validar_turma(turma_usada=turma)
    if not validou_turma: return mensagem
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    else:
        validou_periodo, mensagem = validar_periodo(periodo=periodo)
        if not validou_periodo: return mensagem
    
    if curriculo != "":
        validou_curriculo, mensagem = validar_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo_usado=curriculo)    
        if not validou_curriculo: return mensagem
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)

    params = {
        'disciplina': dados_disciplina["disciplina"]["codigo"],
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': turma
    }
    response = requests.get(f'{URL_BASE}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]