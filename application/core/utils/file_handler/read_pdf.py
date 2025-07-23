import base64
import fitz
from langchain_core.documents import Document

def ler_pdf(pdfs_b64):
    documentos_processados = []

    for pdf in pdfs_b64:
        filename = pdf.get("filename", "desconhecido.pdf")
        b64_data = pdf.get("content", "")

        try:
            pdf_bytes = base64.b64decode(b64_data)
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            for i, page in enumerate(doc):
                text = page.get_text("text").strip()
                if text:
                    documentos_processados.append(Document(
                        page_content=text,
                        metadata={"page": i + 1, "filename": filename}
                    ))

        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")

    return "\n\n".join([
        f"[{doc.metadata['filename']} - Página {doc.metadata['page']}]\n{doc.page_content}"
        for doc in documentos_processados
    ])
