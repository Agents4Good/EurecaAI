import traceback
import httpx
from typing import Any
from config import USER_AGENT

async def make_request(url: str, params: dict) -> dict[str, Any] | None:
    """Faz uma requisição GET com tratamento de erros."""
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()

            print("🟢 Status Code:", response.status_code)
            print("🟢 Content-Type:", response.headers.get("Content-Type"))
            print("🟢 Response Text:", response.text[:300])  # Mostra parte da resposta pra debug
            return response.json()
        except Exception as e:
            print("❌ Erro ao fazer request:")
            traceback.print_exc()
            return None
     