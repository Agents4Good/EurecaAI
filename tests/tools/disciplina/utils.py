from typing import Any

import json
import requests
from ..utils.preprocess_text import get_most_similar_acronym
from ..utils.most_similar import get_most_similar
from ..utils.processar_json import processar_json
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso
from langchain_community.chat_models import ChatDeepInfra
from ..utils.validacoes import valida_periodo_curriculo
from ..utils.base_url import URL_BASE
from ..curso.utils import get_curso_most_similar
from flask_app.utils.langchain_models import model


mapper = {"nome": "nome", "codigo": "codigo_da_disciplina"}
format = """{'disciplina': {'codigo': '', 'nome_da_disciplina': ''}}"""

def get_disciplina_grade_most_similar(nome_do_campus: Any, nome_do_curso: Any, nome_da_disciplina: Any, curriculo: Any) -> dict:
    """
    Buscar o nome e o código de uma disciplina da grade do curso.

    Args:
        nome_do_campus: nome do campus.
        nome_do_curso: nome do curso.
        nome_da_disciplina: nome da disciplina.
        curriculo: valor inteiro do ano.

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """

    print(f"get_disciplina_grade_most_similar chamada com campus={nome_do_campus}, nome_do_curso={nome_do_curso}, nome_da_disciplina={nome_da_disciplina} e curriculo={curriculo} chamada.")
    nome_do_curso = str(nome_do_curso)
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        curriculo = curriculo['codigo_do_curriculo']
        print(f"curriculo que será usado: {curriculo}")
    
    else:
        curriculos = get_todos_curriculos_do_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{ "error_status": "500", "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis} e que o curriculo mais recente é o de {todos_curriculos_disponiveis[-1]}." }], "ocorreu um erro"

    todas_disciplinas_curso = get_todas_disciplinas(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    print("todas as disciplinas do curso foram recuperadas")
    disciplinas_most_similar, top_k = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.5) # disciplina mais similar
    print("\n\n\n\n\n", disciplinas_most_similar, top_k, "\n\n\n\n")

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        As possíveis disciplinas são: {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome_da_disciplina).
        """
    )
    
    result = processar_json(response.content, "disciplina")
    print(f"Disciplina mais similar encontrada: {result} para o curriculo de {curriculo}.")
    return result, curriculo


def get_disciplina_grade_most_similar_por_codigo_do_curso(codigo_do_curso: Any, nome_da_disciplina: Any, curriculo: Any) -> dict:
    """
    Buscar o nome e o código de uma disciplina da grade do curso.
    Use quando tiver certeza do curriculo do curso para recuperar as disciplinas do curriculo.

    Args:
        codigo_do_curso: código do curso.
        nome_da_disciplina: nome da disciplina.
        curriculo: valor inteiro do ano.

    Returns:
        dict: dicionário contendo o nome e código da disciplina ou uma mensagem de erro.
    """

    print(f"get_disciplina_grade_most_similar_por_codigo_do_curso chamada com codigo_do_curso={codigo_do_curso}, nome_da_disciplina={nome_da_disciplina} e curriculo={curriculo} chamada.")
    nome_da_disciplina = get_most_similar_acronym(str(nome_da_disciplina), "disciplina")
    codigo_do_curso = str(codigo_do_curso)
    curriculo = str(curriculo)
    
    todas_disciplinas_curso = get_disciplinas_por_codigo(codigo_do_curso=codigo_do_curso, curriculo=curriculo)
    print("todas as disciplinas do curso foram recuperadas")
    disciplinas_most_similar, top_k = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.35)
    print("\n\n\n\n\n", disciplinas_most_similar, top_k, "\n\n\n\n")

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        As possíveis disciplinas são: {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome_da_disciplina).
        """
    )

    result = processar_json(response.content, "disciplina")
    print(f"Disciplina mais similar encontrada: {result} para o curriculo de {curriculo}.")
    return result, curriculo

def get_todas_disciplinas(nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    print(f"Tool `get_disciplinas` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if curriculo == "":
        dados_curso, curriculo, _, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, periodo="", curriculo=curriculo)
        if mensagem != "": return mensagem
    else:
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)

    
    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo
    }

    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        print("Disciplinas recuperadas com sucesso")
        disciplinas = json.loads(response.text)
        return disciplinas
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]
    

def get_disciplinas_por_codigo(codigo_do_curso: Any, curriculo: Any = "") -> list:
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
        codigo_do_curso (Any): codigo do curso.
        curriculo (Any, optional): (Opcional) Ano do currículo ("" usa o mais recente). Defaults to "".

    Returns:
        list: Uma lista com informações relevantes sobre a pergunta a respeito da(s) disciplina(s).
    """
    
    codigo_do_curso = str(codigo_do_curso)    
    curriculo = str(curriculo)
    print(f"Tool `get_disciplinas` chamada com codigo_do_curso={codigo_do_curso} e codigo_curriculo={curriculo}.")

    params = {
        'curso': codigo_do_curso,
        'curriculo': curriculo
    }

    print(f"Recuperando as disciplinas do curso do curso de codigo {codigo_do_curso} com o curriculo de {curriculo}")
    
    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]