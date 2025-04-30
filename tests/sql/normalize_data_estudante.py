from faker import Faker
Faker = Faker('pt_BR')

def normalize_data_estudante(data_json):
    """
    Normaliza os dados do estudante com o faker para incluir os campos que não existem nos dados.
    """

    # Cria uma instância do Faker
    fake = Faker('pt_BR')

    # Campos que não existem nos dados
    campos_adicionais = {
        "nome_do_estudante": fake.name(),
    }

    # Adiciona os campos adicionais a cada dicionário na lista
    for item in data_json:
        for campo, valor in campos_adicionais.items():
            item[campo] = valor

    return data_json