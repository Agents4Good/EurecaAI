PROMPT_SQL_DISCIPLINA = """
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Assuma que você já tem os dados do Curso carregados na tabela, não precisa se preocupar com curso.
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.

{input}
"""