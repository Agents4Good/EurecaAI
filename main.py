import logging
import asyncio
from client.mcp_client import MCPClient


async def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python client.py <path_to_server_script>")
    #     sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server("/home/beatriz/agents4good/EurecaAIMCP/eureca/main.py")  # caminho pro seu servidor
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())