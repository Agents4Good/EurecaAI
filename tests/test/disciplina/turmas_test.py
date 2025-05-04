import json
import requests
import unittest
from ...tools.utils.base_url import URL_BASE
from ...tools.disciplina.get_turmas_disciplina import get_turmas_disciplina

def get_turmas(codigo_disciplina: str, periodo: str):
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": codigo_disciplina
    }
    response = requests.get(f'{URL_BASE}/turmas', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    
    raise("Ocorreu um erro ao buscar pelas turmas.")
    
def periodo_corrente():
    params = { "campus": 1 }
    response = requests.get(f'{URL_BASE}/calendarios/periodo-corrente', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)[0]["periodo"]

    raise("Ocorreu um erro ao buscar o período corrente.")


class TestTurmasValidas(unittest.TestCase):
    def test_de_curso_usando_periodo_valido_e_sem_curriculo(self):
        codigo_da_disciplina = "1411171" # Teoria da Computação
        periodo_escolhido = "2023.2"
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao", 
            periodo=periodo_escolhido
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


    def test_de_curso_sem_periodo_e_com_curriculo_valido(self):
        codigo_da_disciplina = "1411171" # Teoria da Computação
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            curriculo="2023"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


    def test_de_curso_sem_periodo_e_sem_curriculo(self):
        codigo_da_disciplina = "1411171" # Teoria da Computação
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
        
        
    def test_de_curso_sem_periodo_e_sem_curriculo_laboratorio_estrutura_dados(self):
        codigo_da_disciplina = "1411179" # Laboratório de estrutura de dados
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="laboratório de estrutura de dados", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


    def test_de_curso_sem_periodo_e_sem_curriculo_estrutura_dados(self):
        codigo_da_disciplina = "1411172" # Estrutura de Dados
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="estrutura de dados", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
        
        
    def test_de_curso_sem_periodo_e_sem_curriculo_programacao_1(self):
        codigo_da_disciplina = "1411167" # Programação 1
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="programação 1", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


    def test_de_curso_sem_periodo_e_sem_curriculo_laboratorio_de_programacao_1(self):
        codigo_da_disciplina = "1411180" # Laboratório de Programação 1
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="laboratório de programação 1", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
    
    
    def test_de_curso_sem_periodo_e_sem_curriculo_programacao_i(self):
        codigo_da_disciplina = "1411167" # Programação 1
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="programação i", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
    
    
    def test_de_curso_sem_periodo_e_sem_curriculo_laboratorio_de_programacao_i(self):
        codigo_da_disciplina = "1411180" # Laboratório de Programação i
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="laboratório de programação i", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
        

    def test_de_curso_sem_periodo_e_sem_curriculo_programacao_2(self):
        codigo_da_disciplina = "1411168" # Programação 2
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="programação 2", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


    def test_de_curso_sem_periodo_e_sem_curriculo_laboratorio_de_programacao_2(self):
        codigo_da_disciplina = "1411181" # Laboratório Programação 2
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="laboratório de programação 2", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
        
    
    def test_de_curso_sem_periodo_e_sem_curriculo_programacao_ii(self):
        codigo_da_disciplina = "1411168" # Programação ii
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="programação ii", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
        
    
    def test_de_curso_sem_periodo_e_sem_curriculo_laboratorio_de_programacao_ii(self):
        codigo_da_disciplina = "1411181" # Laboratório de programação ii
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="laboratório de programação ii", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao"
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)
    

    def test_de_curso_com_periodo_e_com_curriculo(self):
        codigo_da_disciplina = "1411171" # Teoria da Computação
        periodo_escolhido = "2024.1" # str(periodo_corrente())
        curriculo_escolhido = "2023"
        
        saida_esperada = get_turmas(codigo_disciplina=codigo_da_disciplina, periodo=periodo_escolhido)
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            periodo=periodo_escolhido,
            curriculo=curriculo_escolhido
        )

        self.assertIsInstance(resultado, list)
        for item in resultado: self.assertIsInstance(item, dict)

        self.assertEqual(saida_esperada, resultado)


class TestTurmasInvalidas(unittest.TestCase):
    def test_de_curso_com_periodo_invalido_e_curriculo_valido(self):
        periodo_escolhido = "2090.1"
        curriculo_escolhido = "2023"
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            periodo=periodo_escolhido,
            curriculo=curriculo_escolhido
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_de_curso_com_periodo_valido_e_curriculo_invalido(self):
        periodo_escolhido = "2024.1"
        curriculo_escolhido = "2024"
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            periodo=periodo_escolhido,
            curriculo=curriculo_escolhido
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


    def test_de_curso_com_periodo_invalido_e_curriculo_invalido(self):
        periodo_escolhido = "2090.1"
        curriculo_escolhido = "2090"
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            periodo=periodo_escolhido,
            curriculo=curriculo_escolhido
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_de_curso_com_periodo_invalido_negativo(self):
        periodo_escolhido = "-2024.1"
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            periodo=periodo_escolhido
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Período inválido. Informe ao usuário que os períodos que ele pode acessar são", resultado)
        self.assertRegex(resultado, r"e que o período mais recente é o de [0-9]{4}\.[0-2]")


    def test_de_curso_com_curriculo_invalido_negativo(self):
        curriculo_escolhido = "-2024"
        
        resultado = get_turmas_disciplina(
            nome_da_disciplina="Teoria da computacao", 
            nome_do_campus="campina grande", 
            nome_do_curso="ciencia da computacao",
            curriculo=curriculo_escolhido
        )

        self.assertIsInstance(resultado, str)
        self.assertIn("Currículo inválido. Informe ao usuário que para o curso", resultado)
        self.assertRegex(resultado, r"e que o mais recente é o currículo de [0-9]{4}")


if __name__ == "__main__":
    unittest.main()