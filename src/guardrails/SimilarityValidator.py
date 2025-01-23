
from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)
from guardrails import Guard
from typing import Any, Dict, Optional, Callable
from ..utils.text_preprocessor import similarity_between_texts


@register_validator(name="guardrails/teste", data_type="string")
class SimilarityValidator(Validator):
    """
        Validador customizado que faz a verificação da similaridade entre dois textos"
    """
    def __init__(self, texto1: str, texto2: str, match_type: Optional[str] = None, on_fail: Optional[Callable] = None):        
        super().__init__(on_fail=on_fail, match_type=match_type)
        
        self.texto1 = texto1
        self.texto2 = texto2
        
    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """
            Verifia a similiaridade entre dois textos. Caso os textos possuam
            similaridade < 0.5 retorna um FailResult.

            Args:
                value: string
                metadata: dicionário de metadados

            Returns:
               PassResult: passou na validação
               FailResult: não passou na validação
        """
        similarity = similarity_between_texts(self.texto1, self.texto2)
        
        if similarity < 0.5:
            print(f"{value}: Similaridade baixa (menor que 0.5)")
            return FailResult(error_message="Erro")
        
        print(f"{value}: Similaridade alta (igual ou acima de 0.5)")
        return PassResult()

guard = Guard().use(
    SimilarityValidator(texto1="texto1", texto2="texjjjjje  dfqweffqe wqto2")
)

try:
    guard.parse("Agente Inteligente").model_validate
    print("Passou no teste de similaridade cosseno!")
except Exception as e:
    print("Ocorreu um erro: ", e)