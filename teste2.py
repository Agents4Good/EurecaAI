from transformers import AutoModel, AutoTokenizer

modelo_nome = "meta-llama/Llama-3.3-70B-Instruct"  # Substitua pelo modelo que deseja baixar

# Baixar o modelo e o tokenizer
modelo = AutoModel.from_pretrained(modelo_nome)
tokenizer = AutoTokenizer.from_pretrained(modelo_nome)

# O modelo e o tokenizer serão armazenados em ~/.cache/huggingface/
print("Download concluído!")
from transformers import AutoModel, AutoTokenizer

modelo_nome = "meta-llama/Llama-3.3-70B-Instruct"  # Nome do modelo
diretorio_local = "./modelo_llama3"  # Diretório onde o modelo será salvo

# Baixar o modelo e o tokenizer
modelo = AutoModel.from_pretrained(modelo_nome)
tokenizer = AutoTokenizer.from_pretrained(modelo_nome)

# Salvar localmente
modelo.save_pretrained(diretorio_local)
tokenizer.save_pretrained(diretorio_local)

print(f"Modelo salvo em: {diretorio_local}")
