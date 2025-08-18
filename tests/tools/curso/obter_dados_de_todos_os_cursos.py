import json
import requests
from typing import Any
from ..campus.utils import get_campus_most_similar
from .utils import get_lista_cursos
from ..utils.base_url import URL_BASE
from ...sql.Curso.prompt import PROMPT_SQL_CURSOS
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.GerenciadorNoSQLAutomatizado import CLIENT_NOSQL
from ...sql.GerenciadorNoSQLAutomatizado import GerenciadorNoSQLAutomatizado

def obter_dados_de_todos_os_cursos(query: Any, nome_do_campus: Any = "") -> list:
    """
    _summary_
    Buscar informações relativo a todos os cursos da UFCG, como código do curso, nome do curso, código do setor, nome do setor, 
    nome do campus, turno do curso, período do de inicio do curso, código inep, modalidade academica (grau do curso), curriculo atual, ciclo enade e data de criação do curso.
    Use esta função quando o usuário fizer uma pergunta **geral** sobre cursos da UFCG, sem mencionar nomes específicos.
    
    Exemplos de uso:
        - "Quantos cursos são oferecidos em Patos?"
        - "Quais cursos são noturnos em Cajazeiras?"
        - "Quantos cursos de graduação existem?"
        - "Quantos cursos de graduação existem em Sousa?"
    
    Args:
        query: pergunta completa feita pelo usuário.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.
    
    Returns:
        Informações que ajude a responder a pergunta feita pelo usuário.
    """

    query=str(query)
    nome_do_campus=str(nome_do_campus)
    print(f"Tool `obter_dados_de_todos_os_cursos` chamada com nome_do_campus={nome_do_campus}")  

    try:
        cursos = get_lista_cursos(nome_do_campus)
        cursos = [
            {**{('nome_do_curso' if k == 'descricao' else k): v for k, v in c.items()}}
            for c in cursos
        ]
        #gerenciador = GerenciadorSQLAutomatizado("Curso", "db_cursos.sqlite")
        
        PROMPT_SQL_CURSOS = """
        Você é um especialista em MongoDB.
        Dado o significado dos campos abaixo e uma pergunta do usuário, gere uma **consulta MongoDB em Python** usando PyMongo.

        Campos disponíveis:
        {format}

        Pergunta do usuário:
        {input}

        Responda com um único dicionário Python contendo **dois campos obrigatórios**:
        - "filter": contendo o critério de filtro da consulta.
        - "projection": contendo apenas os campos necessários para responder à pergunta. Exclua o campo "_id", a menos que ele seja explicitamente solicitado.

        Nunca retorne todos os campos na projeção.

        Responda apenas com o dicionário que representa a consulta MongoDB e sem aspas.
        """
        
        PROMPT_SQL_CURSOS = """
        Você é um especialista em pandas.
        Com base na estrutura abaixo e na pergunta do usuário, gere uma expressão pandas válida para filtrar um DataFrame chamado df.

        Estrutura do DataFrame:
        {format}

        Pergunta do usuário:
        {input}

        Retorne apenas o código pandas no seguinte formato:
            df[<condição>][[<colunas>]]

        Não adicione comentários, nem texto adicional.
        Sempre selecione apenas as colunas pedidas na pergunta para responder. 

        Raciocine sobre a pergunta do usuário e use os campos disponíveis para construir a consulta.
        """

        gerenciador = GerenciadorNoSQLAutomatizado(
            db=CLIENT_NOSQL,
            collection_name="Curso",
            json_data=cursos,
            prompt=PROMPT_SQL_CURSOS,
            temperature=0.6
        )
        #gerenciador.save_data(cursos)
        #return gerenciador.get_data(query, PROMPT_SQL_CURSOS, temperature=0)
        return gerenciador.invoke_pandas(query)
    
    except Exception as e:
        return [{"Error": str(e)}]