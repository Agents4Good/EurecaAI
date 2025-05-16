
import re

from sentence_transformers import SentenceTransformer, util

def limpar_query(query: str, termos_a_remover: list[str]) -> str:
    """
    Remove múltiplos termos da query, considerando preposições comuns antes deles.
    
    Args:
        query (str): Texto original da query.
        termos_a_remover (list[str]): Lista de termos que devem ser removidos da query.
        
    Returns:
        str: Query limpa, sem os termos indicados.
    """
    resultado = query
    
    for termo in termos_a_remover:
        if termo:
            # Expressão para remover o termo com preposições comuns antes
            pattern = r'(\bdo\b|\bda\b|\bde\b|\bno\b|\bna\b|\bem\b)?\s*' + re.escape(termo) + r'\b'
            resultado = re.sub(pattern, '', resultado, flags=re.IGNORECASE)
    
    # Limpar espaços duplicados e pontuação solta no fim
    resultado = re.sub(r'\s{2,}', ' ', resultado).strip()
    resultado = resultado.strip(' ,.?')
    return resultado

