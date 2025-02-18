from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace


from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.tools import Tool
from langchain.tools.render import render_text_description
import requests
import json

base_url = "https://eureca.lsd.ufcg.edu.br/das/v2"
llm = HuggingFaceEndpoint(repo_id="HuggingFaceH4/zephyr-7b-beta")
chat_model = ChatHuggingFace(llm=llm)

def get_cursos_ativos() -> list:
   url_cursos = f'{base_url}/cursos'
   params = {
       'status-enum':'ATIVOS',
       'campus': '1'
   }
   print("chamando a tool get_cursos_ativos.")
   response = requests.get(url_cursos, params=params)

   if response.status_code == 200:
       data_json = json.loads(response.text)
       return [{'codigo_do_curso': data['codigo_do_curso'], 'descricao': data['descricao']} for data in data_json]
   else:
       return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

minha_tool = Tool(
   name="get_cursos_ativos",
   func=get_cursos_ativos,
   description="""
   Buscar todos os cursos ativos da UFCG.


   Args:
  
   Returns:
       Lista de cursos com 'codigo_do_curso' e 'descricao'.
   """
)

tools = [minha_tool]

prompt = hub.pull("hwchase17/react-json")
prompt = prompt.partial(
   tools=render_text_description(tools),
   tool_names=", ".join([t.name for t in tools]),
)

chat_model_with_stop = chat_model.bind(stop=["\nObservation"])
agent = (
   {
       "input": lambda x: x["input"],
       "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
   }
   | prompt
   | chat_model_with_stop
   | ReActJsonSingleInputOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
   {
       "input": "Pense passo a passo. Chame a tool get_cursos_ativos! Busque, mesmo que demore, espere",
   }
)
