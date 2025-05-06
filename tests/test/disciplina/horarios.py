import json
import requests
import unittest
from ...tools.utils.base_url import URL_BASE
from ...tools.disciplina.get_horarios_disciplina import get_horarios_disciplina

def get_horarios(codigo_da_disciplina: str, periodo: str, turma: str):
    params = {
        "disciplina": codigo_da_disciplina,
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "turma": turma        
    }
    
    response = requests.get(f"{URL_BASE}/horarios", params=params)   
    if response.status_code == 200:
        horarios = json.loads(response.text)
        
        filtros_horarios = []
        turmas_map = {}
        dias = {"2": "Segunda-feira", "3": "Terça-feira", "4": "Quarta-feira", "5": "Quinta-feira", "6": "Sexta-feira", "7": "Sábado"}

        for horario in horarios:
            turma = horario['turma']
            sala = horario['codigo_da_sala']
            dia = str(horario['dia'])
            dia_nome = dias.get(dia, f"Dia {dia}")
            horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

            if turma not in turmas_map:
                turmas_map[turma] = { 'turma': turma, 'sala': sala, 'horarios': {} }
                filtros_horarios.append(turmas_map[turma])

            turmas_map[turma]['horarios'][dia_nome] = horario_formatado

        return filtros_horarios
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]

    
class TestHorarios(unittest.TestCase):
    def test_buscando_horarios_de_uma_disciplina_sem_periodo_e_sem_turma_2(self): #OK
        saida_esperada = get_horarios(codigo_da_disciplina="1411171", periodo="2024.2", turma="1")

        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação"
        )
        
        print("Resultado", resultado)
        print("Saida esperada", saida_esperada)
        self.assertIsInstance(resultado, list)
        for saida in resultado: self.assertIsInstance(saida, dict)
        self.assertEqual(saida_esperada, resultado)


    def test_buscando_horarios_de_uma_disciplina_com_periodo_e_sem_turma(self): #OK
        saida_esperada = get_horarios(codigo_da_disciplina="1411171", periodo="2024.1", turma="1")

        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1"
        )
        
        print("Resultado", resultado)
        print("Saida esperada", saida_esperada)
        self.assertIsInstance(resultado, list)
        for saida in resultado: self.assertIsInstance(saida, dict)
        self.assertEqual(saida_esperada, resultado)


    def test_buscando_horarios_de_uma_disciplina_sem_periodo_e_com_turma(self): #OK
        saida_esperada = get_horarios(codigo_da_disciplina="1411171", periodo="2024.2", turma="1")

        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            turma="1"
        )
        
        print("Resultado", resultado)
        print("Saida esperada", saida_esperada)
        self.assertIsInstance(resultado, list)
        for saida in resultado: self.assertIsInstance(saida, dict)
        self.assertEqual(saida_esperada, resultado)


    def test_buscando_horarios_de_uma_disciplina_sem_periodo_e_sem_turma_3(self): #OK
        saida_esperada = get_horarios(codigo_da_disciplina="1411171", periodo="2024.1", turma="1")

        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            turma="1"
        )
        
        print("Resultado", resultado)
        print("Saida esperada", saida_esperada)
        self.assertIsInstance(resultado, list)
        for saida in resultado: self.assertIsInstance(saida, dict)
        self.assertEqual(saida_esperada, resultado)


class TestHorariosInvalido(unittest.TestCase):
    def test_buscando_horarios_de_uma_disciplina_com_turma_invalida_igual_0(self): #OK
        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            turma="0"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_buscando_horarios_de_uma_disciplina_com_turma_invalida_igual_negativo(self): #OK
        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            turma="-1"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_buscando_horarios_de_uma_disciplina_com_turma_invalida_igual_21(self): #OK
        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            turma="21"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


    def test_buscando_horarios_de_uma_disciplina_com_turma_invalida_maior_que_21(self): #OK
        resultado = get_horarios_disciplina(
            nome_do_campus="campina grande",
            nome_do_curso="ciencia da computação",
            nome_da_disciplina="teoria da computação",
            periodo="2024.1",
            turma="100"
        )
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema).", resultado)


if __name__ == "__main__":
    unittest.main()