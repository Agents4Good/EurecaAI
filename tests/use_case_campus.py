import uuid, json
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.schema import SystemMessage
from prompts.prompts import *
from langchain_ollama import ChatOllama
from tools.campus.get_campi import get_campi
from tools.campus.get_calendarios import get_calendarios
from tools.campus.get_periodo_mais_recente import get_periodo_mais_recente
from dotenv import load_dotenv
load_dotenv()

class AgentToll:
    def __init__(self, LLM, model: str, tools: list, prompt: str, temperatura: int = 0):
        self.model = LLM(model=model, temperature=temperatura).bind_tools(tools)
        self.tools = ToolNode(tools)
        self.prompt = prompt
        self.app = self.build()
    
    
    def call_model(self, state: MessagesState):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=self.prompt))
        return {"messages": [self.extract_tool_calls(self.model.invoke(messages))]}
    
    
    def build(self):
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")
        return workflow.compile()

        
    def should_continue(self, state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
    
    
    def extract_tool_calls(self, response):
        try:
            content_data = json.loads(response.content)
            if "tool_calls" in content_data:
                tool_calls = content_data["tool_calls"]

                for tool_call in tool_calls:
                    tool_call.setdefault("id", str(uuid.uuid4()))
                    tool_call.setdefault("type", "tool_call")
                
                response.tool_calls = tool_calls
                response.content = content_data.get("content", "")
        
        except json.JSONDecodeError:
            pass
        return response
    
    
    def run(self, question: str):
        for chunk in self.app.stream({"messages": [("human", question)]}, stream_mode="values"):
            chunk["messages"][-1].pretty_print()


question = "Quais são os campus da UFCG?"
tools = [get_campi, get_calendarios, get_periodo_mais_recente]
agent = AgentToll(LLM=ChatOllama, model="llama3.2:3b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)
agent.run(question=question)
