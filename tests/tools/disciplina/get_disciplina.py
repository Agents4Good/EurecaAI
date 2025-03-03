import json
import requests
from typing import Any
from .utils import get_disciplina_most_similar
from ..utils.base_url import URL_BASE

def get_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, curriculo: Any = "") -> list:    
    """
    Buscar as informações específicas de uma disciplina do curso.
    É possível obter informações como: nome do setor, campus, carga horária, créditos.

    Args:
        nome_da_disciplina: nome da disciplina específica.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    """
    
    print(f"Tool get_informacoes_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}")    
    
    nome_da_disciplina = str(nome_da_disciplina)
    nome_do_curso = str(nome_do_curso)
    nome_do_campus = str(nome_do_campus)
        
    try:
        dados_disciplina, curriculo = get_disciplina_most_similar(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, nome_disciplina=nome_da_disciplina, curriculo=curriculo)
    except Exception as e:
        return [{"error_status": response.status_code, "msg": str(e)}]

    params = {
        'curriculo': curriculo,
        'disciplina': dados_disciplina['disciplina']['codigo']
    }

    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]