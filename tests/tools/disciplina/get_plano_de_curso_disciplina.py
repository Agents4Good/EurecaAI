import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar_por_codigo_do_curso
from ..utils.base_url import URL_BASE
from ..utils.validacoes import valida_periodo_curriculo

def get_plano_de_curso_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, curriculo: Any = "", periodo: Any = "") -> list:
    """_summary_
    Retorna o plano de curso de uma disciplina.
    
    Use esta função quando a pergunta envolver:
    - ementa da disciplina, objetivos, conteúdos;
    - metodologia, avaliação ou bibliografia.
    
    Args:
        nome_do_curso (Any): Nome do curso.
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        nome_da_disciplina (Any): Nome da disciplina.
        curriculo (Any, optional): Ano do currículo. Defaults to "".
        periodo (Any, optional): Período do curso. Defaults to "".

    Returns:
        list: Informações a respeito de ementa, objetivos, conteúdos, metodologia, avaliação ou bibliografia.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    curriculo=str(curriculo)
    periodo=str(periodo)
    print(f"Tool get_plano_de_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, curriculo={curriculo} e periodo={periodo}")
    
    dados_curso, curriculo, periodo, mensagem = valida_periodo_curriculo(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, periodo=periodo, curriculo=curriculo)
    if mensagem != "": return mensagem

    dados_disciplina, _ = get_disciplina_grade_most_similar_por_codigo_do_curso(nome_da_disciplina=nome_da_disciplina, codigo_do_curso=dados_curso["curso"]["codigo"], curriculo=curriculo)
    if type(dados_disciplina) == list and type(dados_disciplina[0]) == dict and "error_status" in dados_disciplina[0]:
       return dados_disciplina[0]["msg"]
    
    params = {
        'disciplina': dados_disciplina['disciplina']['codigo'],
        'periodo-de': periodo,
        'periodo-ate': periodo
    }
    response = requests.get(f'{URL_BASE}/planos-de-curso', params=params)

    if response.status_code == 200:
        resultado = json.loads(response.text)
        print(resultado)
        return resultado
    else:
        return [{
            "error_status": response.status_code, 
            "msg": f"Não foi possível obter informação da disciplina de {nome_da_disciplina} por não existir para esse período ou por ser chamada de outro nome."
        }]