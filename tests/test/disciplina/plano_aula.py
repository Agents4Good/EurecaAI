import json
import unittest
import requests
from ...tools.disciplina.get_plano_de_aulas import get_plano_de_aulas
from ...tools.campus.get_periodo_mais_recente import get_periodo_mais_recente
from ...tools.utils.base_url import URL_BASE

def get_plano_aula(codigo_da_disciplina: str, periodo: str, turma: str):
    params = {
        "disciplina": codigo_da_disciplina,
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "turma": turma
    }
    resultado = requests.get(f"{URL_BASE}/aulas", params=params)
    if resultado.status_code == 200:
        return json.loads(resultado.text)


class TestPlanoAulaValido(unittest.TestCase):
    def test_plano_aula_sem_periodo_sem_turma(self):
        periodo_atual = "2024.1"

        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo=periodo_atual,
            turma=""
        )
        
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciência da computação",
            nome_da_disciplina="teoria da computação"
        )
        
        self.assertIsInstance(resultado, list)
        for aula in resultado: self.assertIsInstance(aula, dict)
        self.assertEqual(saida_esperada ,resultado)


    def test_plano_aula_sem_periodo_e_com_turma(self):
        periodo_atual = "2024.1"
        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo=periodo_atual,
            turma="1"
        )
        
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciência da computação",
            nome_da_disciplina="teoria da computação",
            turma="1"
        )
        
        self.assertIsInstance(resultado, list)
        for aula in resultado: self.assertIsInstance(aula, dict)
        self.assertEqual(saida_esperada ,resultado)


    def test_plano_aula_com_periodo_anterior_e_com_turma(self):
        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo="2023.2",
            turma="2"
        )
        
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciência da computação",
            nome_da_disciplina="teoria da computação",
            turma="2",
            periodo="2023.2"
        )
        
        self.assertIsInstance(resultado, list)
        for aula in resultado: self.assertIsInstance(aula, dict)
        self.assertEqual(saida_esperada ,resultado)


    def test_plano_aula_sem_periodo_anterior_e_com_turma(self):
        periodo_atual = "2024.1"
        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo=periodo_atual,
            turma="2"
        )
        
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciência da computação",
            nome_da_disciplina="teoria da computação",
            turma="2",
        )
        
        self.assertIsInstance(resultado, list)
        for aula in resultado: self.assertIsInstance(aula, dict)
        self.assertEqual(saida_esperada ,resultado)


class TestPlanoAulaInvalido(unittest.TestCase):
    def test_plano_curso_turma_invalida_limite_menor_que_inferior_igual_a_0(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            turma="0"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_plano_curso_turma_invalida_limite_maior_que_superior_20(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            turma="21"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_plano_curso_periodo_invalido_superior(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="2090.1"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_plano_curso_periodo_invalido_inferior(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="1999.2"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_plano_curso_periodo_invalido_diferente_padrao(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="10"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_plano_curso_curriculo_invalido_diferente_padrao(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="0"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_plano_curso_curriculo_invalido_no_padrao(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="2022"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_plano_curso_curriculo_invalido_no_padrao_superior(self):
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="2090"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


if __name__ == "__main__":
    unittest.main()