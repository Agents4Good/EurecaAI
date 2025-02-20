import os
path = os.path.join(os.getcwd(), "utils","siglas.json")

import json

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
