import json
import requests
from typing import Any
from ..campus.utils import get_campus_most_similar
from .utils import get_lista_cursos
from ..utils.base_url import URL_BASE
from ...sql.Curso.prompt import PROMPT_SQL_CURSOS
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ..utils.remover_parametros_query import remover_parametros_da_query

def obter_dados_de_todos_os_cursos(query: Any, nome_do_campus: Any = "") -> list:
    """
    _summary_
    Buscar informações relativo a todos os cursos da UFCG, como código do curso, nome do curso, código do setor, nome do setor, 
    nome do campus, turno do curso, período do de inicio do curso, código inep, modalidade academica (grau do curso), curriculo atual, ciclo enade e data de criação do curso.
    Use esta função quando o usuário fizer uma pergunta **geral** sobre cursos da UFCG, sem mencionar nomes específicos.
    
    Exemplos de uso:
        - "Quantos cursos são oferecidos em Patos?"
        - "Quais cursos são noturnos em Cajazeiras?"
        - "Quantos cursos de graduação existem?"
        - "Quantos cursos de graduação existem em Sousa?"
    
    Args:
        query: pergunta completa feita pelo usuário.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.
    
    Returns:
        Informações que ajude a responder a pergunta feita pelo usuário.
    """

    #query= remover_parametros_da_query(query, excluir=['self'])
    query = str(query)
    nome_do_campus=str(nome_do_campus)
    print(f"Tool `obter_dados_de_todos_os_cursos` chamada com nome_do_campus={nome_do_campus}")  

    params = {'status':'ATIVOS' }
    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]

    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)
    if response.status_code == 200:
        cursos = json.loads(response.text)
        gerenciador = GerenciadorSQLAutomatizado("Curso", "db_cursos.sqlite", PROMPT_SQL_CURSOS, temperature=0.0)
        gerenciador.save_data(cursos)
        return gerenciador.get_data("curso", query)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]