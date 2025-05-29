from typing import Any
from .get_todos_setores import get_todos_setores, get_todos_setores_por_codigo_do_campus
from ..utils.most_similar import get_most_similar
from langchain_ollama import ChatOllama
from ..utils.processar_json import processar_json
from langchain_community.chat_models import ChatDeepInfra

model = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
format = """{'setor': {'codigo': '', 'nome': ''}}"""
mapper_setor = {"nome": "descricao", "codigo": "codigo_do_setor"}

def get_setor_most_similar(nome_do_centro_setor: str, nome_do_campus: str, filtro: str = "") -> dict:
    """
    Busca o código do setor pelo nome dele.

    Args:
        nome_do_centro_setor: nome do setor.
        nome_do_campus: O parâmetro nome_do_campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se o campus não foi informado, retorne uma mensagem de erro pois, precisa do campus).
        filtro: usar 'UNID' ou 'CENTRO'. (se não foi informado, ou se perguntar pelo setor, então use a string vazia '').

    Returns:
        dict: dicionário contendo código e o nome do setor.
    """
    print(f"`get_setor_most_similar` chamado com nome_do_centro_setor={nome_do_centro_setor}, nome_do_campus={nome_do_campus}, filtro={filtro}")
    
    setores_campus = get_todos_setores(nome_do_campus=nome_do_campus, filtro="UNID")
    setores_filtrados = [setor for setor in setores_campus if filtro.lower() in setor["descricao"].lower()]
    setor_most_similar, _ = get_most_similar(lista_a_comparar=setores_filtrados, dado_comparado=nome_do_centro_setor, top_k=5, mapper=mapper_setor, limiar=0.65)
    
    response = model.invoke(
        f"""
        Para o setor de nome: '{nome_do_centro_setor}', quais desses possíveis cursos abaixo é mais similar ao campus do nome informado?
        
        {setor_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response.content, "setor")



def get_setor_most_similar_por_codigo(nome_do_centro_setor: str, codigo_do_campus: str, filtro: str = "") -> dict:
    """
    Busca o código do setor pelo nome dele.

    Args:
        nome_do_centro_setor: nome do setor.
        codigo_do_campus: código do campus(se o campus não foi informado, retorne uma mensagem de erro pois, precisa do campus).
        filtro: usar 'UNID' ou 'CENTRO'. (se não foi informado, ou se perguntar pelo setor, então use a string vazia '').

    Returns:
        dict: dicionário contendo código e o nome do setor.
    """
    print(f"`get_setor_most_similar_por_codigo_do_campus` chamado com nome_do_centro_setor={nome_do_centro_setor}, codigo_do_campus={codigo_do_campus}, filtro={filtro}")
    
    setores_campus = get_todos_setores_por_codigo_do_campus(codigo_do_campus=codigo_do_campus, filtro="UNID")
    setores_filtrados = [setor for setor in setores_campus if filtro.lower() in setor["descricao"].lower()]
    setor_most_similar, _ = get_most_similar(lista_a_comparar=setores_filtrados, dado_comparado=nome_do_centro_setor, top_k=5, mapper=mapper_setor, limiar=0.65)
    
    response = model.invoke(
        f"""
        Para o setor de nome: '{nome_do_centro_setor}', quais desses possíveis cursos abaixo é mais similar ao campus do nome informado?
        
        {setor_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response.content, "setor")