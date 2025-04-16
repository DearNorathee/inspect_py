
# get_all_functions_names
from typing import Union
import numpy as np
from play_audio_file import play_alarm_done, play_audio_file, play_alarm_error
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
                            print(f"{file_names[i]} done!")
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