PROMPT_SQL_CURSOS = '''
Dada uma pergunta de entrada, crie uma consulta (sqlite) sintaticamente correta para executar e ajudar a encontrar a resposta.

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.

'''

