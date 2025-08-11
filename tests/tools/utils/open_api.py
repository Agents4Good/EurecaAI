import inspect
from fastapi import FastAPI, Body
from pydantic import create_model, BaseModel
from typing import Any, get_origin, get_args, Optional
from tests.tools.disciplina.mcp_disciplina import get_tools_formatted, tools

app = FastAPI(title="MCP API via FastAPI")

formatted_tools = get_tools_formatted(tools)

def create_input_model(func):
    signature = inspect.signature(func)
    fields = {}
    for name, param in signature.parameters.items():
        anno = param.annotation if param.annotation != inspect.Parameter.empty else Any
        default = ... if param.default == inspect.Parameter.empty else param.default
        fields[name] = (anno, default)
    model = create_model(f"{func.__name__.capitalize()}Input", **fields)
    return model

def get_response_model(func):
    sig = inspect.signature(func)
    ret = sig.return_annotation
    if ret == inspect.Signature.empty:
        return None
    
    # Se for tipo genérico como Optional, extrai o tipo real
    origin = get_origin(ret)
    args = get_args(ret)
    
    # Se for Optional[T], pegar só T
    if origin is Optional and args:
        ret = args[0]

    # Se for tipo padrão (dict, list, int, str) ou Pydantic BaseModel, retorna
    # (Aqui simplifico, mas dá para ampliar a checagem)
    if inspect.isclass(ret):
        # Verifica se é BaseModel do Pydantic
        if issubclass(ret, BaseModel):
            return ret
        # Para tipos built-in aceita
        if ret in {dict, list, str, int, float, bool}:
            return ret
    
    return None  # fallback

def make_endpoint(func, input_model, response_model):
    async def endpoint(params: input_model = Body(...)):
        result = func(**params.dict())
        return result
    endpoint.__doc__ = func.__doc__
    return endpoint

for tool in formatted_tools:
    func = tool["execute"]
    tool_name = tool["name"]
    input_model = create_input_model(func)
    response_model = get_response_model(func)
    endpoint = make_endpoint(func, input_model, response_model)
    
    if response_model:
        app.post(f"/{tool_name}", response_model=response_model)(endpoint)
    else:
        app.post(f"/{tool_name}")(endpoint)

print("Rotas disponíveis:")
for route in app.routes:
    print(route.path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
