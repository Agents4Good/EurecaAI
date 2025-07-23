from langchain_core.messages import HumanMessage

def ler_imagens(arquivos):
    mensagens = [{"type": "text", "text": "Temos as seguintes imagens"}]

    for img in arquivos:
        try:
            filename = img.get("filename", "desconhecido.png")
            b64_data = img.get("content", "")

            if not b64_data.strip():
                continue

            mensagens.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64_data}"}
            })
        except Exception as e:
            print(f"Erro ao processar imagem {filename}: {e}")

    return HumanMessage(content=mensagens) if len(mensagens) > 1 else None
