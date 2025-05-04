import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ...sql.Estudante_na_Disciplina.prompt import PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado  import GerenciadorSQLAutomatizado
from ...sql.normalize_data_estudante import normalize_data_estudante
from ..utils.validacoes import validar_periodo, validar_curriculo, validar_turma

def get_notas_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "") -> list:
    """_summary_
    Retorna as notas dos alunos em uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - notas, aprovações ou reprovações;
    - dispensa de disciplina;
    - nomes ou matrícula dos alunos.
    
    Args:
        query (Any): Pergunta original do usuário.
        nome_da_disciplina (Any): Nome da disciplina.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        turma (Any, optional): Número da turma. Defaults to "01".
        periodo (Any, optional): Período do curso. Defaults to "".

    Returns:
        list: Chame esta função se a pergunta for sobre desempenho ou histórico dos alunos em uma disciplina.
    """

    query=str(query)    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    turma=str(turma)
    periodo=str(periodo)
    curriculo=""
    print(f"Tool get_notas_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")

    validou_turma, mensagem = validar_turma(turma_usada=turma)
    if not validou_turma: return mensagem

    if curriculo == "" and nome_do_curso != "" and nome_do_campus != "":
        curriculo = get_curriculo_mais_recente_curso(nome_do_curso, nome_do_campus)["codigo_do_curriculo"]
    else:
        validou_curriculo, mensagem = validar_curriculo(curriculo_usado=curriculo, nome_do_campus=nome_do_campus, nome_da_disciplina=nome_da_disciplina)
        if not validou_curriculo: return mensagem
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    else:
        validou_periodo, mensagem = validar_periodo(periodo=periodo)
        if not validou_periodo: return mensagem
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma
    }
    response = requests.get(f'{URL_BASE}/matriculas', params=params)

    if response.status_code == 200:
        estudantes_na_disciplina = normalize_data_estudante(json.loads(response.text))
        gerenciador = GerenciadorSQLAutomatizado(table_name="Estudante_na_Disciplina", db_name="db_estudante_disciplina.sqlite")
        gerenciador.save_data(estudantes_na_disciplina)
        
        return gerenciador.get_data(query, PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]