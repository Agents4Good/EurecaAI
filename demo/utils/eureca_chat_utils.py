from typing import TypedDict, Optional, List

from langchain_core.callbacks.base import BaseCallbackHandler
from langgraph.graph import MessagesState

from tests.tools.curso import *
from tests.tools.disciplina import *
from tests.tools.estudante import *
from tests.tools.setor import *
from tests.tools.campus.get_calendarios import get_calendarios
from tests.tools.campus.get_campi import get_campi
from tests.tools.campus.get_periodo_mais_recente import get_periodo_mais_recente


# TOOLS USADAS
CAMPUS_TOOLS = [
    get_campi,
    get_calendarios,
    get_periodo_mais_recente
]

SETOR_TOOLS = [
    get_estagios
]

CURSO_TOOLS = [
    obter_dados_de_curso_especifico, 
    obter_dados_de_todos_os_cursos,
    get_todos_curriculos_do_curso
]

DISCIPLINA_TOOLS = [
    get_disciplina_ofertadas_periodo,
    get_horarios_turmas_vagas_disciplina,
    get_matriculas_disciplina,
    get_plano_de_aulas,
    get_plano_de_curso_disciplina,
    get_pre_requisitos_disciplina,
    #get_disciplinas,
]

ESTUDANTE_TOOLS = [
    obter_dados_gerais_de_todos_estudantes,
    obter_ingressantes_sisu
]

SETOR_TOOLS = [
    get_estagios,
    get_professores_setor,
    get_todos_setores
]


# Handler de streaming para tokens
class SocketIOStreamingHandler(BaseCallbackHandler):
    def __init__(self, sid, socketio):
        self.sid = sid
        self.sio = socketio

    async def emit(self, event, data):
        await self.sio.emit(event, data, room=self.sid)

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.sio.emit("token", {"resposta": token}, room=self.sid)

# SCHEMA USADO PARA A CONFIG DO GRAFO
class ConfigSchema(TypedDict):
    token: Optional[str]
    callbacks_sio: List[SocketIOStreamingHandler]

# SETAR ESTADO DO GRAFO GERAL (SUPERVISOR)
class AgentState(MessagesState):
    next: str
    context: str
    summary: str
    response_count: int
    # last_agent: Optional[str]
    # agent_repetition_count: int
