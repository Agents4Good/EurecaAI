from langchain_ollama import ChatOllama
from utils.files import write_in_json_file
import subprocess

#caminho para o projeto Eureca
path = "D:/Workspace/python/agents4good/EurecaAI"

model = ChatOllama(model="llama3.2:3b")

def executar_processo(prompt):
    processo = subprocess.Popen(
        ['python', '-m', 'src.main', prompt],  # Chama o script com a pergunta como argumento
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=path
    )

    stdout, stderr = processo.communicate()
    print("Saída do script interativo:")
    print(stdout)
    write_in_json_file(stdout) #escreve no arquivo json a resposta da LLM
    if stderr:
        print("Erros:")
        print(stderr)

while True:
    prompt = input("Pergunta: ")
    executar_processo(prompt)
