import json
import requests
from typing import Any
from ..campus.utils import get_campus_most_similar
from ..curso.utils import get_curso_most_similar
from .util.salvar_dados_tabela import save_cursos
from ..utils.base_url import URL_BASE
from .util.prompts import PROMPT_SQL_CURSOS
from .util.tabelas import TABELA_CURSO
from ...sql.obter_dados_sql import obter_dados_sql

def get_informacoes_cursos(query: Any, nome_do_campus: Any = "", nome_do_curso: Any = "") -> list:
    """
    Ontem informações dos cursos em geral, como nome do curso, nome do campus, turno do curso, período do de inicio do curso, data de criação do curso, código inep, modalidade academica (grau do curso) e curriculo atual e enade.

    Args:
        query: pergunta feita pelo usuário.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.
        nome_do_curso: nome do curso.
    
    Returns:
        Informações que ajude a responder a pergunta feita pelo usuário.
    """

    query=str(query)
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    print(f"Tool get_informacoes_cursos chamada com nome_do_campus={nome_do_campus} e nome_do_curso={nome_do_curso}")  

    params = { 'status':'ATIVOS' }
    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]

    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)
    if response.status_code == 200:
        cursos = json.loads(response.text)
        db_name = "db_cursos.sqlite"
        save_cursos(cursos, db_name)
        return obter_dados_sql(query, db_name, PROMPT_SQL_CURSOS, TABELA_CURSO, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]