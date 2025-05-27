import json
import os

from langchain_ollama import ChatOllama
from .SQLGeneratorVanna import MyVanna
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def train_vanna(model_name: str, train_path: str, db_path: str = None):
    """
    Treina o modelo Vanna com os dados de treinamento fornecidos.
    
    Args:
        model_name (str): Nome do modelo a ser treinado.
        train_path (str): Caminho para o arquivo de treinamento.
        db_path (str, optional): Caminho para o banco de dados SQLite. Se None, não conecta ao banco de dados.
    """

    train_path = os.path.join(BASE_DIR, train_path)
    print(f"Treinando o modelo {model_name} com os dados do arquivo {train_path}.")

    vanna = MyVanna(LLM=ChatOllama, model_name=model_name, config={"model": "llama3.1", "temperature": 0.0})
    
    if db_path:
        vanna.connect_to_sqlite(db_path)

    with open(train_path, 'r', encoding='utf-8') as f:
        try:
            training_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao carregar o arquivo JSON: {e}")

    if not training_data:
        raise ValueError("O arquivo de treinamento está vazio ou não contém dados válidos.")
   
    train_set = [
        {"question": item["question"], "sql": item["sql"]}
        for item in training_data.values()
        if "question" in item and "sql" in item
    ]

    for q in train_set:
        print(f"Treinando com: {q['question']} -> {q['sql']}")

        vanna.train(
            question=q["question"],
            sql=q["sql"]
        )

    print(vanna.get_training_data())
    #vanna.remove_training_data(id='10504616-ddl')

    print("Treinamento concluído.")


#Treinamento de Estudante na Disciplina
train_vanna(model_name="estudante_na_disciplina",train_path="Estudante_na_Disciplina/train.json",db_path="db_estudante_disciplina.sqlite")

#Treinamento de Estudante Info Gerais
#train_vanna(model_name="estudante_info_gerais",train_path="Estudante_Info_Gerais/train.json",db_path="db_estudantes.sqlite")

#Treinamento de Estagio
#train_vanna(model_name="estagio",train_path="Estagio/train.json",db_path="db_estagio.sqlite")

#Treinamento de Disciplina
#train_vanna(model_name="disciplina",train_path="Disciplina/train.json",db_path="db_disciplina.sqlite")

#Treinamento de Curso
#train_vanna(model_name="curso", train_path="Curso/train.json", db_path="db_cursos.sqlite")
    