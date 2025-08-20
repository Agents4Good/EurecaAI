from .read_pdf import ler_pdf
from .read_img import ler_imagens
from langchain_core.messages import HumanMessage

def realizar_tratamento_dos_arquivos(arquivos):
    messages = []
    
    pdfs = [arquivo for arquivo in arquivos if arquivo["filename"].lower().endswith(".pdf")]
    if len(pdfs) > 0:
        texto_pdf = ler_pdf(pdfs)
        if texto_pdf.strip():
            messages.append(f"O PDF enviado tem o seguinte texto: {texto_pdf}")

    imagens_dataurls = ler_imagens([arquivo for arquivo in arquivos if arquivo["filename"].lower().endswith((".jpg", ".jpeg", ".png"))])
    
    if imagens_dataurls is not None:
        messages.append(imagens_dataurls)

    return messages