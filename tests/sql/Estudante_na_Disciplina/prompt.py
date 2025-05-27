PROMPT_SQL_ESTUDANTE_NA_DISCIPLINA = '''
Dada uma pergunta de entrada, crie uma consulta (sqlite) sintaticamente correta para executar e ajudar a encontrar a resposta.

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Ignore referências a qualquer tipo de *nome* de disciplina pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Ignore também qualquer trecho da pergunta que pareça incompleto, sem sentido, ambíguo ou não relacionado ao esquema disponível.
</RESTRIÇÕES>

Responda com **somente** uma consulta SQL válida e mínima. **Não inclua explicações, comentários ou raciocínio.**
'''