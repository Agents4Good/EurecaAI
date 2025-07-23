import json
import os

def get_table_keys(table_name: str) -> list:
    try:
        caminho = f'tests/sql/{table_name}/tabela.json'
        if not os.path.exists(caminho): return []
        
        with open(caminho, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
        
        return list(dados_json.get(table_name, {}).keys())
    
    except Exception:
        return []