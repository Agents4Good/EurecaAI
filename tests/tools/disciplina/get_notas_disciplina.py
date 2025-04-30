import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from .disciplina_utils.informacoes_aluno_disciplina.insert_matricula_disciplina import save_disciplinas
from .disciplina_utils.informacoes_aluno_disciplina.prompt_matricula_disciplina import PROMPT_DISCIPLINA
from .disciplina_utils.informacoes_aluno_disciplina.tabela_matricula_disciplina import TABELA_ESTUDANTEDISCIPLINA
from ...sql.obter_dados_sql import obter_dados_sql

from faker import Faker
faker = Faker('pt_BR')

def get_notas_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "") -> list:
    """
    Retorna as notas dos alunos em uma disciplina.

    Use esta função quando a pergunta envolver:
    - notas, aprovações ou reprovações;
    - dispensa de disciplina;
    - nomes ou matrícula dos alunos.

    Parâmetros:
    - query: Pergunta original do usuário.
    - nome_da_disciplina: Nome da disciplina.
    - nome_do_curso: Nome do curso.
    - nome_do_campus: Cidade do campus.
    - turma: (Opcional) Número da turma.
    - periodo: (Opcional) Período do curso.

    Chame esta função se a pergunta for sobre desempenho ou histórico dos alunos em uma disciplina.
    """
    query=str(query)
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    turma=str(turma)
    periodo=str(periodo)
    curriculo=""

    if curriculo == "" and nome_do_curso != "" and nome_do_campus != "":
        curriculo = get_curriculo_mais_recente_curso(nome_do_curso, nome_do_campus)["codigo_do_curriculo"]
    
    print(f"Tool get_media_notas_turma_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma
    }

    response = requests.get(f'{URL_BASE}/matriculas', params=params)
    if response.status_code == 200:
        matriculas = json.loads(response.text)
        db_name = "db_disciplina.sqlite"
        save_disciplinas(matriculas, db_name)
        return obter_dados_sql(query, db_name, PROMPT_DISCIPLINA, TABELA_ESTUDANTEDISCIPLINA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]