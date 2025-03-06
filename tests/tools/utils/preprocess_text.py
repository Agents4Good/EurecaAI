
import os
import json
import difflib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script atual
path = os.path.join(BASE_DIR, "..", "utils", "siglas.json")  # Caminho relativo

def get_most_similar_acronym(sigla: str, context: str):
    """
        Função que utiliza difflib para encontrar a sigla mais similar à sigla informada.

        Args:
            sigla: sigla desejada.
            context: Contexto da sigla, pode ser disciplina, curso etc. Por exemplo se o contexto informado for 'disciplina' então as siglas a serem consideradas serão as siglas das disciplinas que estão no arquivo json siglas.
        
        Returns:
            String vazia (caso ocorra algum problema) ou nome por extenso da sigla mais próxima à desejada. Ex: se for 'fm cc 2', a função retornará 'fundamentos de matemática para ciência da computação 2'.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            dados = json.load(file)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return ""
    
    if not dados:
        print("JSON não apresenta dados")
        return ""

    if context not in dados:
        print(f"Contexto '{context}' não encontrado no JSON.")
        return ""

    sigla = sigla.upper().strip()
    lista_siglas = list(dados[context].keys())

    most_similar = difflib.get_close_matches(sigla, lista_siglas, n=1, cutoff=0.3)

    return dados[context][most_similar[0]] if most_similar[0] else ""

#print(get_most_similar_acronym("fm cc 2", "disciplina"))






