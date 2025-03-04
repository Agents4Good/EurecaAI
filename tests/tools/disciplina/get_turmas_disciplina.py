import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .get_disciplina import get_disciplina
from ..utils.base_url import URL_BASE

def get_turmas_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, periodo: Any = "", curriculo: Any = "") -> list:
    """
    Busca todas as turmas de uma unica disciplina.
    
    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        periodo: período (se não souber não coloque nada aqui para obter o período mais recente).
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').
    
    Returns:
        Lista com informações relevantes das turmas.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    curriculo=str(curriculo)
    
    print(f"Tool get_turmas chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, periodo={periodo} e codigo_curriculo={curriculo}")
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    dados_disciplina = get_disciplina(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)

    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"]
    }
    
    response = requests.get(f'{URL_BASE}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da disciplina porque a disciplina não existe para esse período."}]