import json
import requests
from typing import Any
from ..curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_disciplinas(nome_do_curso: Any, nome_do_campus: Any, codigo_disciplina: Any = "", curriculo: Any = "") -> list:
    """
    Busca todas as discplinas ofertadas de um curso. Usar apenas quando for perguntado sobre apenas as disciplinas que o curso oferece.
    Use essa ferramenta quando quiser informações sobre:
    - código da disciplina;
    - nome da disciplina;
    - carga teórica e prática semanal;
    - quantidade de créditos;
    - horas totais;
    - carga teorica teórica/prática minima/máxima;
    - número de semanas de aulas;
    - código e nome do setor responsável;
    - nome e código do campus;
    - carga horária de extensão; 
    - contabilização de créditos.
    
    Args:
        nome_do_curso: nome do curso. Se não souber, usar o campus padrão "Campina Grande".
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...
        codigo_disciplina: Código da disciplina (se não souber, usar a string vazia '').
        curriculo: ano do curriculo do curso (passe apenas quando o usuário informar explicitamente a palavra "currículo", se não souber use a string vazia '' para usar o currículo mais recente).
    
    Returns:
        Retorna uma lista de disciplinas ofertadas pelo curso.
    """

    curriculo = str(curriculo)
    nome_do_curso = str(nome_do_curso)    
    nome_do_campus = str(nome_do_campus)
    print(f"Tool get_disciplinas_curso chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus} e codigo_curriculo={curriculo}.")
    
    if (curriculo == ""):
        curriculo = get_curriculo_mais_recente_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)

    dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
    
    params = {
        'curso': dados_curso['curso']['codigo'],
        'curriculo': curriculo["codigo_do_curriculo"]
    }

    response = requests.get(f'{URL_BASE}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]