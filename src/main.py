import asyncio, sys

from langchain_core.messages import HumanMessage
from .agents.build_graph import build

from IPython.display import Image

async def run(system, query, config):
    """
    Executa o sistema com uma query e retorna a resposta.
    """
    inputs = {"messages": [HumanMessage(content=query)]}
    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

async def run_interactive(system):
    """
    Executa uma sessão interativa.
    """
    print("Bem-vindo ao UFCGPT, seu assistente acadêmico inteligente!")
    print("Você pode perguntar sobre cursos, disciplinas, matrícula, comunicados oficiais, resoluções acadêmicas e muito mais.")
    print("Digite 'sair' para encerrar a sessão.")

    # Configuração inicial da memória para a sessão interativa
    config = {"configurable": {"thread_id": "1"}}

    while True:
        query = input("\nDigite sua pergunta: ").strip()
        if query.lower() == 'sair':
            print("Obrigado por usar o UFCGPT. Até logo!")
            break
        print("\nProcessando sua solicitação...")
        await run(system, query, config)
        print("\nResposta concluída.")

async def main():
    """
    Executa a aplicação.
    """
    system = build()
    
    '''output_file = "grafo1.png"
    graph_image = system.get_graph().draw_mermaid_png()

    with open(output_file, "wb") as f:
        f.write(graph_image)

    print(f"Grafo salvo como {output_file}" + "\n")'''
    
    if len(sys.argv) < 2:
        #await run_interactive(system)
        async for s in system.astream(
        {
            "messages": [
                #HumanMessage(content=f"{"Qual o código do curso de ciência da computação?"}")
                HumanMessage(content=f"{"De quais regiões vem os estudantes de ciência da computação?"}")
                #HumanMessage(content=f"{"Traga informações sobre o curso de ciência da computação com código: 14102100."}")
            ]
        }
        ):
            if "__end__" not in s:
                print(s)
                print("----")
    else:
        query = " ".join(sys.argv[1:])
        config = {"configurable": {"thread_id": "1"}}
        await run(system, query, config)

if __name__ == '__main__':
    asyncio.run(main())