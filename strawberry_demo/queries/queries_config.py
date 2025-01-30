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
from schemas.estudante_schema import Estudante

from api_requests.campus_requests import *
from api_requests.cursos_requests import *



@strawberry.type
class Query:
    allCampus: List[Campus] = strawberry.field(resolver=get_campi)
    calendarios: List[Calendario] = strawberry.field(resolver=get_calendarios)
    periodoMaisRecente: Calendario = strawberry.field(resolver=get_periodo_mais_recente)
    allCursosAtivos: List[Curso] = strawberry.field(resolver=get_cursos_ativos)
    curso: List[Curso] = strawberry.field(resolver=get_curso) 
    curriculos: List[Curriculo] = strawberry.field(resolver =get_curriculos)
    curriculoMaisRecente: Curriculo = strawberry.field(resolver=get_curriculo_mais_recente)
    estudantesPorCurso: List[Estudante] = strawberry.field(resolver=get_estudantes)