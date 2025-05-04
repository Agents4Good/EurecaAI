import json
import unittest
import requests
from ...tools.disciplina.get_plano_de_curso_disciplina import get_plano_de_curso_disciplina
from ...tools.campus.get_periodo_mais_recente import get_periodo_mais_recente
from ...tools.utils.base_url import URL_BASE

def get_plano_curso(codigo_da_disciplina: str, periodo: str):
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": codigo_da_disciplina
    }
    result = requests.get(f"{URL_BASE}/planos-de-curso", params=params)
    
    if result.status_code == 200:
        return json.loads(result.text)


class TestPlanoCursoSucesso(unittest.TestCase):
    def test_buscando_plano_de_curso_sem_curriculo_e_sem_periodo(self):
        periodo_corrente = "2024.1" # get_periodo_mais_recente()
        saida_esperada = get_plano_curso("1411171", periodo_corrente)
        
        plano_de_curso = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação"
        )
        
        self.assertIsInstance(plano_de_curso, list)
        for item in plano_de_curso: self.assertIsInstance(item, dict)
        
        self.assertEqual(saida_esperada, plano_de_curso)


    def test_buscando_plano_de_curso_sem_curriculo_e_com_periodo(self):
        periodo_corrente = "2024.1" # get_periodo_mais_recente()
        saida_esperada = get_plano_curso("1411171", periodo_corrente)
        
        plano_de_curso = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo=periodo_corrente
        )
        
        self.assertIsInstance(plano_de_curso, list)
        for item in plano_de_curso: self.assertIsInstance(item, dict)
        
        self.assertEqual(saida_esperada, plano_de_curso)


    def test_buscando_plano_de_curso_com_curriculo_e_sem_periodo(self):
        periodo_corrente = "2024.1" # get_periodo_mais_recente()
        saida_esperada = get_plano_curso("1411171", periodo_corrente)
        
        plano_de_curso = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            curriculo="2023"
        )
        
        self.assertIsInstance(plano_de_curso, list)
        for item in plano_de_curso: self.assertIsInstance(item, dict)
        
        self.assertEqual(saida_esperada, plano_de_curso)


    def test_buscando_plano_de_curso_com_curriculo_e_com_periodo(self):
        periodo_corrente = "2024.1" # get_periodo_mais_recente()
        saida_esperada = get_plano_curso("1411171", periodo_corrente)
        
        plano_de_curso = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            curriculo="2023",
            periodo=periodo_corrente
        )
        
        self.assertIsInstance(plano_de_curso, list)
        for item in plano_de_curso: self.assertIsInstance(item, dict)
        
        self.assertEqual(saida_esperada, plano_de_curso)


class TestPlanoCursoInvalido(unittest.TestCase):
    def test_buscando_plano_de_curso_curriculo_invalido(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            curriculo="2024"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_buscando_plano_de_curso_periodo_invalido(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2090.1",
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_buscando_plano_de_curso_periodo_valido_e_curriculo_invalido(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            curriculo="2024"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_buscando_plano_de_curso_periodo_invalido_e_curriculo_valido(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2090.1",
            curriculo="2023"
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_buscando_plano_de_curso_periodo_invalido_e_curriculo_invalido(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2090.1",
            curriculo="2090"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_buscando_plano_de_curso_periodo_invalido_para_ano(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="1"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_buscando_plano_de_curso_curriculo_invalido_para_ano(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            curriculo="1"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_buscando_plano_de_curso_periodo_invalido_para_ano_e_invalido_para_curriculo_ano(self):        
        resultado = get_plano_de_curso_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="1",
            curriculo="1"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


if __name__ == "__main__":
    unittest.main()