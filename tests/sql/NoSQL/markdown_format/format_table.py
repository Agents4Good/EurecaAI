import urllib.parse


def format_md_table(resultado_lista: list) -> str:
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


def format_md_grafico_pizza(resultado_listas, titulo="Gráfico de Pizza"):
    labels, valores = carregar_dados(resultado_listas=resultado_listas)

    chart_config = {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": valores
            }]
        },
        "options": {
            "plugins": {
                "title": {
                    "display": True,
                    "text": titulo
                }
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}"

    return f"![{titulo}]({chart_url})"


def format_md_grafico_barra(resultado_listas, titulo="Gráfico de Barras"):
    labels, valores = carregar_dados(resultado_listas=resultado_listas)

    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": valores
        },
        "options": {
            "plugins": {
                "title": {
                    "display": True,
                    "text": titulo
                }
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}"

    return f"![{titulo}]({chart_url})"


def format_md_grafico_doughnut(resultado_listas, titulo="Gráfico de Rosquinha"):
    labels, valores = carregar_dados(resultado_listas=resultado_listas)
    total = sum(valores)
    
    chart_config = {
        "type": "doughnut",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": valores
            }]
        },
        "options": {
            "plugins": {
                "doughnutlabel": {
                    "labels": [
                        {"text": str(total), "font": {"size": 20}},
                        {"text": "total"}
                    ]
                },
                "title": {
                    "display": True,
                    "text": titulo
                }
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}"

    return f"![{titulo}]({chart_url})"


def carregar_dados(resultado_listas: list):
    labels = []
    valores = []

    for item in resultado_listas:
        if len(item) != 2:
            raise ValueError("Para usar esse gráfico deve haver apenas array de arrays de tamanho 2. Por favor, use a ferramenta de tabela para esse propósito.")

        if isinstance(item[0], (int, float)) and isinstance(item[1], str):
            valores.append(item[0])
            labels.append(item[1])
        elif isinstance(item[1], (int, float)) and isinstance(item[0], str):
            valores.append(item[1])
            labels.append(item[0])
        else:
            raise ValueError("Os dados devem ser pares de valores string e inteiros. Por favor, use a ferramenta de tabela para esse propósito.")

    if not labels or not valores or len(labels) != len(valores):
        raise ValueError("Dados inválidos para gerar gráfico de pizza.")
    
    return labels, valores