import fitz
from langchain_core.documents import Document

def ler_pdf(pdfs):
    documentos_processados = [] 
    
    for pdf in pdfs:
        if pdf.filename.lower().endswith(".pdf"):
            pdf_bytes = pdf.read()
            doc = fitz.open(stream = pdf_bytes, filetype="pdf")
            
            for i, page in enumerate(doc):
                text = page.get_text("text").strip()
                if text:
                    documentos_processados.append(Document(
                        page_content=text,
                        metadata={"page": i + 1, "filename": pdf.filename}
                    ))
                    
        else:
            print(f"Arquivo {pdf.filename} não é um pdf.")
    
    return "\n\n".join([f"[{doc.metadata['filename']} - Página {doc.metadata['page']}]\n{doc.page_content}" for doc in documentos_processados])