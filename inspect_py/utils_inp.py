
# get_all_functions_names
from typing import Union, Literal
import numpy as np
from play_audio_file import play_alarm_done, play_audio_file, play_alarm_error
from pathlib import Path
# this is for type hint
try:
    Scalar_Numpy = Union[np.number, np.bool_, np.object_, np.string_]
except:
    # error found in numpy >=2
    Scalar_Numpy = Union[np.number, np.bool_, np.object_, np.bytes_]
Scalar_BuiltIn = Union[int, float, str, bool, complex]

Scalar = Union[Scalar_BuiltIn,Scalar_Numpy]

# this is for checking types
try:
    scalar_numpy_type = (np.number, np.bool_, np.object_, np.string_)
    scalar_type = (np.number, np.bool_, np.object_, np.string_,int, float, str, bool, np.number, np.bool_)
except:
    scalar_numpy_type = (np.number, np.bool_, np.object_, np.bytes_)
    scalar_builtin_type = (int, float, str, bool, complex)
    scalar_type = scalar_numpy_type + scalar_builtin_type


def func_depend_table(
    py_code_path: Union[str, Path]
    # , exclude_top_modules: set[str] | None = None
    ,exclude_package:bool = True
    ):
    import ast
    import pandas as pd

    # exclude_top_modules = exclude_top_modules or set()

    src = Path(py_code_path).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(py_code_path))

    # 1) Collect imports ? resolve names to module origins
    class ImportCollector(ast.NodeVisitor):
        def __init__(self):
            self.alias_to_module = {}     # e.g. {'pd': 'pandas'}
            self.name_to_qualname = {}    # e.g. {'is_numeric_dtype': 'pandas.api.types.is_numeric_dtype'}

        def visit_Import(self, node: ast.Import):
            for a in node.names:
                mod = a.name                            # 'pandas'
                asname = a.asname or mod.split('.')[-1] # 'pd' or 'pandas'
                self.alias_to_module[asname] = mod

        def visit_ImportFrom(self, node: ast.ImportFrom):
            base = node.module or ""                   # 'pandas.api.types'
            for a in node.names:
                name = a.name                          # 'is_numeric_dtype'
                asname = a.asname or name
                self.name_to_qualname[asname] = f"{base}.{name}" if base else name

    ic = ImportCollector()
    ic.visit(tree)

    # 2) Local function names
    local_funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    builtins_set = set(dir(__import__("builtins")))

    def attr_to_dotted(node: ast.AST):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
            parts.reverse()
            root = parts[0]
            return root, ".".join(parts)
        return None, None

    rows = []

    class CallCollector(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            fn = node.name
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    f = child.func
                    if isinstance(f, ast.Name):
                        name = f.id
                        if name in builtins_set:
                            continue
                        if name in ic.name_to_qualname:                    # from X import name
                            origin = ic.name_to_qualname[name]             # e.g. pandas.api.types.is_numeric_dtype
                            rows.append((fn, name, origin))
                        elif name in local_funcs:                           # local function
                            rows.append((fn, name, "__local__"))
                        else:
                            rows.append((fn, name, "__unknown__"))
                    elif isinstance(f, ast.Attribute):
                        root, dotted = attr_to_dotted(f)                    # e.g. ('pd','pd.DataFrame')
                        if root and root in ic.alias_to_module:            # import pandas as pd
                            mod = ic.alias_to_module[root]                  # 'pandas'
                            tail = dotted.split('.', 1)[1] if '.' in dotted else ""
                            origin = f"{mod}.{tail}" if tail else mod       # 'pandas.DataFrame'
                            rows.append((fn, dotted, origin))
                        else:
                            # Likely a method call (self.x) or unknown object; skip or mark
                            pass
            self.generic_visit(node)

    CallCollector().visit(tree)

    df = pd.DataFrame(rows, columns=["function", "dependency", "origin"])
    if not df.empty:
        df["top_module"] = df["origin"].str.split(".").str[0]
        df_exclude_package = df.copy()
        df_exclude_package.loc[~df['origin'].isin(['__local__','__unknown__']), 'dependency'] = 'root'
        # df_exclude_package = df.loc[df['origin'].isin(['__local__','__unknown__'])].reset_index(drop=True)
        df_exclude_package = df_exclude_package.drop_duplicates(subset=["function","dependency"]).reset_index(drop=True)
        df_exclude_package = df_exclude_package[['function','dependency']]
        if exclude_package:
            return df_exclude_package
        else:
            return df


def handle_multi_input(
    progress_bar: bool = True
    ,verbose: int = 1
    ,alarm_done: bool = True
    ,alarm_error: bool = True
    ,input_extension: str|None = "all"):
    
    from pathlib import Path
    from typing import Union, List, Callable
    from functools import wraps
    import os_toolkit as ost  # Assuming this is your custom module
    from tqdm import tqdm
    import inspect
    import inspect_py as inp

    """
    Decorator to extend single-file processing functions to handle folders/lists.

    Parameters
    ----------
    progress_bar : bool, default=True
        Whether to show a progress bar when processing folders/lists.
    verbose : int, default=1
        Verbosity level (0=quiet, 1=normal, 2=detailed output).
    alarm_done : bool, default=True
        Play success sound after completion.
    alarm_error : bool, default=True
        Play error sound if processing fails.
    input_extension : Union[List[str], str], default=[".mp3", ".wav"]
        File extensions to process when input is a folder.

    Returns
    -------
    Callable
        Decorated function that now accepts folders/lists.

    Examples
    --------

    >>> def change_title_from_filename(
    >>>    filepaths: str | Path
    >>>    ,output_folder: str|Path

    >>>    # input below would get import automatically
    >>>    ,replace: bool = True
    >>>    ,prefix: str = ""
    >>>    ,suffix: str = ""
    >>>    ,errors:Literal["warn","raise"] = "raise"
    >>>    ,print_errors:bool = False

    >>>    # handle_multi_input parameters
    >>>    ,progress_bar: bool = True
    >>>    ,verbose: int = 1
    >>>    ,alarm_done: bool = True
    >>>    ,alarm_error: bool = True
    >>>    ,input_extension: str|None = "all"
    >>>    ):

    >>>    path_input = {
    >>>        "filepaths":filepaths
    >>>        ,"output_folder":output_folder
    >>>    }

    >>>    handle_multi_input_params = {
    >>>        "progress_bar": progress_bar
    >>>        ,"verbose":verbose
    >>>        ,"alarm_done":alarm_done
    >>>        ,"alarm_error":alarm_error
    >>>        ,"input_extension":input_extension
    >>>    }
    >>>    func_temp = handle_multi_input(**handle_multi_input_params)(vt.change_title_from_filename_1file)
    >>>    result = func_temp(**path_input)
    >>>    return result

    """
    ##### TODO: list of folders are not yet implemented

    # my first decorator
    def decorator(func_1file: Callable):
        @wraps(func_1file)
        def wrapper(
            filepaths: Union[str, Path, list[Union[str, Path]]]
            ,output_folder: str|Path
            ,**kwargs):
            
            # --- Handle Folder ---
            func_input_name = inp.input_params(func_1file)

            if ost.is_folder_path(filepaths):
                file_full_paths = ost.get_full_filename(filepaths, extension=input_extension)
                file_names = ost.get_filename(filepaths, extension=input_extension)
                
                if progress_bar:
                    loop_obj = tqdm(enumerate(file_full_paths), total=len(file_full_paths))
                else:
                    loop_obj = enumerate(file_full_paths)
                
                for i, path in loop_obj:
                    
                    try:
                        if "output_folder" in func_input_name:
                            func_1file(path,output_folder = output_folder, **kwargs)
                        else:
                            func_1file(path, **kwargs)

                        if verbose >= 1:
                            print(f"\n{file_names[i]} done!")
                    except Exception as e:
                        if alarm_error:
                            play_alarm_error()
                        raise e
                
                if alarm_done:
                    play_alarm_done()
            
            # --- Handle List of Files ---
            elif isinstance(filepaths, list):
                for path in filepaths:
                    if "output_folder" in func_input_name:
                        func_1file(path,output_folder = output_folder, **kwargs)
                    else:
                        func_1file(path, **kwargs)
                if alarm_done:
                    play_alarm_done()
            
            # --- Handle Single File ---
            else:
                if "output_folder" in func_input_name:
                    func_1file( filepaths, output_folder = output_folder, **kwargs)
                else:
                    func_1file( filepaths,  **kwargs)
                if alarm_done:
                    play_alarm_done()

        return wrapper
    return decorator


def obj_function(Classobj,print_list=False):
    method_list = [attribute for attribute in dir(Classobj) if callable(getattr(Classobj, attribute)) and attribute.startswith('__') is False]
    if print_list:
        print(method_list)
    return method_list

def obj_property(Classobj,print_list=False):
    property_list = [attribute for attribute in dir(Classobj) if not callable(getattr(Classobj, attribute)) and attribute.startswith('__') is False]
    if print_list:
        print(property_list)
    return property_list


def code_text(filename = ""):
    # little tested
    # no functions needed
    ans = []
    if filename == "":
        _filename = __file__
    with open(_filename) as myFile:
        for num, line in enumerate(myFile, 1):
            ans.append(line)
    return ans

def search_code_index(search, filename = ""):
    # little tested
    # need code_text
    ans = []
    if isinstance(search,str):
        code = code_text(filename)
        for i,line in enumerate(code):
            if search in line:
                ans.append(i+1)
    return ans

def search_code_line(search, filename = ""):
    # little tested
    # need code_text
    ans = []
    if isinstance(search,str):
        code = code_text(filename)
        for i,line in enumerate(code):
            if search in line:
                ans.append(line)
    elif isinstance(search,list):
        for x in search:
            temp = search_code_line(x, filename)
            ans.append(temp)

    return ans

def get_var_name(variable_name,filename = ""):
    # little tested
    # need code_text,search_code_line
    if isinstance(variable_name,str):
        code_line = search_code_line(variable_name,filename)
        _code_line = []

        for line in code_line:
            if (" " in line):
                if line.split(" ")[0] == variable_name:
                    _code_line.append(line)

        _code_line = _code_line[0]
        ans = _code_line.split("=")[1].strip()

    elif isinstance(variable_name,list):
        ans = []
        for variable in variable_name:
            temp = get_var_name(variable,filename)
            ans.append(temp)

    return ans