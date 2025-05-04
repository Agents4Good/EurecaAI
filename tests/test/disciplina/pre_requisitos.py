import unittest
from ...tools.utils.base_url import URL_BASE
from ...tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina


class TestPreRequisitosValidas(unittest.TestCase):
    def test_pre_requisitos_disciplina_sem_curriculo(self):
        saida_esperada = ["LÓGICA PARA COMPUTAÇÃO"]
        
        resultado = get_pre_requisitos_disciplina(
            nome_da_disciplina="teoria da computação",
            nome_do_curso="ciencia da computacao",
            nome_do_campus="campina grande"
        )
        
        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, str)

        self.assertEqual(saida_esperada, resultado)


    def test_pre_requisitos_disciplina_com_curriculo(self):
        saida_esperada = ["LÓGICA PARA COMPUTAÇÃO"]
        
        resultado = get_pre_requisitos_disciplina(
            nome_da_disciplina="teoria da computação",
            nome_do_curso="ciencia da computacao",
            nome_do_campus="campina grande",
            curriculo="2023"
        )
        
        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, str)

        self.assertEqual(saida_esperada, resultado)


class TestPreRequisitosInvalidas(unittest.TestCase):
    def test_pre_requisitos_disciplina_com_curriculo_invalido(self):        
        resultado = get_pre_requisitos_disciplina(
            nome_da_disciplina="teoria da computação",
            nome_do_curso="ciencia da computacao",
            nome_do_campus="campina grande",
            curriculo="2090"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_pre_requisitos_disciplina_com_curriculo_invalido_nevativo(self):        
        resultado = get_pre_requisitos_disciplina(
            nome_da_disciplina="teoria da computação",
            nome_do_curso="ciencia da computacao",
            nome_do_campus="campina grande",
            curriculo="-2023"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


if __name__ == "__main__":
    unittest.main()