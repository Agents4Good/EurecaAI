import json
import requests
from typing import Any
from .get_disciplina import get_disciplina_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_plano_de_curso_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, curriculo: Any = "", periodo: Any = "") -> list:
    """
    Busca o plano de curso de uma disciplina.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
        periodo: periodo.
    
    Returns:
        Lista com informações relevantes do plano de curso de uma disciplina.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    curriculo=str(curriculo)
    periodo=str(periodo)
    
    print(f"Tool get_plano_de_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, curriculo={curriculo} e periodo={periodo}")
    
    dados_disciplina = get_disciplina_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        'disciplina': dados_disciplina['disciplina']['codigo'],
        'periodo-de': periodo,
        'periodo-ate': periodo
    }
    
    response = requests.get(f'{URL_BASE}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{
            "error_status": response.status_code, 
            "msg": f"Não foi possível obter informação da disciplina de {nome_da_disciplina} por não existir para esse período ou por ser chamada de outro nome."
        }]