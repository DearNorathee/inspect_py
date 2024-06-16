

def input_params(function):
    import inspect
    """
    Returns a list of parameter names for the given function.
    """
    signature = inspect.signature(function)
    out_list = [param.name for param in signature.parameters.values()]
    return out_list

def get_fun_names(py_code_path: str):
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

    with open(py_code_path, "r") as file:
        tree = ast.parse(file.read(), filename=py_code_path)

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


def func_depend_table(py_code_path: str):
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

    with open(py_code_path, "r") as file:
        tree = ast.parse(file.read(), filename=py_code_path)
    
    functions = []
    dependencies = []

    function_names = get_fun_names(py_code_path)
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            function_name = node.name
            self.generic_visit(node)
            
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        dependencies.append((function_name, child.func.id))
                    elif isinstance(child.func, ast.Attribute):
                        dependencies.append((function_name, child.func.attr))
            
            functions.append(function_name)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    df = pd.DataFrame(dependencies, columns=['function', 'dependency'])
    
    return df

# Example usage
# df = func_depend_table('path_to_your_python_file.py')
# print(df)


# Example usage
# df = func_depend_table('path_to_your_python_file.py')
# print(df)


# Example usage
# df = func_depend_table('path_to_your_python_file.py')
# print(df)


# Example usage
# df = func_depend_table('path_to_your_python_file.py')
# print(df)
