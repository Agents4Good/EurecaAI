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
  - ano_de_criacao_do_curso
  - codigo_inep
  - modalidade_academica
  - curriculo_atual
  - ciclo_enade
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.

{input}
'''