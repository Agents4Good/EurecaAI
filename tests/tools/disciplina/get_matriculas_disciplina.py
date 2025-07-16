import json
import requests
from typing import Any

from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from ...sql.Estudante_na_Disciplina.prompt import PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA
from ...sql.Estudante_Disciplinas_Gerais.prompt import PROMPT_SQL_ESTUDANTE_DISCIPLINAS_GERAIS
from ...sql.Estudante_na_Disciplina.normalize_data import normalize_data
from ...sql.GerenciadorSQLAutomatizado  import GerenciadorSQLAutomatizado
from ..utils.remover_parametros_query import remover_parametros_da_query
from ..utils.validacoes import validar_turma


def get_matriculas_disciplina(query: Any, nome_do_campus: Any, nome_do_curso: Any, nome_da_disciplina: Any = "", periodo_de: Any = "", periodo_ate: Any = "") -> list:
    """_summary_
    Retorna informações das matrículos dos alunos em uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - notas, aprovações ou reprovações;
    - dispensa de disciplina;
    - nomes ou matrícula dos alunos;
    - quantidade de estudantes em uma disciplina de um curso.
    - observação: se na pergunta houver apenas um único período, use este período tanto para 'periodo_de' quanto para 'periodo_ate'.

    Ao usar essa ferramenta, inclua na resposta os parâmetros que foram utilizados junto com a resposta encontrada.
    
    Args:
        query (Any): Pergunta completa do usuário.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        nome_do_curso (Any): Nome do curso. Defaults to "".
        nome_da_disciplina (Any): Nome da disciplina.
        periodo_de (Any): Período mínimo de busca. Defaults to "".
        periodo_ate (Any): Período máximo de busca. Defaults to "".

    Returns:
        list: Uma lista com informações relevantes a respeito das matrículas dos estudantes de uma disciplina.
    """

    #query = str(query)
    query= remover_parametros_da_query(query, excluir=['self'])   
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    periodo_de=str(periodo_de)
    periodo_ate=str(periodo_ate)
    curriculo=""
    print(f"Tool `get_matriculas_disciplina` chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, periodo_de={periodo_de}, periodo_ate={periodo_ate} e curriculo={curriculo}")
    print(f"Query da pergunta: {query}")
    
    if periodo_de == "" and periodo_ate == "":
        periodo_de = periodo_ate = get_periodo_mais_recente()

    params = {
        "periodo-de": periodo_de,
        "periodo-ate": periodo_ate
    }

    if nome_da_disciplina and nome_do_campus:
        dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
        params["disciplina"] = dados_disciplina["disciplina"]["codigo"]

    if nome_do_curso:
        dados_curso = get_curso_most_similar(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        params["curso"] = dados_curso["curso"]["codigo"]
    
    else: return ["Erro: Informe que o usuário deve passar somente o curso para obter informação de todas as disciplinas ou então a disciplina desejada junto do curso dela."]


    response = requests.get(f'{URL_BASE}/matriculas', params=params)

    if response.status_code == 200:
        estudantes_na_disciplina = normalize_data(json.loads(response.text))

        if nome_da_disciplina != "":
            gerenciador = GerenciadorSQLAutomatizado(table_name="Estudante_na_Disciplina", db_name="db_estudante_disciplina.sqlite", prompt=PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA)
            gerenciador.save_data(estudantes_na_disciplina)
        else:
            gerenciador = GerenciadorSQLAutomatizado(table_name="Estudante_Disciplinas_Gerais", db_name="db_estudante_disciplinas_gerais.sqlite", prompt=PROMPT_SQL_ESTUDANTE_DISCIPLINAS_GERAIS)
            gerenciador.save_data(estudantes_na_disciplina)

        try:
            dados = gerenciador.get_data("estudante_na_disciplina",query, True)
            if len(dados) == 0:
                return ["Não foi encontrado nada"]
        except TypeError as e:
            return [{"Error": "Ocorreu um erro para gerar a consulta SQL."}]
       
        return dados
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]