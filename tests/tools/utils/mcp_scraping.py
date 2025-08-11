import inspect

def mcp_scraping(function):
    signature = inspect.signature(function)
    
    return {
        "name": function.__name__,
        "docstring": inspect.getdoc(function),
        "type_return": str(signature.return_annotation),
        "args": [
            {"name": name, "type": str(param.annotation)} 
            for name, param in signature.parameters.items()
        ]
    }


def clean_type(type_str: str) -> str:
    if type_str == "typing.Any":
        return "Any"
    if type_str.startswith("<class '") and type_str.endswith("'>"):
        return type_str[8:-2]
    return type_str


def get_tools_formatted(tools):
    tools_formatted = []
    
    for tool in tools:
        scraping = mcp_scraping(tool)
        
        parameters_schema = {
            "type": "object",
            "properties": {
                arg["name"]: {"type": clean_type(arg["type"])}
                for arg in scraping["args"]
            }
        }
        
        tools_formatted.append({
            "name": scraping["name"],
            "description": scraping["docstring"] or "",
            "parameters": parameters_schema,
            "execute": tool
        })
    
    
    return tools_formatted