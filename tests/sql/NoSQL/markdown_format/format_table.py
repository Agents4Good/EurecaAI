def format_md(resultado_lista: list) -> str:
    if not resultado_lista:
        return "Nenhum dado disponível."
    
    colunas = resultado_lista[0].get("colunas", [])
    data = [doc.get("dados", []) for doc in resultado_lista]
    
    output = f"<h1>DADOS RECUPERADOS:</h1>\n\n"
    output += "| " + " | ".join(colunas) + " |\n"
    output += "| " + " | ".join(["----"] * len(colunas)) + " |\n"
    for i, dt in enumerate(data):
        output += "| " + " | ".join(map(str, dt)) + " |"
        if i != len(data) - 1:
            output += "\n"
    
    return output