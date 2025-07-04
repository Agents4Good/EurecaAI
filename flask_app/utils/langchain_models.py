from langchain_community.chat_models import ChatDeepInfra
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(override=True)

# Supervisor
supervisor_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)
#supervisor_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Agregador
#aggregator_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0, max_tokens=2048)
aggregator_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Agentes Especializados
agents_model = ChatDeepInfra(model="Qwen/Qwen3-14B", temperature=0, max_tokens=2048)
#agents_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Para ser utilizado nas tools que fazem RAG
model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)