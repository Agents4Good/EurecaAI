import json
import requests
from typing import Any
from .utils import get_disciplina_grade_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..utils.base_url import URL_BASE

def get_plano_de_curso_disciplina(nome_do_curso: Any, nome_do_campus: Any, nome_da_disciplina: Any, curriculo: Any = "", periodo: Any = "") -> list:
    """
    Busca o plano de curso de uma disciplina.
    Use essa ferramenta quando quiser informações sobre:
    - ementa da disciplina;
    - objetivos da disciplina;
    - conteudo da disciplina;
    - metodologia adotada na disciplina;
    - avaliações;
    - referências bibliográficas utilizadas.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        nome_da_disciplina: nome da disciplina.
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo", se não souber use a string vazia '' para usar o currículo mais recente).
        periodo: periodo do curso (se não souber ou não foi informado, então passe a string vazia '').
    
    Returns:
        Lista com informações relevantes do plano de curso de uma disciplina.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    nome_da_disciplina=str(nome_da_disciplina)
    curriculo=str(curriculo)
    periodo=str(periodo)
    print(f"Tool get_plano_de_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, nome_da_disciplina={nome_da_disciplina}, curriculo={curriculo} e periodo={periodo}")
    
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
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