import json
import requests
from typing import Any
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from ...sql.Disciplina.prompt import PROMPT_SQL_DISCIPLINA
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ..utils.validacoes import valida_periodo_curriculo

def get_disciplinas(query: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    """_summary_
    Informações de todas as disciplinas de um curso.
    
    Use esta função quando a pergunta envolver:
    - código, nome, créditos ou carga horária da disciplina;
    - carga teórica/prática semanal ou total;
    - número de semanas de aula;
    - nome do setor responsável e campus;
    - carga de extensão ou contabilização de créditos.
    
    Chame esta função se a pergunta for sobre as disciplinas que o curso oferece.
    
    Args:
        query (Any): reformule a pergunta removendo qualquer referência ao nome do curso, nome do campus e ao currículo (ano).
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        curriculo (Any, optional): (Opcional) Ano do currículo ("" usa o mais recente). Defaults to "".

    Returns:
        list: Uma lista com informações relevantes sobre a pergunta a respeito da(s) disciplina(s).
    """
    
    query=str(query)
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    print(f"Tool `get_disciplinas` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if curriculo == "":
        _, curriculo, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, periodo="", curriculo=curriculo)
        if mensagem != "": return mensagem
    
    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)

    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo
    }

    print("CURRICULO USADO ", curriculo)
    
    print(f"Recuperando as disciplinas do curso de {dados_curso['curso']['nome']} e código {dados_curso['curso']['codigo']} e currículo {curriculo}")
    print(params)
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
        return [{"error_status": response.status_code, "msg": response.json()}]