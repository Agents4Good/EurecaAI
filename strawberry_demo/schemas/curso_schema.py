from typing import Optional
import strawberry


@strawberry.type
class Curso:
    codigo_do_curso: int
    descricao: str
    status: str
    grau_do_curso:str
    codigo_do_setor:int
    nome_do_setor: str
    campus:int
    nome_do_campus: str
    turno: str
    periodo_de_inicio: str
    data_de_funcionamento: Optional[str]
    codigo_inep: int
    modalidade_academica: str
    curriculo_atual: int
    area_de_retencao: Optional[int]
    ciclo_enade: Optional[int]
