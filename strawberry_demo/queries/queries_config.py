import sys
#configuração pra não dar problema na importação
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List
import strawberry
import strawberry.resolvers


from schemas.campus_schema import Campus
from schemas.calendario_schema import Calendario
from schemas.curso_schema import Curso
from schemas.curriculo_schema import Curriculo
from schemas.estudante_schema import Estudante, EstudanteDisciplina
from schemas.disciplina_schema import Disciplina, HorarioDisciplina, PreRequisitoDisciplina
from schemas.plano_de_curso_schema import PlanoDeCurso
from schemas.aula_schema import Aula
from schemas.turma_schema import Turma

from api_requests.campus_requests import *
from api_requests.cursos_requests import *
from api_requests.disciplina_requests import *



@strawberry.type
class Query:
    allCampus: List[Campus] = strawberry.field(resolver=get_campi)
    calendarios: List[Calendario] = strawberry.field(resolver=get_calendarios)
    periodoMaisRecente: Calendario = strawberry.field(resolver=get_periodo_mais_recente)
    allCursosAtivos: List[Curso] = strawberry.field(resolver=get_cursos_ativos)
    curso: List[Curso] = strawberry.field(resolver=get_curso) 
    curriculos: List[Curriculo] = strawberry.field(resolver =get_curriculos)
    curriculoMaisRecente: Curriculo = strawberry.field(resolver=get_curriculo_mais_recente)
    #estudantesGeraisPorCurso: List[Estudante] = strawberry.field(resolver=get_estudantes)
    estudantesFormados: List[Estudante] = strawberry.field(resolver=get_estudantes_formados)
    disciplinaPorCursoCurriculo: List[Disciplina] = strawberry.field(resolver=get_disciplinas_curso)
    disciplinaPorCodigoCurriculo: List[Disciplina] = strawberry.field(resolver=get_disciplina)
    planoDeCursoPorDisciplinaPeriodo: List[PlanoDeCurso] = strawberry.field(resolver=get_plano_de_curso)
    planoDeAula : List[Aula] = strawberry.field(resolver=get_plano_de_aulas)
    turmas: List[Turma] = strawberry.field(resolver=get_turmas)
    horarioDisciplinas: List[HorarioDisciplina] = strawberry.field(resolver=get_horarios_disciplinas)
    disciplina:List[Disciplina] = strawberry.field(resolver=get_disciplina_for_tool)
 