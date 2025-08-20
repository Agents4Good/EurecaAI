from typing import Any
from ..utils.preprocess_text import get_most_similar_acronym
from ..utils.most_similar import get_most_similar
from .get_disciplinas import get_disciplinas, get_disciplinas_por_codigo
from ..utils.processar_json import processar_json
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso
from application.config import model


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
    nome_da_disciplina = get_most_similar_acronym(str(nome_da_disciplina), "disciplina")
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

    todas_disciplinas_curso = get_disciplinas("", nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    print("todas as disciplinas do curso foram recuperadas")
    disciplinas_most_similar, top_k = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.65)
    print("\n\n\n\n\n", disciplinas_most_similar, top_k, "\n\n\n\n")

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        As possíveis disciplinas são: {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome_da_disciplina).
        Se o nome da disciplina em questão for **idêntico** a umas das possíveis disciplinas, então é óbvio que a resposta é essa disciplina idêntica.
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
    print("AAAAAAAAAAAAAAAH: ", response.content)
    result = processar_json(response.content, "disciplina")
    print(f"Disciplina mais similar encontrada: {result} para o curriculo de {curriculo}.")
    return result, curriculo