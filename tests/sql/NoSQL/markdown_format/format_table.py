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


def format_md_grafico_pizza(resultado_listas, titulo="Gráfico de Pizza Gerado"):
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
                    "display": 'true',
                    "text": titulo
                }
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}"

    return f"Link do gráfico gerado a seguir (devolva o link neste exato formato): ![{titulo}]({chart_url})"


def format_md_grafico_barra(resultado_listas, titulo="Gráfico de Barras Gerado"):
    labels, valores = carregar_dados(resultado_listas=resultado_listas)

    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Quantidade",
                    "data": valores
                }
            ]
        },
        "options": {
            "title": {
                "display": "true",
                "text": titulo,
                "fontSize": 8  # Tamanho da fonte do título
            },
             "legend": {
                "labels": {
                    "fontSize": 7  # Tamanho da fonte da legenda
                }
            },
            "scales": {
                "xAxes": [{
                    "ticks": {
                        "fontSize": 7  # Tamanho da fonte no eixo X
                    }
                }],
                "yAxes": [{
                    "ticks": {
                        "fontSize": 7  # Tamanho da fonte no eixo Y
                    }
                }]
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}&width=400&height=200"

    return f"Link do gráfico gerado a seguir (devolva o link neste exato formato): ![{titulo}]({chart_url})"


def format_md_grafico_doughnut(resultado_listas, titulo="Gráfico de Rosquinha Gerado"):
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
                    "display": 'true',
                    "text": titulo
                }
            }
        }
    }

    base_url = "https://quickchart.io/chart"
    chart_param = urllib.parse.quote(str(chart_config).replace("'", '"'))
    chart_url = f"{base_url}?c={chart_param}"

    return f"Link do gráfico gerado a seguir (devolva o link neste exato formato): ![{titulo}]({chart_url})"


def carregar_dados(resultado_listas: list):
    labels = []
    valores = []

    for item in resultado_listas:
        if len(item) != 2:
            raise ValueError("Para usar esse gráfico deve haver apenas array de arrays de tamanho 2. Por favor, use a ferramenta de tabela para esse propósito.")

        if isinstance(item[0], (int, float)) and isinstance(item[1], str) or item[1] is None:
            valores.append(item[0])
            labels.append(item[1]) if item[1] is not None else labels.append("Outros")
        elif isinstance(item[1], (int, float)) and isinstance(item[0], str) or item[0] is None:
            valores.append(item[1])
            labels.append(item[0]) if item[0] is not None else labels.append("Outros")
        else:
            raise ValueError("Os dados devem ser pares de valores string e inteiros. Por favor, use a ferramenta de tabela para esse propósito.")

    if not labels or not valores or len(labels) != len(valores):
        raise ValueError("Dados inválidos para gerar gráfico de pizza.")
    
    return labels, valores

print(format_md_grafico_pizza([(None, 16), ('AL', 2), ('BA', 2), ('CE', 5), ('DF', 2), ('GO', 1), ('PB', 344), ('PE', 26), ('PI', 7), ('RJ', 8), ('RN', 14), ('SP', 15)]))