from langchain_community.chat_models import ChatDeepInfra
from dotenv import load_dotenv

load_dotenv(override=True)

# Supervisor
supervisor_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)

# Agregador
aggregator_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0, max_tokens=2048)

# Agentes Especializados
agents_model = ChatDeepInfra(model="Qwen/Qwen3-14B", temperature=0, max_tokens=2048)

# Para ser utilizado nas tools que fazem RAG
model = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)