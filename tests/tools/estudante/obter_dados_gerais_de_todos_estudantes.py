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

def obter_dados_gerais_de_todos_estudantes(query: Any, nome_do_curso: Any, nome_do_campus: Any, situacao_estudante: Any, motivo_de_evasao: Any = "", gerar_grafico: Any = ""):
   """
      _summary_
      Buscar informações gerais dos estudantes da UFCG com base no(s) curso(s).
      Como quantidade, nome, matrícula, idade, sexo, cor, naturalidade, nacionalidade e local de nascimento.
      situação do estudante: 
         - Quando vocẽ usar situação do tipo "SUSPENSOS" use o motivo de evação como "SUSPENSOS";
         - Quando vocẽ usar situação do tipo "REINGRESSOS" use o motivo de evação como "CANCELADO NOVO INGRESSO MESMO CURSO";
         - Quando vocẽ usar situação do tipo "REATIVADOS" use o motivo de evação como "CANCELADO NOVO INGRESSO MESMO CURSO", "GRADUADO", "CANCELADO 3 REPROV MESMA DISCIPLINA", "CANCELAMENTO P/ SOLICITACAO ALUNO", "CANCELADO REPROVOU TODAS POR FALTAS", "CANCELAMENTO POR ABANDONO", "REGULAR", "CANCELAMENTO DE MATRICULA 
         - Quando vocẽ usar situação do tipo "DESISTENTES" use o motivo de evação como "NAO COMPARECEU AO REMANEJAMENTO", "AGUARDANDO CADASTRAMENTO", "NAO COMPARECEU CADASTRO", "INGRESSANTE NAO FEZ 1ª MATRICULA
         - Quando vocẽ usar situação do tipo "EVADIDOS" use o motivo de evação como "CANCELAMENTO P/ DECISAO JUDICIAL", "TRANSFERIDO PARA OUTRA IES", "CANCELADO 3 REPROV MESMA DISCIPLINA", "CUMPRIMENTO CONVENIO", "CANCELADO REPROVOU TODAS POR FALTAS", "CANCELAMENTO P/ SOLICITACAO ALUNO", "CANCELAMENTO POR ABANDONO", "CANCELAMENTO DE MATRICULA ", "CANCELAMENTO P/ MUDANCA CURSO", "REMANEJADO CURSO OU PERIODO", "CONCLUIDO - NAO COLOU GRAU", "CANCELADO NOVO INGRESSO OUTRO CURSO
         - Quando vocẽ usar situação do tipo "JUBILADOS" use o motivo de evação como "CANCELAMENTO DE MATRICULA", "CANCELADO REPROVOU TODAS POR FALTAS", "CANCELAMENTO P/ DECISAO JUDICIAL", "CANCELADO 3 REPROV MESMA DISCIPLINA
         - Quando vocẽ usar situação do tipo "ABANDONOS" use o motivo de evação como CANCELAMENTO P/ SOLICITACAO ALUNO", "CANCELAMENTO POR ABANDONO
         - Quando vocẽ usar situação do tipo "TRANSFERIDOS" use o motivo de evação como REMANEJADO CURSO OU PERIODO", "TRANSFERIDO PARA OUTRA IES", "CANCELADO NOVO INGRESSO OUTRO CURSO", "CANCELAMENTO P/ MUDANCA CURSO
         - Quando vocẽ usar situação do tipo "FINALIZADOS" use o motivo de evação como "CONCLUIDO - NAO COLOU GRAU", "CUMPRIMENTO CONVENIO
         - Quando vocẽ usar situação do tipo "INATIVOS" use o motivo de evação como CANCELAMENTO P/ DECISAO JUDICIAL", "TRANSFERIDO PARA OUTRA IES", "CANCELADO NOVO INGRESSO MESMO CURSO", "GRADUADO", "CANCELADO 3 REPROV MESMA DISCIPLINA", "CUMPRIMENTO CONVENIO", "NAO COMPARECEU AO REMANEJAMENTO", "CANCELADO REPROVOU TODAS POR FALTAS", "CANCELAMENTO P/ SOLICITACAO ALUNO", "AGUARDANDO CADASTRAMENTO", "CANCELAMENTO POR ABANDONO", "CANCELAMENTO DE MATRICULA ", "NAO COMPARECEU CADASTRO", "CANCELAMENTO P/ MUDANCA CURSO", "REMANEJADO CURSO OU PERIODO", "CONCLUIDO - NAO COLOU GRAU", "CANCELADO NOVO INGRESSO OUTRO CURSO", "INGRESSANTE NAO FEZ 1ª MATRICULA
         - Quando vocẽ usar situação do tipo "EGRESSOS" use o motivo de evação como "GRADUADO"
         - Quando vocẽ usar situação do tipo "ATIVOS" use o motivo de evação como "REGULAR"

         Observação: Lembrando que o campo motivo_de_evasão é opcional e só deve usar quando vier motivo de evasão na pergunta.

      Args:
         query: Pergunta feita pelo usuário.
         nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
         nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 
         situacao_estudante: a situação do estudante, PRECISA ser um desses: 'SUSPENSOS', 'REINGRESSOS', 'REATIVADOS', 'DESISTENTE', 'EVADIDOS', 'JUBILADOS', 'ABANDONOS', 'TRANSFERIDOS', 'FINALIZADOS', 'INATIVOS', 'EGRESSOS', 'ATIVOS'.
         motivo_de_evasao (Any, optional): Motivo de evasão. Se não foi informado, use "". Defaults to ""
         gerar_grafico (Any, optional): Tipo do gráfico que o usuário quer gerar, PRECISA ser um desses: 'BARRA', 'PIZZA', 'ROSCA'. Caso o usuário não queira ou não tenha informado, use o padrão vazio ''.

      Returns:
         Informações dos estudantes que ajude a responder a pergunta feita pelo usuário.
   """

   print(f"Tool `obter_dados_de_todos_estudantes` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, situacao_estudante={situacao_estudante} motivo_de_evasao={motivo_de_evasao} e gerar_grafico={gerar_grafico}.")
   query = str(query)
   nome_do_campus = str(nome_do_campus)
   nome_do_curso = str(nome_do_curso)
   situacao_estudante = str(situacao_estudante)
   motivo_de_evasao = str(motivo_de_evasao)
   gerar_grafico = str(gerar_grafico)

   if situacao_estudante in SITUACAO:
      params = {"situacao-do-estudante": situacao_estudante}
   else:
      return ["Por favor informe a situação dos estudantes correta.\n Pode ser uma dessas: SUSPENSOS, REINGRESSOS, REATIVADOS, DESISTENTE, EVADIDOS, JUBILADOS, ABANDONOS, TRANSFERIDOS, FINALIZADOS, INATIVOS, EGRESSOS, ATIVOS"]
   
   if (nome_do_curso != "" and nome_do_campus != ""):
      dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
      params["curso"] = dados_curso['curso']['codigo']
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
      print(len(estudantes))
      estudantes = [estudante for estudante in estudantes if motivo_de_evasao in estudante["motivo_de_evasao"]]
      print(len(estudantes))
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