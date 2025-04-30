import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
#from .disciplina_utils.informacoes_aluno_disciplina.insert_matricula_disciplina import save_disciplinas
#from .disciplina_utils.informacoes_aluno_disciplina.prompt_matricula_disciplina import PROMPT_ESTUDANTE_NA_DISCIPLINA
#from .disciplina_utils.informacoes_aluno_disciplina.tabela_matricula_disciplina import TABELA_DISCIPLINA

#from ...sql.obter_dados_sql import obter_dados_sql
from ...sql.Estudante_na_Disciplina.prompt import PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado  import GerenciadorSQLAutomatizado
from ...sql.normalize_data_estudante import normalize_data_estudante

def get_informacoes_aluno_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "", curriculo: Any = "") -> list:
    """
    Buscar informações relevantes dos estudantes em uma disciplina específica, como as matrículas deles, as notas (médias), dispensa da disciplina e o status (situação) dos estudantes na disciplina.

    Args:
        query: pergunta feita pelo usuário.
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Se o usuário não informou o campus de Campina Grande)
        turma: valor numérico da turma da disciplina (se não foi informada, então passe a strig vazia '').
        periodo: periodo do curso (se não foi informado, então passe a string vazia '').
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo").
    
    Returns:
        Informações relacionados aos estudantes da disciplina.
    """

    db_name = "db_disciplina.sqlite"
    #gerenciador = GerenciadorSQLAutomatizado(table_name="Estudante_na_Disciplina", db_name=db_name)

    query=str(query)
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)

    turma=str(turma)
    periodo=str(periodo)
    curriculo=str(curriculo)

    if curriculo == "" and nome_do_curso != "" and nome_do_campus != "":
        curriculo = get_curriculo_mais_recente_curso(nome_do_curso, nome_do_campus)
    
    print(f"Tool get_media_notas_turma_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma
    }

    response = requests.get(f'{URL_BASE}/matriculas', params=params)

    print("\n\nDADOS \n\n", response[0], "\n")
    return;
    if response.status_code == 200:
        estudantes_na_disciplina = normalize_data_estudante(json.loads(response.text))
        #save_disciplinas(matriculas, db_name)
        gerenciador.save_data(estudantes_na_disciplina)
        #return obter_dados_sql(query, db_name, PROMPT_ESTUDANTE_NA_DISCIPLINA, TABELA_DISCIPLINA, temperature=0)
        return gerenciador.get_data(query, PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]