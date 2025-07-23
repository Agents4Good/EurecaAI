PROMPT_SQL_ESTAGIO = """
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
- Se a pergunta envolve algum campo que a tabela não tem, ignore esse campo.
- Escreva apenas o comando SQL.
- Ignore informações do 
- Ignore informações do nome do campus na pergunta (não precisa usar o campo de campus da tabela se ele souber o campus, já é feito um pré-processamento nos dados antes de chegar em você. Use o campo campus da tabela se ele não souber).
- Ignore informações do nome do curso na pergunta (não precisa usar o campo de curso da tabela se ele souber o curso, já é feito um pré-processamento nos dados antes de chegar em você. Use o campo curso da tabela se ele não souber).
- Ignore informações do nome do centro ou unidade na pergunta (não precisa usar o capo de campus se ele souber o campus, já é feito um pré-processamento nos dados antes de chegar em você. Use o campo campus da tabela se ele não souber porque).
- Só use a data quando ele especificar o dia ou mês seguido do ano (ignore caso a pergunte informe apenas o ano ao gerar o SQL);
- Fazer apenas um comando SQL que resolva o problem.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.

{input}
"""
