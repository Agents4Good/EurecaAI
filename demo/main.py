import asyncio, sys

from .agents.eureca_chat import EurecaChat
from .run_demo import RunDemo

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra

from dotenv import load_dotenv

load_dotenv()

# SUPERVISOR
supervisor = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)

# AGREGADOR
#aggregator = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)
#aggregator = ChatOllama(model="qwen3", temperature=0)

# AGENTES ESPECÍFICOS
agents = ChatDeepInfra(model="Qwen/Qwen3-14B", temperature=0, max_tokens=2048)
#agents = ChatOpenAI(model="meta-llama/Llama-3.3-70B-Instruct", base_url="https://api.deepinfra.com/v1/openai", temperature=0)


async def main():
    """
    Executa a aplicação.
    """
    app = EurecaChat(
        supervisor_model=supervisor,
        aggregator_model=supervisor,
        agents_model=agents
    ).build()
    demo = RunDemo(app)

    #demo.save_graph_image("eureca_graph.png")

    config = {"configurable": {"thread_id": "1"}}

    if len(sys.argv) < 2:
        query = "qual o código de ciência da computação?"
        #query = "Quais cursos foram criado em 2009" # DANDO PROBLEMA
        #query = "Quais são as matrículas dos estudantes que cursaram Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?" # DANDO PROBLEMA
        query = "O curso de Ciências Sociais está disponível em qual campus e quais são os cursos do campus de patos?" # INTEGRAR ALTERAÇÕES FEITAS EM CURSO DA BRANCH 'NOM'
        query = "Quais são os códigos e nomes das disciplinas no curso de computação"
        query = "Eu quero sabar a ementa da disciplina teoria da comuptação do curso de ciência da computação"
        query = "Quantos esudantes estrangeiros tem no curso de ciência da computação do campus de campina grande?"
        query = "Quantas estudantes mulheres tem no curso de ciência da computação do Campus de campina grande?"
        query = "De onde vem os estudantes do curso de ciência da computação do campus Campina grande por estado? Me mostre pra cada estado do país"
        
        #query = "As médias das notas de compiladores em ciência da computação"
        query = "Quais são os setorees do campus de campina grande?"
        
        #demo.run(query, config)
        await demo.run_async(query, config)
    else:
        query = " ".join(sys.argv[1:])

if __name__ == '__main__':
    #main()
    asyncio.run(main())