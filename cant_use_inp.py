# the diff between fix_bug vs cant_use is that:
#   fix_bug: you can still use some functionality of it, it's that there's some parameter like(alarm path) that still have the problem
#   cant_use: the main functionality is not correct, or may not work entirely
from inspect_py.utils_inp import *
from inspect_py.sandbox1_inp import *
from typing import List, Tuple, Literal, Union
from pathlib import Path

def func_depend_table(py_code_path: Union[str,Path] ):
    # still have bugs
    # in test_02_utils_pw.py it still returns OrderedDict
    # and not all functions are listed there
    # one thing I could try is use function_names and the limit the searching only withing 1 file(py_code_path) only
    # also if the function has no other dependency label them 'root' in 'dependency' column
    """
    Analyzes a Python file and returns a DataFrame containing the functions
    defined in the file along with their dependencies on other functions
    within the same file.

    Parameters
    ----------
    py_code_path : str
        The path of the Python file (.py) to analyze.

    Returns
    -------
    pd.DataFrame
        A DataFrame with two columns: 'function' and 'dependency', where
        'function' is a function defined in the file and 'dependency' is
        another function within the same file that it depends on.
    """
    import ast
    import pandas as pd

    with open(str(py_code_path), "r") as file:
        tree = ast.parse(file.read(), filename=str(py_code_path))
    
    functions = []
    dependencies = []

    function_names = get_fun_names(py_code_path)

    class FunctionVisitor(ast.NodeVisitor):

        def __init__(self, function_names):
            self.function_names = function_names

        def visit_FunctionDef(self, node):
            function_name = node.name
            self.generic_visit(node)
            built_in_funcs = get_builtin_func()
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        if child.func.id not in built_in_funcs:
                            dependencies.append((function_name, child.func.id))
                    elif isinstance(child.func, ast.Attribute):
                        pass
                        # if child.func.attr not in built_in_funcs:
                        #     dependencies.append((function_name, child.func.attr))
            
            functions.append(function_name)
    
    visitor = FunctionVisitor(function_names)
    visitor.visit(tree)
    
    df = pd.DataFrame(dependencies, columns=['function', 'dependency'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df
