from typing import Any
from ..utils.preprocess_text import get_most_similar_acronym
from ..utils.most_similar import get_most_similar
from .get_todas_disciplinas import get_todas_disciplinas
from ..utils.processar_json import processar_json
from langchain_ollama import ChatOllama
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.get_todos_curriculos_curso import get_curriculos

model = ChatOllama(model="llama3.1", temperature=0)
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
    
    nome_da_disciplina = get_most_similar_acronym(str(nome_da_disciplina), "disciplina")
    nome_do_curso = str(nome_do_curso)
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        curriculo = curriculo['codigo_do_curriculo']
    else:
        curriculos = get_curriculos(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{ "error_status": "500", "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis}" }], "ocorreu um erro"

    todas_disciplinas_curso = get_todas_disciplinas(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    disciplinas_most_similar, _ = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.65)
    print(disciplinas_most_similar)
    
    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        As possíveis disciplinas são: {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome_da_disciplina).
        """
    )
    
    print(response.content)
    return processar_json(response.content, "disciplina"), curriculo