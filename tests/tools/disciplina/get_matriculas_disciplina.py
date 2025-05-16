import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ...sql.Estudante_na_Disciplina.prompt import PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado  import GerenciadorSQLAutomatizado
from ..utils.validacoes import validar_turma
from langchain_core.tools import tool

def get_matriculas_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "", periodo: Any = "") -> list:
    """_summary_
    Retorna informações das matrículos dos alunos em uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - notas, aprovações ou reprovações;
    - dispensa de disciplina;
    - nomes ou matrícula dos alunos;
    - quantidade de estudantes em uma disciplina de um curso.
    
    Args:
        query (Any): Pergunta do usuário.
        nome_da_disciplina (Any): Nome da disciplina.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        turma (Any, optional): Número da turma. Defaults to "".
        periodo (Any, optional): Período do curso. Defaults to "".

    Returns:
        list: Uma lista com informações relevantes a respeito das matrículas dos estudantes de uma disciplina.
    """

    query=str(query)    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    turma=str(turma)
    periodo=str(periodo)
    curriculo=""
    print(f"Tool `get_matriculas_disciplina` chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")

    validou_turma, mensagem = validar_turma(turma_usada=turma)
    if not validou_turma: return mensagem
    
    periodo = periodo if periodo != "" else get_periodo_mais_recente()
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma
    }
    response = requests.get(f'{URL_BASE}/matriculas', params=params)

    if response.status_code == 200:
        estudantes_na_disciplina = json.loads(response.text)
        gerenciador = GerenciadorSQLAutomatizado(table_name="Estudante_na_Disciplina", db_name="db_estudante_disciplina.sqlite")
        gerenciador.save_data(estudantes_na_disciplina)

        try:
            dados = gerenciador.get_data(query, PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA, temperature=0)
            if len(dados) == 0:
                return ["Não foi encontrado nada"]
        except TypeError as e:
            return [{"Error": "Ocorreu um erro para gerar a consulta SQL."}]
        print(dados)
        return dados
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]