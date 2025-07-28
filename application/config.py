import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatDeepInfra
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

# VARIÁVEIS PARA CRIAR O DB NO DOCKER
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Default

# URI DO BD (Postgres)
DB_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=disable"

# URL DA API DO EURECA
#URL_BASE = "https://eureca.lsd.ufcg.edu.br/das/v2"
URL_BASE = "https://eureca.sti.ufcg.edu.br/das/v2" # produção

# MODELOS UTILIZADOS:

# Supervisor
supervisor_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)
#supervisor_model = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)
#supervisor_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Agregador
#aggregator_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0, max_tokens=2048)
#aggregator_model = ChatOllama(model="llama3.1", temperature=0)
aggregator_model_class = ChatGoogleGenerativeAI
aggregator_model_kwargs = {
    "model": "gemini-2.0-flash",
    "temperature": 0
}

# Agentes Especializados
agents_model = ChatDeepInfra(model="Qwen/Qwen3-14B", temperature=0, max_tokens=2048)
#agents_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Modelo Sumarizador
summarizer_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Modelo para gerador de título do chat
title_model = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)

# Modelo para ser utilizado nas tools que fazem RAG
model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)