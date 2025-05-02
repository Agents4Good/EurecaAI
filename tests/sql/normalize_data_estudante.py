from faker import Faker

def normalize_data_estudante(data_json):
    """
    Normaliza os dados do estudante com o faker para incluir os campos que não existem nos dados.
    """

    fake = Faker('pt_BR')
    campos_adicionais = {"nome_do_estudante": fake.name()}
    for item in data_json:
        for campo, valor in campos_adicionais.items():
            item[campo] = valor

    return data_json