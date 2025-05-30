import requests
import json

URL_BASE = "https://eureca.lsd.ufcg.edu.br/das/v2"

def teste():
    status = ["SUSPENSOS", "REINGRESSOS", "REATIVADOS", "DESISTENTES", "EVADIDOS", "JUBILADOS", "ABANDONOS", "TRANSFERIDOS", "FINALIZADOS", "INATIVOS", "EGRESSOS", "ATIVOS"]
    tipos_status = {tipo: [] for tipo in status}

    for tipo in tipos_status:
        params = {
            "situacao-do-estudante": tipo,
            "curso": 14102100
        }
        try:
            dados = requests.get(f"{URL_BASE}/estudantes", params=params)
            if dados.status_code == 200:
                dados_json = dados.json()
                tipos_status[tipo] = list(set(x.get("motivo_de_evasao") for x in dados_json if x.get("motivo_de_evasao")))
            else:
                print(f"Erro ao buscar dados para status {tipo}: {dados.status_code}")
        except Exception as e:
            print(f"Erro ao requisitar dados para status {tipo}: {e}")
    
    for tipo in tipos_status:
        print(f"""\n\n{tipo}:\n\n{tipos_status[tipo]}\n{len(tipos_status[tipo])}\n\n""")
    
    tot = ""
    for tipo in tipos_status:
        tot += f""""{tipo}" quando for para {'", "'.join(tipos_status[tipo])}"""
    print(tot)

teste()
