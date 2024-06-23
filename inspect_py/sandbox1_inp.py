from inspect_py.utils_inp import *
from typing import List, Tuple, Literal, Union
from pathlib import Path

def get_builtin_func():
    import builtins
    all_builtin_functions = [name for name in dir(builtins) if callable(getattr(builtins, name))]
    return all_builtin_functions

def input_params(function):
    import inspect
    """
    Returns a list of parameter names for the given function.
    """
    signature = inspect.signature(function)
    out_list = [param.name for param in signature.parameters.values()]
    return out_list

def get_fun_names(py_code_path: Union[str,Path]):
    """
    Analyzes a Python file and returns a list of function names defined in the file.

    Parameters
    ----------
    py_code_path : str
        The path of the Python file (.py) to analyze.

    Returns
    -------
    list of str
        A list containing the names of functions defined in the file.
    """
    import ast

    with open(str(py_code_path), "r") as file:
        tree = ast.parse(file.read(), filename=str(py_code_path))

    function_names = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            function_names.append(node.name)
            self.generic_visit(node)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)

    return function_names

# Example usage
# functions = get_fun_names('path_to_your_python_file.py')
# print(functions)


