from ..utils.most_similar import get_most_similar
from .get_campi import get_campi
from langchain_ollama import ChatOllama
from ..utils.processar_json import processar_json

model = ChatOllama(model="llama3.1", temperature=0)
format = """{'campus': {'codigo': '', 'nome': ''}}"""
mapper_campus = {"nome": "descricao", "codigo": "campus"}

def get_campus_most_similar(nome_do_campus: str) -> dict:
    """
    Busca os dados do campus interessado. Os dados contém o nome e o código do campus.

    Args:
        campus: nome do campus interessado.

    Returns:
        Retorna os dados de apenas um campus com seu nome e codigo.
    """
    
    campi = get_campi()
    campus_most_similar, _ = get_most_similar(lista_a_comparar=campi, dado_comparado=nome_do_campus, top_k=3, mapper=mapper_campus, limiar=0.65)

    if len(campus_most_similar) == 0:
        raise ValueError("Campus não encontrado")
    
    response = model.invoke(
        f"""
        Para o campus de nome: '{nome_do_campus}', quais desses possíveis campus abaixo é mais similar ao campus do nome informado?
        
        {campus_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    #print("\n\n", processar_json(response.content, "campus"))
    return processar_json(response.content, "campus")