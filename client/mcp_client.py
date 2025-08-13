import os
import asyncio
from typing import Optional
from langchain_community.chat_models import ChatDeepInfra
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
from agentes.agente_tools import AgenteTools

from langchain_community.chat_models import ChatDeepInfra
from agentes.agente_tools import AgenteTools
from agentes.agente_tools_sem_suporte import AgenteToolsSemSuporte


from dotenv import load_dotenv
load_dotenv()



# prompt = """
# Você é um assistente universitário e pode usar ferramentas para responder perguntas. Você não deve executar as ferramentas, seu papel é apenas escolher as ferramentas corretas e passar os parámetros no fluxo de execução. ** Sempre que quiser usar uma ferramenta, escreva assim: **
#     use_tool(nome_da_ferramenta, {'param1': 'valor', 'param2': 'valor'})
    
# Suas ferramentas:
# - buscar_todas_disciplinas_curso {campus: codigo_campus, curso: codigo_do_curso }.
# - buscar_disciplina_especifica_curso {disciplina: codigo_disciplina, campus: codigo_campus, curso: codigo_curso}

# IMPORTANTE:
# - utilize somente as suas ferramentas.
# """



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

        streamable = {
            "url": "http://100.66.116.115:8888/mcp", # URL que Bia usa
            "transport": "streamable_http",
        }

        self.client = MultiServerMCPClient({"servidor": streamable})
        self.session_cm = self.client.session("servidor")
        self.session = await self.session_cm.__aenter__()
        await self.session.initialize()
        self.tools = await load_mcp_tools(self.session)
        #print( " PROMPT ", prompt.messages[0].content.text)

        print("✅ Ferramentas carregadas diretamente do MCP server:",
              [t.name for t in self.tools])
        
        prompts = await load_mcp_prompt(self.session, "campus_prompt")
        prompt = prompts[0].content


        # print(" PROMPT ", prompt)
        # print("TIPOOOO PROMPT " , type(prompt.content))
        #print("Available prompts:", [p.content for p in prompt])

        #print(" TOOOLS ", self.tools)
       
        # sem suporte a tool call Qwen/Qwen2.5-Coder-7B
        #meta-llama/Llama-4-Scout-17B-16E-Instruct

    
        self.agent = AgenteToolsSemSuporte(
            LLM=ChatDeepInfra,
            model="Qwen/Qwen2.5-Coder-7B",
            tools=self.tools,
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
            session=self.session
        )


        # self.agent = AgenteTools(
        #     LLM=ChatDeepInfra,
        #     model="Qwen/Qwen2.5-Coder-7B",
        #     tools=self.tools,
        #     prompt=prompt,
        #     temperature=0.7,
        #     max_tokens=1000
        # )



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

