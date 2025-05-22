import json
from typing import Any
import requests
from ..campus.utils import get_campus_most_similar
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE


from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.Estudante_Info_Gerais.prompt import PROMPT_SQL_ESTUDANTES_INFO_GERAIS
from ...sql.Estudante_Info_Gerais.normalize_data import normalize_data_estudante
from ...sql.NoSQL.markdown_format.format_table import format_md_grafico_barra, format_md_grafico_pizza, format_md_grafico_doughnut

SITUACAO = ['SUSPENSOS', 'REINGRESSOS', 'REATIVADOS', 'DESISTENTE', 'EVADIDOS', 'JUBILADOS', 'ABANDONOS', 'TRANSFERIDOS', 'FINALIZADOS', 'INATIVOS', 'EGRESSOS', 'ATIVOS']
TIPO_GRAFICO = ['BARRA', 'PIZZA', 'ROSCA']

def obter_dados_gerais_de_todos_estudantes(query: Any, nome_do_curso: Any, nome_do_campus: Any, situacao_estudante: Any, gerar_grafico: Any = ""):
   """
      _summary_
      Buscar informações gerais dos estudantes da UFCG com base no(s) curso(s).
      Como quantidade, nome, matrícula, idade, sexo, cor, naturalidade, nacionalidade e local de nascimento.

      Args:
         query: Pergunta feita pelo usuário.
         nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
         nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 
         situacao_estudante: a situação do estudante, PRECISA ser um desses: 'SUSPENSOS', 'REINGRESSOS', 'REATIVADOS', 'DESISTENTE', 'EVADIDOS', 'JUBILADOS', 'ABANDONOS', 'TRANSFERIDOS', 'FINALIZADOS', 'INATIVOS', 'EGRESSOS', 'ATIVOS'.
         gerar_grafico: Tipo do gráfico que o usuário quer gerar, PRECISA ser um desses: 'BARRA', 'PIZZA', 'ROSCA'. Caso o usuário não queira ou não tenha informado, use o padrão vazio ''.

      Returns:
         Informações dos estudantes que ajude a responder a pergunta feita pelo usuário.
      
   """

   print(f"Tool `obter_dados_de_todos_estudantes` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, situacao_estudante={situacao_estudante} e gerar_grafico={gerar_grafico}.")
   query = str(query)
   nome_do_campus = str(nome_do_campus)
   nome_do_curso = str(nome_do_curso)
   situacao_estudante = str(situacao_estudante)
   gerar_grafico = str(gerar_grafico)

   if situacao_estudante in SITUACAO:
      params = {"situacao-do-estudante": situacao_estudante}
   else:
      return ["Por favor informe a situação dos estudantes correta.\n Pode ser uma dessas: SUSPENSOS, REINGRESSOS, REATIVADOS, DESISTENTE, EVADIDOS, JUBILADOS, ABANDONOS, TRANSFERIDOS, FINALIZADOS, INATIVOS, EGRESSOS, ATIVOS"]
      
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
      db_name = "db_estudantes.sqlite"
      gerenciador = GerenciadorSQLAutomatizado("Estudante_Info_Gerais", db_name)
      gerenciador.save_data(estudantes)
      response = gerenciador.get_data(query, PROMPT_SQL_ESTUDANTES_INFO_GERAIS)
      if gerar_grafico == "BARRA":
         print(format_md_grafico_barra(response))
         return format_md_grafico_barra(response)
      elif gerar_grafico == "PIZZA":
         return format_md_grafico_pizza(response)
      elif gerar_grafico == "ROSCA":
         return format_md_grafico_doughnut(response)
      print("Resposta da tool: ", response, "\n")
      return  f"RESULTADO DO SQL: {response}"
   else:
      return [{"error_status": response.status_code, "msg": response.json()}]