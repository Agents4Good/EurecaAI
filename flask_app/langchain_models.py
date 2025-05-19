from langchain_community.chat_models import ChatDeepInfra

# TESTE: para ser utilizado nas tools que fazem RAG
model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)