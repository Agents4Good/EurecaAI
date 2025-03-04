import json
import requests
from typing import Any
from .get_disciplina import get_disciplina
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_plano_aulas_turma(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, periodo: Any = "", numero_da_turma: Any = "", curriculo: Any = "") -> list:
    """
    Busca o plano de aulas de uma turma de uma disciplina. 
    Use quando quiser buscar informação do tema abordado na aula em um dia específico. 
    Essa ferramenta lhe dará uma lista de temas das aulas da disciplina que irá ocorrer em cada dia.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        periodo: período letivo (passe a string vazia '' se não souber).
        numero_da_turma: valor numérico da turma (se não souber, use a turma '01' como turma padrão).
        curriculo: valor inteiro do ano (se não tiver ou se quiser a mais recente use a string vazia '').

    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    curriculo=str(curriculo)
    numero_da_turma=str(numero_da_turma)
    periodo=str(periodo)
    
    print(f"Tool get_plano_de_aulas chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, periodo={periodo}, numero_turma={numero_da_turma} e curriculo={curriculo}.")
    dados_disciplina = get_disciplina(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (str(periodo) == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        'disciplina': dados_disciplina["disciplina"]["codigo"],
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': numero_da_turma
    }

    response = requests.get(f'{URL_BASE}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]