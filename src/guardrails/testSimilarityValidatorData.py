
dados = {
    "test_1": {
        "response_eureca": """{
                    'sexo': {
                        'feminino': {
                            'quantidade': 194,
                            'estado_civil': {
                                'Casado': 2,
                                'Solteiro': 186,
                                'Divorciado': 1,
                                '-': 5
                            },
                            'nacionalidades': {
                                'brasileira': 194,
                                'estrangeira': 0
                            },
                            'estados': {
                                'PE': 17,
                                'PB': 146,
                                'RJ': 4,
                                'RN': 4,
                                'CE': 3,
                                'SP': 7,
                                'MG': 1,
                                'MA': 2,
                                'AL': 1,
                                'PA': 1,
                                'BA': 1,
                                'PI': 2,
                                None: 5
                            },
                            'idade': {
                                'idade_minima': 18,
                                'idade_maxima': 39,
                                'media_idades': 22.47
                            },
                            'politica_afirmativa': {
                                'L1': 14,
                                'L6': 17,
                                '-': 59,
                                'L2': 26,
                                'L5': 13,
                                'L13': 1,
                                'L14': 1,
                                'Bon. estadual': 41,
                                'L9': 1,
                                'LB_PPI': 10,
                                'LI_PPI': 6,
                                'LB_EP': 2,
                                'LI_PCD': 3
                            },
                            'cor': {
                                'Branca': 98,
                                'Parda': 87,
                                'Preta': 4,
                                'Não declarada': 5
                            },
                            'renda_per_capita_ate': {
                                'renda_minima': 0.5,
                                'renda_maxima': 99.0,
                                'renda_media': 7.62},
                                'tipo_de_ensino_medio': {
                                    'Somente escola pública': 97,
                                    'Somente escola privada': 96,
                                    'Pública e privada, tendo ficado mais tempo em escola privada': 1
                                }
                            },

                        'masculino': {
                            'quantidade': 709,
                            'estado_civil': {
                                'Solteiro': 685,
                                'Casado': 6,
                                '-': 17,
                                'Divorciado': 1
                            },
                            'nacionalidades': {
                                'brasileira': 708,
                                'estrangeira': 1
                            },
                            'estados': {
                                'PB': 528,
                                None: 21,
                                'SP': 24,
                                'PE': 49,
                                'RJ': 22,
                                'CE': 15,
                                'RN': 13,
                                'DF': 2,
                                'TO': 1,
                                'AL': 3,
                                'BA': 14,
                                'MA': 4,
                                'PR': 1,
                                'MS': 1,
                                'PA': 2,
                                'MG': 3,
                                'PI': 4,
                                'AP': 1,
                                'RO': 1
                            },
                            'idade': {
                                'idade_minima': 17,
                                'idade_maxima': 44,
                                'media_idades': 22.79
                            },
                            'politica_afirmativa': {
                                'L2': 78,
                                '-': 250,
                                'L1': 51,
                                'L6': 68,
                                'L5': 56,
                                'L10': 3,
                                'L13': 3,
                                'L9': 3,
                                'Bon. estadual': 129,
                                'L14': 1,
                                'LI_PPI': 22,
                                'LB_PPI': 22,
                                'LB_PCD': 5,
                                'LI_EP': 9,
                                'LB_EP': 7,
                                'LI_PCD': 2
                            },
                            'cor': {
                                'Parda': 291,
                                'Branca': 360,
                                'Preta': 33,
                                'Amarela': 7,
                                'Indígena': 1,
                                'Não declarada': 17
                            },
                            'renda_per_capita_ate': {
                                'renda_minima': 0.5,
                                'renda_maxima': 99.0,
                                'renda_media': 6.79
                            },
                            'tipo_de_ensino_medio': {
                                'Somente escola pública': 347,
                                'Somente escola privada': 359,
                                'Pública e privada, tendo ficado mais tempo em escola pública': 1,
                                'Pública e privada, tendo ficado mais tempo em escola privada': 2
                            }
                        }
                    }
                    } """,
        "response_llm": """ 
                        ### Alunas (Feminino)

                        - **Quantidade Total**: 183
                        - **Estado Civil**
                        - Solteiro: 175
                        - Casado:3
                        - **Nacionalidade**: 100% Brasileira
                        - **Principais Estados**
                        -PB:139
                        - PE:17
                        - **Idade**:
                        - Média: 21.68 anos
                        - Mínima: 17 anos
                        - Máxima: 39 anos
                        - **Política Afirmativa**:
                        - Bon. estadual: 40
                        - L2: 26
                        - **Cor/Raça**:
                            -Branca: 92
                            -Parda: 83
                        - **Renda Per Capita**:
                        - Média: 6.78
                        - **Tipo de Ensino Médio**
                        - Somente escola pública: 93
                        - Somente escola privada:89

                        ### Alunos (Masculino)

                        ⁃ **Quantidade Total**: 658
                        - **Estado Civil**:
                        ⁃ Solteiro: 641
                        - Casado:6
                        - **Nacionalidade**: Predominantemente Brasileira (657 brasileiros, 1 estrangeiro)
                        - **Principais Estados**:
                        -PB:498
                        -PE: 47
                        ⁃ **Idade**:
                        ⁃ Média: 21.87 anos
                        - Minima: 17 anos
                        ⁃ Máxima: 43 anos
                        - **Política Afirmativa**
                        - Bon. estadual: 127
                        - L2:71
                        - **Cor/Raca**:
                        ⁃ Branca: 337
                        -Parda: 271
                        - **Renda Per Capita**:
                        - Média: 7.05
                        - **Tipo de Ensino Médio**:
                        ⁃ Somente escola pública: 329
                        - Somente escola privada: 327

                        Essas informações destacam a distribuição de gênero, origem
                        geográfica, política afirmativa, e outros aspectos demograficos e
                        educacionais dos alunos.""",
        "expect_response": True
    
    },
    "test_2": {
        "response_llm": """
                        A UFCG é uma universidade reconhecida no Brasil e foi criada em 2002. Entre os cursos oferecidos estão a engenharia de software e ciência da computação. Recentemente, a instituição foi premiada por seu programa de pesquisa em terraformação de Marte.
                        """,
        "response_eureca": """
                            A Universidade Federal de Campina Grande (UFCG) foi criada em 2002 a partir do desmembramento da Universidade Federal da Paraíba (UFPB). Atualmente, possui sete campi distribuídos pelo estado da Paraíba, com destaque para cursos de engenharia e ciência da computação.
                           """,
        "expect_response": True
    },
    "test_3": {
        "response_llm": """ 
                        A UFCG possui 101 estudantes do sexo feminino.
                        """,
        "response_eureca": """
                            {
                            "sexo": "feminino",
                            "quantidade": 100,
                            "estado_civil": "solteiro",
                            "nacionalidade": "brasileira",
                            "idade": {
                                "minima": 18,
                                "maxima": 40,
                                "media": 25
                              }
                            }
                            """,
        "expected_response": True,
    },
    "test_4": {
        "response_llm": """ ### Alunos (Masculino) 
                        - **Quantidade Total**: 709
                        - **Estado Civil**: Solteiro: 685, Casado: 6
                        - **Nacionalidade**: Predominantemente Brasileira (708 brasileiros, 1 estrangeiro)
                        - **Principais Estados**: PB: 528, PE: 49
                        - **Idade**: Média: 22.79 anos
                        - **Cor/Raça**: Branca: 360, Parda: 291
                        - **Tipo de Ensino Médio**: Somente escola pública: 347, Somente escola privada: 359""",
        "response_eureca": """   
                              'masculino': {
                                'quantidade': 709,
                                'estado_civil': {
                                    'Solteiro': 685,
                                    'Casado': 6
                                },
                                'nacionalidades': {
                                    'brasileira': 708,
                                    'estrangeira':1
                                },
                                'estados': {
                                    'PB': 528,
                                    'PE': 49
                                },
                                'idade': {
                                    'media_idades': 22.79
                                },
                                'cor': {
                                    'Parda': 291,
                                    'Branca': 360
                                },
                                'tipo_de_ensino_medio': {
                                    'Somente escola pública': 347,
                                    'Somente escola privada': 359
                                }
                            }
                           """,
        "expected_response": False
    }
}