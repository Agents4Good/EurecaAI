
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script atual
path = os.path.join(BASE_DIR, "..", "utils", "siglas.json")  # Caminho relativo

def remove_siglas(texto: str):
    """
    Remove siglas de uma palavra ou frase
    """
    with open(path, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    
    substituicoes = {**dados["disciplina"], **dados["curso"]}
    palavras = texto.split()
    palavras_modificadas = [substituicoes.get(palavra.upper(), palavra) for palavra in palavras]
    
    return " ".join(palavras_modificadas)