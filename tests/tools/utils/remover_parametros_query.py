
import re
import inspect
import unicodedata

def normalizar_texto(texto: str) -> str:
    """
    Remove acentos e converte para minúsculas.
    """
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8').casefold()

def remover_parametros_da_query(query: str, excluir: list[str] = None) -> str:
    """
    Remove da query os parâmetros fornecidos na função chamadora.
    """
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)

    parametros = {arg: values[arg] for arg in args if arg != 'query' and arg != 'self'}
    if excluir:
        for chave in excluir:
            parametros.pop(chave, None)

    termos_para_remover = [str(v) for v in parametros.values() if v]

    query_normalizada = normalizar_texto(query)
    termos_normalizados = [normalizar_texto(termo) for termo in termos_para_remover]

    for termo in termos_normalizados:
        if termo in query_normalizada:
            query_normalizada = query_normalizada.replace(termo, '')

    return query_normalizada.strip()

