import re
from typing import Any, Tuple
from .connection_nosql import get_mongo_collection
from .markdown_format.format_table import format_md_table

def save_data(id: Any, colecao: Any, sql: Any, data: Any) -> Tuple[str, bool]:
    id = str(id)
    sql = str(sql).lower()
    data = list(data)
    colecao = str(colecao)
    
    colunas = re.search(r"select\s+(.*?)\s+from", sql, re.IGNORECASE)
    if colunas:
         colunas = [c.strip() for c in colunas.group(1).split(",")]
         if colunas[0] == "*": 
            colunas = ""
    else:
        return "Erro: não foi possível extrair colunas da SQL.", False
    
    colecao_db = get_mongo_collection(id, colecao)
    documento = {
        "colunas": colunas,
        "dados": data
    }
    
    colecao_db.insert_one(documento)
    
    skip = 0
    limit = 50
    resultados = colecao_db.find().skip(skip).limit(limit)    
    resultados_lista = list(resultados)
    output = format_md_table(resultado_lista=resultados_lista)
    
    total = colecao_db.count_documents({})
    has_more = total > 50
    return output, has_more


def recovery_data(id: Any, colecao: Any, page: Any, limit: Any) -> Tuple[str, bool]:
    """_summary_
    Recupera informações que estão no banco de dados.

    Args:
        colecao (str): Nome da coleção no MongoDB.
        id (str): ID onde os dados estão persistidos.
        page (int): Número da página.
        limit (int): Tamanho dos dados retornados.

    Returns:
        str: Retorna os dados formatados em markdown para o usuário.
    """
    
    id = str(id)
    page = int(page)
    limit = int(limit)
    colecao = str(colecao)
    
    colecao_db = get_mongo_collection(id, colecao)
    skip = (page - 1) * limit
    resultados = colecao_db.find().skip(skip).limit(limit)
    resultado_lista = list(resultados)
    
    
    if len(resultado_lista) == 0:
        return "Você já recebeu todos os dados, não há mais.", False
    
    
    output = format_md_table(resultado_lista=resultado_lista)
    total_docs = colecao_db.count_documents({})
    total_pages = (total_docs + limit - 1) // limit
    has_more = page < total_pages
    
    return output, has_more

print(save_data("10", "estudante", "SELECT NOME FROM ESTUDANTE", [["Nome1"], ["Nome2"]]))