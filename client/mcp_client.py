import os
import asyncio
from typing import Optional
from langchain_community.chat_models import ChatDeepInfra
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from agentes.agente_tools import AgenteTools

from langchain_community.chat_models import ChatDeepInfra
from agentes.agente_tools import AgenteTools

from dotenv import load_dotenv
load_dotenv()

class MCPClient:
    def __init__(self):
        self.client: Optional[MultiServerMCPClient] = None
        self.session = None 
        self.tools = None
        self.agent: Optional[AgenteTools] = None

    async def connect_to_server(self, server_script_path: str):
        if not server_script_path.endswith((".py", ".js")):
            raise ValueError("Server script deve ser .py ou .js")

        transport = {
            "command": "python" if server_script_path.endswith(".py") else "node",
            "args": [server_script_path],
            "transport": "stdio",
        }

        self.client = MultiServerMCPClient({"servidor": transport})
        self.session_cm = self.client.session("servidor")
        self.session = await self.session_cm.__aenter__()
        await self.session.initialize()
        self.tools = await load_mcp_tools(self.session)

        print("✅ Ferramentas carregadas diretamente do MCP server:",
              [t.name for t in self.tools])

        self.agent = AgenteTools(
            LLM=ChatDeepInfra,
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            tools=self.tools,
            prompt="Você é um assistente universitário e pode usar ferramentas para responder perguntas.",
            temperature=0.7,
            max_tokens=1000,
        )

    async def process_query(self, query: str) -> str:
        """Processa a query usando DeepInfra + MCP tools via agente LangChain"""
        if not self.agent:
            raise RuntimeError("Agente não inicializado. Rode connect_to_server antes.")
        
        response = await self.agent.arun(query)
        return response

    async def chat_loop(self):
        print("\n🤖 MCP Client com DeepInfra iniciado! Digite 'quit' para sair.")
        while True:
            try:
                query = input("\nVocê: ").strip()
                #query = "traga todas as disciplinas do curso 14102100 campus 1 "
                if query.lower() == "quit":
                    break
                response = await self.process_query(query)
                print("\n🤖 Resposta:", response)
            except Exception as e:
                print(f"\n❌ Erro no ChatLoop: {e}")

    async def cleanup(self):
        if self.session_cm:
            await self.session_cm.__aexit__(None, None, None)

