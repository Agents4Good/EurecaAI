import inspect

def get_func_info(skip_args=None):
    """Retorna o nome da função chamadora e seus parâmetros em formato string."""

    if skip_args is None:
        skip_args = {"params", "func_name", "args_values"}

    frame = inspect.currentframe().f_back 
    func_name = frame.f_code.co_name
    args_values = inspect.getargvalues(frame).locals

    parametros_str = ", ".join(
        f"{k}={v!r}" for k, v in args_values.items() if k not in skip_args
    )

    return func_name, parametros_str