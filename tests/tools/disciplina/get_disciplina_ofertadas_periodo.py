from typing import Any
from ..utils.validacoes import valida_periodo_curriculo
from ..setor.utils import get_setor_most_similar, get_setor_most_similar_por_codigo
from ..curso.utils import get_curso_most_similar
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ..utils.remover_parametros_query import remover_parametros_da_query
from ...sql.Disciplina.prompt import PROMPT_SQL_DISCIPLINA
from ..utils.base_url import URL_BASE
import requests
import json

def get_disciplina_ofertadas_periodo(query: Any, nome_do_curso: Any, nome_do_campus: Any, periodo: Any = ""):
    """_summary_
    Retorna as disciplinas ofertadas por um curso em um período específico.
    
    Use esta função quando a pergunta envolver:
    - código, nome, créditos ou carga horária da disciplina;
    - carga teórica/prática semanal ou total;
    - número de semanas de aula;
    - nome do setor responsável e campus;
    - carga de extensão ou contabilização de créditos.
    
    Chame esta função se a pergunta for sobre as disciplinas que o curso oferece no período.
    
    Args:
        query (Any): reformule a pergunta sem citar nome de curso, nem de campus e nem currículo nesse parâmetro.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        periodo (Any, optional): Período do curso. Defaults to "".

    Returns:
        list: Uma lista com informações relevantes sobre a pergunta a respeito da(s) disciplina(s) no período.
    """

    #query= remover_parametros_da_query(query, excluir=['self'])
    query = str(query)
    nome_do_curso=str(nome_do_curso)    
    nome_do_campus=str(nome_do_campus)
    periodo=str(periodo)
    print(f"Tool `get_disciplina_ofertadas_periodo` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e periodo={periodo}.")

    dados_curso, _, periodo, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo="", periodo=periodo)
    if mensagem != "": return mensagem
    
    params = {
        'curso': dados_curso['curso']['codigo'],
        'periodo-de': periodo,
        'periodo-ate': periodo
    }
    response = requests.get(f'{URL_BASE}/turmas-por-cursos', params=params)
    
    if response.status_code == 200:
        print("Turmas retornadas com sucesso")
        turmas = json.loads(response.text)
        codigo_disciplinas = list(set(turma["codigo_da_disciplina"] for turma in turmas))
        print(dados_curso["curso"]["codigo"][0])
        setor_mais_similar = get_setor_most_similar_por_codigo(codigo_do_campus=str(dados_curso["curso"]["codigo"][0]), nome_do_centro_setor=nome_do_curso, filtro="UNID")

        disciplinas_dentro = []
        response_disciplina = requests.get(f'{URL_BASE}/disciplinas', params={ "setor": setor_mais_similar["setor"]["codigo"], "curso": dados_curso['curso']['codigo']})
        if response_disciplina.status_code == 200:
            disciplinas_curso = json.loads(response_disciplina.text)
            for disciplina in disciplinas_curso:
                if disciplina["codigo_da_disciplina"] in codigo_disciplinas:
                    disciplinas_dentro.append(disciplina)
        
        if query == "":
            return disciplinas_dentro
        gerenciador = GerenciadorSQLAutomatizado(table_name="Disciplina", db_name="db_disciplina.sqlite", prompt=PROMPT_SQL_DISCIPLINA)
        gerenciador.save_data(disciplinas_dentro)
        return gerenciador.get_data("disciplina", query)
    
    else:
        print(response.json())
        return [{"error_status": response.status_code, "msg": response.json()}]