import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strawberry_demo.main import schema

default_campus = "campus,descricao,representacao"
default_calendario = "id, periodo,campus, inicioDasAulas, inicioDasMatriculas,numeroDeSemanas,periodo,ultimoDiaParaRegistroDeNotas,umQuartoDoPeriodo,umTercoDoPeriodo"
  
# python -m strawberry_demo.queries.campus.campus_functions

def get_all_campi(data: str = default_campus):
        """
        Buscar todos os campi.
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
    """
    Buscar calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
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
     
#DOCUMENTAÇÂO DAS FUNÇÕES
get_all_campi.__doc__ = f"""
        Args:
            data: campos a serem retornados, por padrão é {default_campus}
    
        Returns:
            Lista com dicionários que possuem os campos desejados. Por padrão é
            {default_campus}.
"""

get_all_calendarios.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
       Informações desejadas dos calendário acadêmico. Por padrão é {default_calendario}
"""

get_periodo_mais_recente.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
       Informações desejadas do calendário acadêmico mais recente. Por padrão é {default_calendario}

"""



