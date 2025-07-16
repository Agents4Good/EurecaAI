from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

class RunDemo():

    def __init__(self, system):
        self.system = system

    def run(self, query: str, config: dict, stream_mode: str = "values"):
        """
        Executa o sistema com uma query e retorna a resposta.
        """

        if stream_mode == "values" or "json":
            inputs = {"messages": [HumanMessage(content=query)]}
            for message_chunk in self.system.stream(inputs, config, stream_mode=stream_mode):
                message_chunk["messages"][-1].pretty_print()
                
        elif stream_mode == "messages":
            inputs = {"messages": [HumanMessage(content=query)]}
            for message_chunk, _ in self.system.stream(inputs, config, stream_mode=stream_mode):
                if message_chunk.content:
                    print(message_chunk.content, end="", flush=True)

    
    async def run_async(self, query: str, config: str, stream_mode: str = "values"):
        """
        """

        if stream_mode == "values" or "json":
            inputs = {"messages": [HumanMessage(content=query)]}
            async for message_chunk in self.system.astream(inputs, config, stream_mode=stream_mode):
                message_chunk["messages"][-1].pretty_print()

    
    def save_graph_image(self, filename: str = "graph.png"):
        output_file = filename
        graph_img = self.system.get_graph().draw_mermaid_png()

        try:
            with open(output_file, "wb") as f:
                f.write(graph_img)
            print("Imagem criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar a imagem: {e}")
