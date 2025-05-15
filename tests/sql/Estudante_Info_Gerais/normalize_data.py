from faker import Faker

def normalize_data_estudante(data_json):
    """
    Normaliza os dados do estudante com o faker para incluir os campos que não existem nos dados.
    """
    fake = Faker('pt_BR')
    for item in data_json:
        Faker.seed(int(item["matricula_do_estudante"]))
        campos_adicionais = {
            "nome": fake.name(), 
            "email": fake.email(), 
            "telefone": fake.phone_number()
        }
        for campo, valor in campos_adicionais.items():
            item[campo] = valor

    return data_json