import strawberry
from typing import Optional

@strawberry.type
class PlanoDeCurso:
    turma: Optional[int]
    codigo_da_disciplina: Optional[int]
    nome_da_disciplina: Optional[str]
    codigo_do_setor: Optional[int]
    nome_do_setor: Optional[str]
    periodo: Optional[str]
    ementa: Optional[str]
    objetivos: Optional[str]
    conteudo: Optional[str]
    metodologia: Optional[str]
    avaliacao: Optional[str]
    referencias: Optional[str]
