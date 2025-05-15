PROMPT_SQL_ESTUDANTES_INFO_GERAIS = """
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Não invente ou modifique os nomes das colunas.
- Selecione apenas as colunas que foram solicitadas na pergunta, se uma coluna não foi solicitada, não a inclua.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
</RESTRIÇÕES>

Gere uma consulta SQL válida que responda a pergunta:

{input}

"""



# <INSTRUÇÕES ESPECIAIS>
# - Se um campo contém múltiplos valores separados por vírgulas (como deficiências), e a pergunta pede por um desses valores (ex: deficiência B22), use o operador `LIKE` assim:
# "SELECT ... FROM ... WHERE deficiencias LIKE '%,B22,%'
# - Sempre use o padrão `LIKE '%,VALOR,%'` para garantir que o valor está corretamente isolado entre vírgulas.
# </INSTRUÇÕES ESPECIAIS>
