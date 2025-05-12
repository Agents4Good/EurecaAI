PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA = '''
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.

{input}
'''