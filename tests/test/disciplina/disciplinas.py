import unittest
from ...tools.disciplina.get_disciplinas import get_disciplinas

class TestDisciplina(unittest.TestCase):
    def test_consulta_sql_1(self):

        resultado = get_disciplinas(
            query="quantas horas tem a disciplina de teoria da computação do curso de ciencia da computacao do campus de campina grande",
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação"
        )

        print(resultado)

if __name__ == "__main__":
    unittest.main()