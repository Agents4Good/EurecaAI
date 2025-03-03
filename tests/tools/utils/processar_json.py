import json

def processar_json(json_str: str, tipo: str):
    try:
        result = json.loads(json_str.replace("'", '"'))
        if tipo not in result or not isinstance(result[tipo], dict):
            return "Erro: Estrutura do JSON inválida. A chave tipo deve ser um dicionário."
        if 'codigo' not in result[tipo] or not result[tipo]['codigo']:
            return "Erro: O campo 'codigo' está ausente ou vazio."
        '''if 'nome' not in result[tipo] or not result[tipo]['nome']:
            return "Erro: O campo 'nome' está ausente ou vazio."'''
        return result
    except json.JSONDecodeError:
        raise ValueError("Erro: A string fornecida não é um JSON válido.")