import base64
from langchain_core.messages import HumanMessage

def ler_imagens(arquivos):
    """
    Lê imagens do caminho especificado e retorna seu conteúdo codificado em base64.
    
    Args:
        image_path (str): Caminho para o arquivo da imagem.
        
    Returns:
        str: String base64 da imagem.
    """
    mensagens = [{"type": "text", "text": "Temos as seguintes imagens"}]

    for arquivo in arquivos:
        image_bytes = arquivo.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        mensagens.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}})

    
    return HumanMessage(content=mensagens) if len(mensagens) > 0 else None