import getpass, os, re
from langchain_core.messages import HumanMessage
from .agent_tools import AgentTools, AgentState
from langgraph.graph import StateGraph, START, END

class AgenteDisciplinas(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)

    def build(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_node("exit", self.exit_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", "exit"])
        workflow.add_edge("tools", "agent")
        workflow.add_edge("exit", END)
        return workflow.compile()
    

    """def run(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        '''
        output_file = "grafo.png"
        graph_image = self.app.get_graph().draw_mermaid_png()

        with open(output_file, "wb") as f:
            f.write(graph_image)
        '''
        s
        for message_chunk, metadata in self.app.stream({"messages": [HumanMessage(content=question)]}, thread, stream_mode="messages"):
            if message_chunk.content:
                print(message_chunk.content, end="", flush=True)"""