import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..utils.obter_dados_sql import obter_dados_sql
from .disciplina_utils.informacoes_aluno_disciplina.insert_matricula_disciplina import save_disciplinas
from .disciplina_utils.informacoes_aluno_disciplina.prompt_matricula_disciplina import PROMPT
from .disciplina_utils.informacoes_aluno_disciplina.tabela_matricula_disciplina import TABELA
from faker import Faker
faker = Faker('pt_BR')

def get_informacoes_aluno_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "") -> list:
    """
    Buscar informações relevantes dos estudantes em uma disciplina específica, como as matrículas deles, as notas (médias), dispensa da disciplina e o status (situação) dos estudantes na disciplina.

    Args:
        query: pergunta feita pelo usuário.
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Se o usuário não informou o campus de Campina Grande)
        turma: valor numérico da turma da disciplina (se não foi informada, então passe a strig vazia '').
        periodo: periodo do curso (se não foi informado, então passe a string vazia '').
    
    Returns:
        Informações relacionados aos estudantes da disciplina.
    """
    query=str(query)
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    
    turma=str(turma)
    periodo=str(periodo)
    curriculo= ""
    curriculo=str(curriculo)
    
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
        return obter_dados_sql(query, db_name, PROMPT, TABELA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]