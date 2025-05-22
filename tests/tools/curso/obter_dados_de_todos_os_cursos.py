import json
import requests
from typing import Any
from ..campus.utils import get_campus_most_similar
from ..utils.base_url import URL_BASE
from ...sql.Curso.prompt import PROMPT_SQL_CURSOS
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado

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

    query=str(query)

    
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
        gerenciador = GerenciadorSQLAutomatizado("Curso", "db_cursos.sqlite")
        gerenciador.save_data(cursos)
        return gerenciador.get_data(query, PROMPT_SQL_CURSOS, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]
    
    {
    "Curso": {
        "codigo_do_curso": {
            "type": "INTEGER",
            "description": "Codigo do curso",
            "mapper": "codigo_do_curso"
        },
        "nome_do_curso": {
            "type": "TEXT",
            "description": "Nome do curso",
            "mapper": "descricao"
        },
        "codigo_do_setor": {
            "type": "INTEGER",
            "description": "Codigo do setor",
            "mapper": "codigo_do_setor"
        },
        "nome_do_setor": {
            "type": "TEXT",
            "description": "Nome do setor",
            "mapper": "nome_do_setor"
        },
        "nome_do_campus": {
            "type": "TEXT",
            "description": "Nome do campus",
            "mapper": "nome_do_campus"
        },
        "turno": {
            "type": "TEXT",
            "description": "Turno do curso",
            "mapper": "turno"
        },
        "periodo_de_inicio": {
            "type": "TEXT",
            "description": "Periodo de inicio do curso",
            "mapper": "periodo_de_inicio"
        },
        "codigo_inep": {
            "type": "INTEGER",
            "description": "Codigo do INEP",
            "mapper": "codigo_inep"
        },
        "modalidade_academica": {
            "type": "TEXT",
            "description": "Modalidade acadêmica do curso cuja opções são BACHARELADO, LICENCIATURA, TECNICO",
            "mapper": "modalidade_academica"
        },
        "curriculo_atual": {
            "type": "TEXT",
            "description": "É o ano em que a grade do curso foi renovada",
            "mapper": "curriculo_atual"
        },
        "ciclo_enade": {
            "type": "INTEGER",
            "description": "De quantos em quantos semestres ocorre a prova do enade",
            "mapper": "ciclo_enade"
        }
    }
}