import functools
from dotenv import load_dotenv

from ..tools.eureca.curso_tools import *
from ..tools.eureca.disciplina_tools import *
from ..tools.eureca.campus_tools import *
from ..tools.eureca.setor_tools import *
from ..tools.detector.detect_tags import *

from ..prompts.system_prompts import *

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor


CURSO_EURECA_TOOLS = [
    buscar_codigos_cursos,
    consultar_curso,
    #get_curriculos,
    #get_curriculo_mais_recente,
    #get_estudantes,
    #get_estudantes_formados
]

DISCIPLINA_EURECA_TOOLS = [
    get_disciplinas_curso,
    get_disciplina,
    get_plano_de_curso,
    get_plano_de_aulas,
    get_turmas,
    get_media_notas_turma_disciplina,
    get_horarios_disciplinas,
    pre_requisitos_disciplinas
]

CAMPUS_EURECA_TOOLS = [
    get_campi,
    get_calendarios,
    get_periodo_mais_recente
]

SETOR_TOOLS = [
    get_setores,
    get_total_professores,
    get_estagios
]

DETECTOR_TOOLS = [
    detect
]

load_dotenv()

model = ChatOllama(model="MFDoom/deepseek-r1-tool-calling:8b")
#model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
#model = ChatOpenAI(model="gpt-4o")

async def agent_node(state, agent, name):
    """
      Executa um agente específico com base em um estado fornecido (state) 
      e retornar a resposta desse agente.
    """
    try:
        result = await agent.ainvoke(state)
        if isinstance(result, dict) and "messages" in result:
            return {"messages": [AIMessage(content=result["messages"][-1].content, name=name)]}
        return {"messages": [AIMessage(content=str(result), name=name)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Ocorreu um erro: {str(e)}", name=name)]}

def create_general_agent(llm, tools, state_modifier):
    prompt = ChatPromptTemplate.from_messages([
        ("system", state_modifier), 
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


# Agente_Cursos_Eureca
#cursos_eureca_agent = build_hf_agent_with_tools()
cursos_eureca_agent = create_react_agent(model, tools=CURSO_EURECA_TOOLS, state_modifier=CURSOS_SYSTEM_PROMPT)
cursos_eureca_node = functools.partial(agent_node, agent=cursos_eureca_agent, name="Agente_Cursos_Eureca")

# Agente_Disciplinas_Turmas_Eureca
disciplinas_eureca_agent = create_react_agent(model, tools=DISCIPLINA_EURECA_TOOLS, state_modifier=DISCIPLINAS_TURMAS_SYSTEM_PROMPT)
disciplinas_eureca_node = functools.partial(agent_node, agent=disciplinas_eureca_agent, name="Agente_Disciplinas_Turmas_Eureca")

# Agente_Campus_Eureca
campus_eureca_agent = create_react_agent(model, tools=CAMPUS_EURECA_TOOLS, state_modifier=CAMPI_SYSTEM_PROMPT)
campus_eureca_node = functools.partial(agent_node, agent=campus_eureca_agent, name="Agente_Campus_Eureca")

# Agente_Setor_Professor_Estagio_Eureca
setor_agent = create_react_agent(model, tools=SETOR_TOOLS, state_modifier=SETOR_SYSTEM_PROMPT)
setor_node = functools.partial(agent_node, agent=setor_agent, name="Agente_Setor_Professor_Estagio_Eureca")

# Agente_Detector
detector_agent = create_react_agent(model, tools=DETECTOR_TOOLS, state_modifier=DETECTOR_SYSTEM_PROMPT)
detector_node = functools.partial(agent_node, agent=detector_agent, name="Agente_Detector")