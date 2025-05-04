import json
import requests
from typing import Any
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from .disciplina_utils.disciplina.prompt_disciplina import PROMPT_SQL_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from langchain_core.tools import tool
from ..utils.validacoes import validar_curriculo

def get_disciplinas(query: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """_summary_
    Retorna as disciplinas ofertadas por um curso.
    
    Use esta função quando a pergunta envolver:
    - código, nome, créditos ou carga horária da disciplina;
    - carga teórica/prática semanal ou total;
    - número de semanas de aula;
    - nome do setor responsável e campus;
    - carga de extensão ou contabilização de créditos.
    
    Chame esta função se a pergunta for sobre as disciplinas que o curso oferece.
    
    Args:
        query (Any): a pergunta feita.
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        curriculo (Any, optional): (Opcional) Ano do currículo ("" usa o mais recente). Defaults to "".

    Returns:
        list: Uma lista com informações relevantes.
    """
    
    query=str(query)
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
    else:
        validado, mensagem = validar_curriculo(curriculo_usado=curriculo, nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        if not validado: return mensagem
    
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)

    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo
    }
    
    print(f"Recuperando as disciplinas do curso de {dados_curso['curso']['nome']} e código {dados_curso['curso']['codigo']} e currículo {curriculo}")
    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        print("Disciplinas recuperadas com sucesso")
        disciplinas = json.loads(response.text)
        if query == "":
            return disciplinas
        gerenciador = GerenciadorSQLAutomatizado(table_name="Disciplina", db_name="db_disciplina.sqlite")
        gerenciador.save_data(disciplinas)
        return gerenciador.get_data(query, PROMPT_SQL_DISCIPLINA, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]