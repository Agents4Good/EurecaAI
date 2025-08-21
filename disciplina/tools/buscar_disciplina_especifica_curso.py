from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info


@mcp.tool()
async def buscar_disciplina_especifica_curso(disciplina: Any, curso: Any, campus:Any) -> list[dict]:
    """
    Busca informações sobre uma determinada disciplina de um curso específico

    Args:
        disciplina: código da disciplina.
        curso: código do curso.
        campus: código do campus.
    
       Returns:
            list[dict]: Lista com uma única disciplina no formato:
                {
                    "codigo_da_disciplina": int,                 # Código da disciplina
                    "nome": str,                                 # Nome da disciplina
                    "carga_horaria_teorica_semanal": int,        # CH teórica semanal
                    "carga_horaria_pratica_semanal": int,        # CH prática semanal
                    "quantidade_de_creditos": int,               # Número de créditos
                    "horas_totais": int,                         # Carga horária total
                    "media_de_aprovacao": int,                   # Média necessária para aprovação
                    "carga_horaria_teorica_minima": int,         # CH teórica mínima
                    "carga_horaria_pratica_minima": int,         # CH prática mínima
                    "carga_horaria_teorica_maxima": int,         # CH teórica máxima
                    "carga_horaria_pratica_maxima": int,         # CH prática máxima
                    "numero_de_semanas": int,                    # Número de semanas da disciplina
                    "codigo_do_setor": int,                      # Código do setor responsável
                    "nome_do_setor": str,                        # Nome do setor responsável
                    "campus": int,                               # Código do campus
                    "nome_do_campus": str,                       # Nome do campus
                    "status": str,                               # Status da disciplina (ex.: ATIVO)
                    "contabiliza_creditos": str,                 # Indica se conta para créditos ("S" ou "N")
                    "tipo_de_componente_curricular": str,        # Tipo do componente (ex.: Atividade Complementar)
                    "carga_horaria_extensao": int                 # CH de extensão, se houver
                }
    """

    params = {
        "status": "ATIVOS",
        "campus": campus,
        "curso": curso, 
        "disciplina": disciplina
    }

    
    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/disciplinas"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return f"Não foi possível obter a disciplina {disciplina} do curso {curso} do campus {campus}"
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise