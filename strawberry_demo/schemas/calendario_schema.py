from typing import Optional
import strawberry

@strawberry.type
class Calendario:
    id: int
    periodo: str
    campus: int
    inicio_das_matriculas: str
    inicio_das_aulas: str
    um_terco_do_periodo: Optional[str]
    ultimo_dia_para_registro_de_notas: Optional[str]
    um_quarto_do_periodo: Optional[str]
    numero_de_semanas: Optional[str]
