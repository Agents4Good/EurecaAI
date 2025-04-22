import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..campus.utils import get_campus_most_similar
from ..utils.obter_dados_sql import obter_dados_sql
from .util.salvar_dados_tabela import save_estudantes_cursos
from ..utils.base_url import URL_BASE
from .util.prompts import PROMPT_SQL_ESTUDANTES
from .util.tabelas import TABELA_ESTUDANTE_CURSO

def get_informacoes_estudantes(query: Any, nome_do_curso: Any, nome_do_campus: Any) -> dict:
    """
    Buscar informações gerais dos estudantes da UFCG com base no(s) curso(s).

    Args:
        query: Pergunta feita pelo usuário.
        nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 

    Returns:
        Informações que ajude a responder a pergunta feita pelo usuário.
    """

    print(f"Tool get_estudantes chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")    
    params = { "situacao-do-estudante": "ATIVOS" }
    pergunta_feita = str(pergunta_feita)
    nome_do_campus = str(nome_do_campus)
    nome_do_curso = str(nome_do_curso)
    
    if (nome_do_curso != "" and nome_do_campus != ""):
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        params["curso"] = dados_curso['curso']['codigo']
    elif (nome_do_curso == "" and nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params["campus"] = dados_campus['campus']['codigo']
    elif (nome_do_curso == "" and nome_do_campus == ""):
        pass
    else:
        return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]
    
    response = requests.get(f'{URL_BASE}/estudantes', params=params)
    if response.status_code == 200:
        estudantes = json.loads(response.text)
        db_name = "estudantes_db.sqlite"
        save_estudantes_cursos(estudantes, db_name)
        return obter_dados_sql(query, db_name, PROMPT_SQL_ESTUDANTES, TABELA_ESTUDANTE_CURSO, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]