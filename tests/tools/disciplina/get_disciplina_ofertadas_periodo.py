from typing import Any
from ..utils.validacoes import valida_periodo_curriculo
from ..curso.utils import get_curso_most_similar
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
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

    query=str(query)
    nome_do_curso=str(nome_do_curso)    
    nome_do_campus=str(nome_do_campus)
    periodo=str(periodo)
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e periodo={periodo}.")

    periodo, _, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo="", periodo=periodo)
    if mensagem != "": return mensagem
    
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)

    params = {
        'curso': dados_curso['curso']['codigo'],
        'periodo-de': periodo,
        'periodo-ate': periodo
    }
    response = requests.get(f'{URL_BASE}/turmas', params=params)
    
    if response.status_code == 200:
        print("Turmas retornadas com sucesso")
        turmas = json.loads(response.text)
        codigo_disciplinas = list(set(turma["codigo_da_disciplina"] for turma in turmas))

        disciplinas = []
        for codigo_disciplina in codigo_disciplinas:
            response_disciplina = requests.get(f'{URL_BASE}/disciplinas', params={ "disciplina": codigo_disciplina })
            if response_disciplina.status_code == 200:
                disciplinas.append(json.loads(response_disciplina.text)[0])

        if query == "":
            return disciplinas
        gerenciador = GerenciadorSQLAutomatizado(table_name="Disciplina", db_name="db_disciplina.sqlite", prompt=PROMPT_SQL_DISCIPLINA, temperature=0)
        gerenciador.save_data(disciplinas)
        return gerenciador.get_data("disciplina", query)
    
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]