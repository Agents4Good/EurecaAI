import json
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def read_json_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '..', 'data', 'examples.json')

    with open(json_path, 'r', encoding='utf-8') as arquivo:
        try:
            data = json.load(arquivo)
            if isinstance(data, dict) and len(data) > 0:
                last_key = list(data.keys())[-1]  
                return last_key
            else:
                return "0"
        except json.JSONDecodeError:
            return "0"


def write_in_json_file(new_data):
    index = read_json_file()[-1:]
    novo_index = f"example_{str(int(index) + 1)}"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '..', 'data', 'examples.json')

    with open(json_path, 'r', encoding='utf-8') as arquivo:
        try:
            data = json.load(arquivo) 
            if not isinstance(data, dict):  
                data = {}
        except json.JSONDecodeError:
                data = {}  

    # Adiciona o novo dado
    data[novo_index] = new_data
    
    with open(json_path, 'w', encoding='utf-8') as arquivo:
        json.dump(data, arquivo, indent=4, ensure_ascii=False)

    print("Dados salvos com sucesso no arquivo JSON.")
