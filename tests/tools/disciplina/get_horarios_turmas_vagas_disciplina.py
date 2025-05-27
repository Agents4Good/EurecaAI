import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from .turmas_por_cursos import get_turmas_por_cursos
from ..utils.base_url import URL_BASE
from ..utils.validacoes import valida_periodo_curriculo, validar_turma

def get_horarios_turmas_vagas_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, turma: Any = "", periodo: Any = "") -> list:
    """_summary_
    Retorna os horários e sala de aula de uma disciplina, além das turmas da disciplina e as vagas ofertadas para as turmas dessa disciplina.

    Use esta função quando a pergunta envolver:
    - dia, horário ou sala da aula;
    - setor responsável ou período da disciplina;
    - vagas ofertadas para uma disciplina ofertada para um ou mais cursos.

    Args:
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        nome_da_disciplina (Any): Nome da disciplina.
        turma (Any): Número da turma. Defaults to "".
        periodo (Any, optional): Período do curso. Defaults to "".
        
    Returns:
        list: Chame esta função se a pergunta for sobre quando e onde a disciplina ocorre.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    turma=str(turma)
    periodo=str(periodo)
    print(f"Tool `get_horarios_turmas_disciplina` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, turma={turma} e periodo={periodo}")
    
    validou_turma, mensagem = validar_turma(turma_usada=turma)
    if not validou_turma: return mensagem
    
    periodo, curriculo, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, periodo=periodo, curriculo="")
    if mensagem != "": return mensagem

    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=curriculo)
    
    print(dados_disciplina)

    if type(dados_disciplina) == list and type(dados_disciplina[0]) == dict and "error_status" in dados_disciplina[0]:
       return dados_disciplina[0]["msg"]


    params = {
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma,
        "periodo-de": periodo,
        "periodo-ate": periodo
    }
    response = requests.get(f'{URL_BASE}/horarios', params=params)

    print("========================\n")
    print("PARAMETROS", params)

    if response.status_code == 200:
        horarios = json.loads(response.text)
            
        filtros_horarios = []
        turmas_map = {}
        dias = {"2": "Segunda-feira", "3": "Terça-feira", "4": "Quarta-feira", "5": "Quinta-feira", "6": "Sexta-feira", "7": "Sábado"}

        for horario in horarios:
            turma = horario['turma']
            sala = horario['codigo_da_sala']
            dia = str(horario['dia'])
            dia_nome = dias.get(dia, f"Dia {dia}")
            horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

            if turma not in turmas_map:
                turmas_map[turma] = { 'turma': turma, 'sala': sala, 'horarios': {} }
                filtros_horarios.append(turmas_map[turma])

            turmas_map[turma]['horarios'][dia_nome] = horario_formatado
            turmas_map[turma]['vagas'] = get_turmas_por_cursos(dados_disciplina["disciplina"]["codigo"], turma, periodo)
        print(filtros_horarios)

        return filtros_horarios
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]

#print(get_horarios_turmas_disciplina(nome_do_curso="Ciência da Computação", nome_do_campus="Campina Grande", nome_da_disciplina="Teoria da computação", turma="", periodo="2024.1"))