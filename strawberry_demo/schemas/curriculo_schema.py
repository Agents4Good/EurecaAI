import strawberry
from typing import Optional

@strawberry.type
class Curriculo:
    codigo_do_curso: int
    codigo_do_curriculo: int
    regime: int
    duracao_minima: int
    duracao_maxima: int
    duracao_media: int
    carga_horaria_creditos_minima: int
    carga_horaria_creditos_maxima: int
    carga_horaria_disciplinas_obrigatorias_minima: int
    carga_horaria_disciplinas_optativas_minima: int
    carga_horaria_atividades_complementares_minima: int
    carga_horaria_minima_total: int
    minimo_creditos_disciplinas_obrigatorias: int
    minimo_creditos_disciplinas_optativas: int
    minimo_creditos_atividades_complementares: int
    minimo_creditos_total: int
    numero_disciplinas_obrigatorias_minimo: int
    numero_disciplinas_optativas_minimo: int
    numero_atividades_complementares_minimo: int
    numero_disciplinas_minimo: int
    numero_interrupcoes_matricula_maximo: int
    numero_interrupcoes_periodo_maximo: int
    numero_matriculas_institucionais_maximo: int
    numero_matriculas_extensao_maximo: Optional[int]
    carga_horaria_extensao: Optional[int]
    disciplina_atividades_complementares_flexiveis: Optional[int]
    disciplina_atividades_complementares_extensao: Optional[int]
    periodo_inicio: Optional[int]
