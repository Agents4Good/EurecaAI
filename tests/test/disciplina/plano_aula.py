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
    else:
        return [{"error_status": resultado.status_code, "msg": "Não foi possível obter informação da UFCG."}]


class TestPlanoAulaValido(unittest.TestCase):
    def test_plano_aula_sem_periodo_sem_turma(self): #OK
        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo="2024.2",
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


    def test_plano_aula_sem_periodo_e_com_turma(self): #OK
     
        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo="2024.2",
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


    def test_plano_aula_com_periodo_anterior_e_com_turma(self): #OK
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


    def test_plano_aula_sem_periodo_anterior_e_com_turma(self): #OK

        saida_esperada = get_plano_aula(
            codigo_da_disciplina="1411171",
            periodo="2024.2",     # 2024.1 é pro lsd .2 é pro sti
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
    def test_plano_curso_turma_invalida_limite_menor_que_inferior_igual_a_0(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            turma="0"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_plano_curso_turma_invalida_limite_maior_que_superior_20(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            turma="21"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_plano_curso_periodo_invalido_superior(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="2090.1"
        )
        
        self.assertIsInstance(resultado, list)
        self.assertIsInstance(resultado[0], dict)
        self.assertIn("Não foi possível obter informação da UFCG.", resultado[0]["msg"])
        


    def test_plano_curso_periodo_invalido_inferior(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="1999.2"
        )
        
        self.assertIsInstance(resultado, list)
        self.assertIsInstance(resultado[0], dict)
        self.assertIn("Não foi possível obter informação da UFCG.", resultado[0]["msg"])
        

    def test_plano_curso_periodo_invalido_diferente_padrao(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            periodo="10"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Informe ao usuário o curso não existia nesse período, portanto não é possível obter os dados da disciplina nesse período.", resultado)
       

    def test_plano_curso_curriculo_invalido_diferente_padrao(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="0"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertRegex(resultado, r"Informe ao usuário que este curriculo é inválido e que os disponíveis são: .* e que o curriculo mais recente é o de [0-9]{4}")


    def test_plano_curso_curriculo_invalido_no_padrao(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="2022"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertRegex(resultado, r"Informe ao usuário que este curriculo é inválido e que os disponíveis são: .* e que o curriculo mais recente é o de [0-9]{4}")


    def test_plano_curso_curriculo_invalido_no_padrao_superior(self): #OK
        resultado = get_plano_de_aulas(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computacao",
            nome_da_disciplina="teoria da computacao",
            curriculo="2090"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertRegex(resultado, r"Erro: O período [0-9]{4}\.[0-3] não pode ser anterior ao curriculo de [0-9]{4}. Precisa ser igual ou superior")


if __name__ == "__main__":
    unittest.main()