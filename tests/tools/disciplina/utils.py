from typing import Any
from ..utils.preprocess_text import remove_siglas
from ..utils.most_similar import get_most_similar
from .get_todas_disciplinas_curso import get_todas_disciplinas_curso
from .get_todas_disciplinas_grade import get_todas_disciplinas_grade
from ..utils.processar_json import processar_json
from langchain_ollama import ChatOllama
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.get_todos_curriculos_curso import get_todos_curriculos_curso

model = ChatOllama(model="llama3.2:3b", temperature=0)
format = """{'disciplina': {'codigo': '', 'nome': ''}}"""
mapper = {"nome": "nome", "codigo": "codigo_da_disciplina"}

def get_disciplina_most_similar(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> tuple:
    """
    Buscar o nome e o código de uma unica disciplina.

    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        dict: dicionário contendo o nome e código da disciplina.
    """
    
    nome_da_disciplina = remove_siglas(str(nome_da_disciplina)).lower()
    nome_do_curso = str(nome_do_curso)
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    
    print(f"Tool get_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e curriculo={curriculo}")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        curriculo = curriculo['codigo_do_curriculo']
    else:
        curriculos = get_todos_curriculos_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{ "error_status": "500", "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis}" }]
        
    todas_disciplinas_curso = get_todas_disciplinas_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    disciplinas_most_similar, _ = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.65)

    response = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response.content, "disciplina"), curriculo



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
    
    nome_da_disciplina = remove_siglas(str(nome_da_disciplina)).lower()
    nome_do_curso = str(nome_do_curso)
    nome_do_campus = str(nome_do_campus)
    curriculo = str(curriculo)
    
    print(f"Tool get_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e curriculo={curriculo}")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        curriculo = curriculo['codigo_do_curriculo']
    else:
        curriculos = get_todos_curriculos_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
        
        existe_curriculo = False
        todos_curriculos_disponiveis = []
        
        for curriculo_dict_i in curriculos:
            curriculo_i = curriculo_dict_i['codigo_do_curriculo']
            todos_curriculos_disponiveis.append(curriculo_i)
            
            if curriculo_i == int(curriculo):
                existe_curriculo = True
        
        if not existe_curriculo:
            return [{ "error_status": "500", "msg": f"Informe ao usuário que este curriculo é inválido e que os disponíveis são: {todos_curriculos_disponiveis}" }]
        
    print(curriculo)
    todas_disciplinas_curso = get_todas_disciplinas_grade(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    print(todas_disciplinas_curso)
    disciplinas_most_similar, _ = get_most_similar(lista_a_comparar=todas_disciplinas_curso, dado_comparado=nome_da_disciplina, top_k=5, mapper=mapper, limiar=0.65)
    print(disciplinas_most_similar)
    
    response_ = model.invoke(
        f"""
        Para a disciplina de nome: '{nome_da_disciplina}', quais dessas possíveis disciplinas abaixo é mais similar a disciplina do nome informado?

        {disciplinas_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response_.content, "disciplina"), curriculo