import json
from typing import Any
import requests
from ..campus.utils import get_campus_most_similar
from ..curso.utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.Estudante_Info_Gerais.prompt import PROMPT_SQL_ESTUDANTES_INFO_GERAIS
from ...sql.Estudante_Info_Gerais.normalize_data import normalize_data_estudante
from ..utils.validacoes import validar_periodo

SITUACAO = ['SUSPENSOS', 'REINGRESSOS', 'REATIVADOS', 'DESISTENTE', 'EVADIDOS', 'JUBILADOS', 'ABANDONOS', 'TRANSFERIDOS', 'FINALIZADOS', 'INATIVOS', 'EGRESSOS', 'ATIVOS']

def obter_dados_gerais_de_todos_estudantes(query: Any, nome_do_curso: Any, nome_do_campus: Any, situacao_estudante: Any, motivo_de_evasao: Any = "", periodo_de_ingresso_de: Any = "", periodo_de_ingresso_ate: Any = "", periodo_de_evasao_de: Any = "", periodo_de_evasao_ate: Any = "") -> list:
   """
      _summary_
      Buscar informações gerais dos estudantes da UFCG com base no(s) curso(s).
      Como quantidade, nome, matrícula, idade, sexo, cor, cra, naturalidade, nacionalidade e local de nascimento.
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
         - Quando vocẽ usar situação do tipo "EGRESSOS" use o motivo de evação como "GRADUADO". 
         - Quando vocẽ usar situação do tipo "ATIVOS" use o motivo de evação como "REGULAR"

         Observação: Lembrando que o campo motivo_de_evasão é opcional e só deve usar quando vier motivo de evasão na pergunta.
         Se a pergunta tiver apenas um período de ingreesso, use o mesmo período nos campos periodo_de_ingresso_de e periodo_de_ingresso_ate.
         Se a pergunta tiver apenas um período de evasão, use o mesmo período nos campos periodo_de_evasão_de e periodo_de_evasão_ate.
         E por favor, se usar essa ferramenta, inclua na resposta os campos que você escolheu nessa ferramenta para complementar a resposta.
         Egressos são os formados e os concluidos são os estudantes que estão prestes a se formar.
         Se ocorrer um erro de período, informe imediatamente ao supervisor para ele perguntar ao usuário para ser mais explícito em relação ao período.
         Cada ano tem 2 períodos.

      Args:
         query: Pergunta feita pelo usuário.
         nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
         nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 
         situacao_estudante: a situação do estudante, PRECISA ser um desses: 'SUSPENSOS', 'REINGRESSOS', 'REATIVADOS', 'DESISTENTE', 'EVADIDOS', 'JUBILADOS', 'ABANDONOS', 'TRANSFERIDOS', 'FINALIZADOS', 'INATIVOS', 'EGRESSOS', 'ATIVOS'.
         motivo_de_evasao (Any, optional): Motivo de evasão. Se não foi informado, use "". Defaults to "".
         periodo_de_ingresso_de (Any, optional): Período de ingresso dos estudantes.
         periodo_de_ingresso_ate (Any, optional): Período de ingresso dos estudantes.
         periodo_de_evasao_de (Any, optional): Período de ingresso dos estudantes.
         periodo_de_evasao_ate (Any, optional): Período de ingresso dos estudantes.

      Returns:
         Informações dos estudantes que ajude a responder a pergunta feita pelo usuário.
   """

   print(f"Tool `obter_dados_de_todos_estudantes` chamada com nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, situacao_estudante={situacao_estudante}, motivo_de_evasao={motivo_de_evasao}, periodo_de_ingresso_de={periodo_de_ingresso_de}, periodo_de_ingresso_ate={periodo_de_ingresso_ate}, periodo_de_evasao_de={periodo_de_evasao_ate}, periodo_de_evasao_ate={periodo_de_evasao_ate}")
   print(f"A query da pergunta foi: {query}")
   query = str(query)
   nome_do_campus = str(nome_do_campus)
   nome_do_curso = str(nome_do_curso)
   periodo_de_ingresso_de = str(periodo_de_ingresso_de)
   periodo_de_ingresso_ate = str(periodo_de_ingresso_ate)
   periodo_de_evasao_de = str(periodo_de_evasao_de)
   periodo_de_evasao_ate = str(periodo_de_evasao_ate)
   situacao_estudante = str(situacao_estudante)
   motivo_de_evasao = str(motivo_de_evasao)
   
   validar_periodos, mensagem = validar_periodo(periodo_de_ingresso_de, periodo_de_ingresso_ate, periodo_de_evasao_de, periodo_de_evasao_ate)
   if not validar_periodos: 
      print("Não passou")
      return mensagem

   print("Passou")

   if situacao_estudante in SITUACAO:
      params = {
         "situacao-do-estudante": situacao_estudante,
         "periodo-de-ingresso-de": periodo_de_ingresso_de,
         "periodo-de-ingresso-ate": periodo_de_ingresso_ate,
         "periodo-de-evasao-de": periodo_de_evasao_de,
         "periodo-de-esavao-ate": periodo_de_evasao_ate
      }
      
      print(params)
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
      estudantes = [estudante for estudante in estudantes if motivo_de_evasao in estudante["motivo_de_evasao"]]
      db_name = "db_estudantes.sqlite"
      gerenciador = GerenciadorSQLAutomatizado("Estudante_Info_Gerais", db_name)
      gerenciador.save_data(estudantes)
      response = gerenciador.get_data(query, PROMPT_SQL_ESTUDANTES_INFO_GERAIS)   
      print("Resposta da tool: ", response, "\n")
      return  f"RESULTADO DO SQL: {response}"
   else:
      return [{"error_status": response.status_code, "msg": response.json()}]