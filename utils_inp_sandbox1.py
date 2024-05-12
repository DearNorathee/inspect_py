

def input_params(function):
    import inspect
    """
    Returns a list of parameter names for the given function.
    """
    signature = inspect.signature(function)
    out_list = [param.name for param in signature.parameters.values()]
    return out_list