import strawberry

@strawberry.type
class Campus:
    campus: int
    descricao: str
    representacao: str