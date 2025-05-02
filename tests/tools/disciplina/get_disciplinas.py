import json
import requests
from typing import Any
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from .disciplina_utils.disciplina.prompt_disciplina import PROMPT_SQL_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from langchain_core.tools import tool

def get_disciplinas(query: Any, nome_do_curso: Any, nome_do_campus: Any, codigo_disciplina: Any = "", curriculo: Any = "") -> list:
    """
    Retorna as disciplinas ofertadas por um curso.

    Use esta função quando a pergunta envolver:
    - código, nome, créditos ou carga horária da disciplina;
    - carga teórica/prática semanal ou total;
    - número de semanas de aula;
    - setor responsável e campus;
    - carga de extensão ou contabilização de créditos.

    Chame esta função se a pergunta for sobre as disciplinas que o curso oferece.

    Args:
        query: a pergunta feita.
        nome_do_curso: Nome do curso.
        nome_do_campus: Cidade do campus.
        codigo_disciplina: (Opcional) Código da disciplina ("" usa o mais recente).
        curriculo: (Opcional) Ano do currículo ("" usa o mais recente).

    Returns:
        Uma lista com informações relevantes.
    """

    query=str(query)
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    codigo_disciplina=str(codigo_disciplina)
    curriculo = str(curriculo)
    dados_curso = {"curso": {"codigo": codigo_disciplina, "nome": nome_do_curso}}
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
    if codigo_disciplina == "":
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)

    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo
    }
    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        disciplinas = json.loads(response.text)
        if query == "":
            return disciplinas
        gerenciador = GerenciadorSQLAutomatizado(table_name="Disciplina", db_name="db_disciplina.sqlite")
        gerenciador.save_data(disciplinas)
        return gerenciador.get_data(query, PROMPT_SQL_DISCIPLINA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]