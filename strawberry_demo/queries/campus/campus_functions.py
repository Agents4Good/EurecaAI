import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strawberry_demo.main import schema,app

default_campus = "campus,descricao,representacao"
default_calendario = "id, periodo,campus,inicio_das_matriculas,inicio_das_aulas,um_terco_do_periodo,ultimo_dia_para_registro_de_notas,um_quarto_do_periodo,numero_de_semanas"
  
# python -m strawberry_demo.queries.campus.campus_functions

def get_all_campi(data: str = default_campus):
        f"""
        Buscar todos os campi.

        Args:
            data: campos a serem retornados, por padrão é {default_campus}
    
        Returns:
            Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
        """
        try:
            query = f"""
                    query {{allCampus     
                    {{ 
                        {data} 
                    }}
                }}
            """
            result = schema.execute_sync(query)
            return result.data['allCampus']
        except Exception as e:
            return e

def get_all_calendarios(data: str = default_calendario):
    f"""
    Buscar calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.

    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
        Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    try:
        query = f"""
                    query {{calendarios
                        {{
                            {data}
                        }}
                    }}
                """
        result = schema.execute_sync(query)
        return result.data['calendarios']
    except Exception as e:
            return e

def get_periodo_mais_recente(data: str = default_calendario):
    """
    Buscar o período mais recente da universidade.

    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
       Informações relevantes do calendário acadêmico mais recente do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    """
    try:
        query = f"""
                    query {{periodoMaisRecente
                        {{
                            {data}
                        }}
                    }}
                """
        result = schema.execute_sync(query)
        return result.data['periodoMaisRecente']
    except Exception as e:
            return e
     
#print("RESPOSTA DA FILTRAGEM ", get_all_campi("campus"))
#print("RESPOSTA DA FILTRAGEM ", get_periodo_mais_recente("id"))




