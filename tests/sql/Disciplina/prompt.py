PROMPT_SQL_DISCIPLINA = """
Dada uma pergunta de entrada, crie uma consulta (sqlite) sintaticamente correta para executar e ajudar a encontrar a resposta.

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Assuma que você já tem os dados do Curso carregados na tabela, não precisa se preocupar com curso.
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
- Se uma parte da pergunta não estiver representada diretamente nos nomes de coluna, ignore totalmente essa parte, mesmo que você ache que ela seja importante para responder a pergunta.
- Apenas retorne no padrão adequado.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
"""