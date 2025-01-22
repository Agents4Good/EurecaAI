from langchain_core.tools import tool

tags = ["<MATRICULA>", "<CPF>", "<EMAIL_ADDRESS>", "PHONE_NUMBER", "URL"]

@tool
def detect(texto: str) -> bool:
    """
    Detectar se o texto recebido possui <tags>.

    Args:
        query: texto recebido na entrada referente à consulta do usuário.
    
    Returns:
        Bool indicando se o texto possui <tags> ou não.
    """
    return any(tag in texto for tag in tags)