import inspect
import json
from typing import Any
import requests
from ..campus.utils import get_campus_most_similar
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from ..utils.remove_term import limpar_query

from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.Estudante_Info_Gerais.prompt import PROMPT_SQL_ESTUDANTES_INFO_GERAIS
from ...sql.Estudante_Info_Gerais.normalize_data import normalize_data_estudante

def obter_dados_gerais_de_todos_estudantes(query: Any, nome_do_curso: Any, nome_do_campus: Any):
   """
      _summary_
      Buscar informações gerais dos estudantes da UFCG com base no(s) curso(s).

      Args:
         query: Pergunta feita pelo usuário.
         nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
         nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 

      Returns:
         Informações dos estudantes que ajude a responder a pergunta feita pelo usuário.
      
   """

   print(f"Tool obter_dados_de_todos_estudantes chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")    
   params = {"situacao-do-estudante": "ATIVOS" }

   
   frame = inspect.currentframe()
   args, _, _, values = inspect.getargvalues(frame)
   parametros = {arg: values[arg] for arg in args if arg != 'query' and arg != 'self'}
   termos_para_remover = [str(v) for v in parametros.values() if v]
   query = limpar_query(str(query), termos_para_remover)
   print(f"Query com os termos removidos: {query}")

   nome_do_campus = str(nome_do_campus)
   nome_do_curso = str(nome_do_curso)
      
   if (nome_do_curso != "" and nome_do_campus != ""):
      dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
      dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
      params["curso"] = dados_curso['curso']['codigo']
      params["campus"] = dados_campus['campus']['codigo']
   elif (nome_do_curso == "" and nome_do_campus != ""):
      dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
      params["campus"] = dados_campus['campus']['codigo']
   elif (nome_do_curso == "" and nome_do_campus == ""):
      pass
   else:
      return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]

   response = requests.get(f'{URL_BASE}/estudantes', params=params)
   if response.status_code == 200:
      estudantes = normalize_data_estudante(json.loads(response.text))
      gerenciador = GerenciadorSQLAutomatizado("Estudante_Info_Gerais", "db_estudantes.sqlite", PROMPT_SQL_ESTUDANTES_INFO_GERAIS, temperature=0)
      gerenciador.save_data(estudantes)
      response = gerenciador.get_data('estudante_info_gerais', query, True)
      return  f"RESULTADO DO SQL: {response}"
     
   else:
      return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos estudantes da UFCG."}]