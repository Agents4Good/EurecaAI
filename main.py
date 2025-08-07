import logging
from typing import Any
import httpx
from mcp_server import mcp
import disciplina.tools 
from config import USER_AGENT
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Initialize and run the server
    logging.info("RODANDO O SERVER.... ")
    #mcp.run(transport='stdio')
     #uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
    mcp.run(transport="streamable-http")
