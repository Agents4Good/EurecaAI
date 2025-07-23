import aiohttp

async def get_info(token):
    url = "https://eureca.sti.ufcg.edu.br/as/profile"
    headers = {
        "accept": "application/json",
        "token-de-autenticacao": token
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.request("GET", url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print("Erro na requisição:", response.status)
                return None