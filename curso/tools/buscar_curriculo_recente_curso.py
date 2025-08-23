from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_curriculo_recente_curso(curso:Any) -> dict:
    """
    Retorna a informação do currículo mais recente de um curso específico da UFCG.

    Args:
        campus (Any): Código do campus.
        curso (Any): Código do curso.

    Returns:
        dict: Dicionário com informações do currículo no formato:
            {
                "codigo_do_curso": int,                                 # Código do curso
                "codigo_do_curriculo": int,                             # Ano/código do currículo
                "regime": int,                                          # Regime acadêmico
                "duracao_minima": int,                                  # Duração mínima (períodos)
                "duracao_maxima": int,                                  # Duração máxima (períodos)
                "duracao_media": int,                                   # Duração média (períodos)
                "carga_horaria_creditos_minima": int,                   # Créditos mínimos por período
                "carga_horaria_creditos_maxima": int,                   # Créditos máximos por período
                "carga_horaria_disciplinas_obrigatorias_minima": int,   # CH mínima obrigatória
                "carga_horaria_disciplinas_optativas_minima": int,      # CH mínima optativa
                "carga_horaria_atividades_complementares_minima": int,  # CH mínima atividades complementares
                "carga_horaria_minima_total": int,                      # CH mínima total do curso
                "minimo_creditos_disciplinas_obrigatorias": int,        # Créditos obrigatórios mínimos
                "minimo_creditos_disciplinas_optativas": int,           # Créditos optativos mínimos
                "minimo_creditos_atividades_complementares": int,       # Créditos atividades complementares mínimos
                "minimo_creditos_total": int,                           # Créditos totais mínimos
                "numero_disciplinas_obrigatorias_minimo": int,          # Disciplinas obrigatórias mínimas
                "numero_disciplinas_optativas_minimo": int,             # Disciplinas optativas mínimas
                "numero_atividades_complementares_minimo": int,         # Atividades complementares mínimas
                "numero_disciplinas_minimo": int,                       # Número total mínimo de disciplinas
                "numero_interrupcoes_matricula_maximo": int,            # Máx. interrupções de matrícula
                "numero_interrupcoes_periodo_maximo": int,              # Máx. interrupções de período
                "numero_matriculas_institucionais_maximo": int,         # Máx. matrículas institucionais
                "numero_matriculas_extensao_maximo": int,               # Máx. matrículas de extensão
                "carga_horaria_extensao": int,                          # CH de extensão
                "disciplina_atividades_complementares_flexiveis": int,  # Código da disciplina flexível
                "disciplina_atividades_complementares_extensao": int,   # Código da disciplina de extensão
                "periodo_inicio": int                                   # Período de início do currículo
            }
    """

    
    params = {
        "curso": curso
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/curriculos"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter o currículo ou nenhum currículo foi encontrado"
        
        return data[-1]
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise

