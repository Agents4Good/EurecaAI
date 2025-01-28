import sys
#configuração pra não dar problema na importação
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List
import strawberry
import strawberry.resolvers
from schemas.campus_schema import Campus
from schemas.calendario_schema import Calendario
from api_requests.campus_requests import *

@strawberry.type
class Query:
    allCampus: List[Campus] = strawberry.field(resolver=get_campi)
    calendarios: List[Calendario] = strawberry.field(resolver=get_calendarios)
    periodoMaisRecente: Calendario = strawberry.field(resolver=get_periodo_mais_recente)