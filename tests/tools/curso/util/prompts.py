PROMPT_SQL_CURSOS = '''
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - codigo_do_curso
  - nome_do_curso
  - codigo_do_setor
  - nome_do_setor
  - nome_do_campus
  - turno
  - periodo_de_inicio
  - data_de_funcionamento
  - codigo_inep
  - modalidade_academica
  - curriculo_atual
  - ciclo_enade
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

#Dado a tabela a acima, responda:
{input}

Responda com uma consulta SQL válida e mínima.
'''


PROMPT_SQL_ESTUDANTES = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é dos estudantes:
{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - nome_do_estudante
  - matricula_do_estudante
  - turno_do_curso
  - codigo_do_curriculo
  - estado_civil
  - sexo
  - forma_de_ingresso
  - nacionalidade
  - local_de_nascimento
  - naturalidade
  - cor
  - deficiente
  - ano_de_conclusao_ensino_medio
  - tipo_de_ensino_medio
  - cra
  - mc
  - iea
  - periodos_completados
  - prac_renda_per_capita_ate
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Use apenas os atributos que a pergunta informa.
</RESTRIÇÕES>

#Dado a tabela a acima, responda:
{input}

Responda com uma consulta SQL válida e mínima.
"""