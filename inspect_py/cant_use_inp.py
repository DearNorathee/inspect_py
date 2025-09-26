# the diff between fix_bug vs cant_use is that:
#   fix_bug: you can still use some functionality of it, it's that there's some parameter like(alarm path) that still have the problem
#   cant_use: the main functionality is not correct, or may not work entirely
from inspect_py.utils_inp import *
from inspect_py.sandbox1_inp import *
from typing import List, Tuple, Literal, Union
from pathlib import Path


def run_1_notebook(notebook_path,kernel_name:str = 'python3', notebook_version = 4):
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    import os
    """
    for run single notebook
    """

    # not tested yet
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=notebook_version)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)
    
    try:
        # Execute the notebook
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    except Exception as e:
        print(f"Error executing the notebook {notebook_path}")
        print(e)
        return False
    
    # Save the executed notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    return True

def run_notebook(notebooks:Union[str,List[str]], verbose:int = 1,kernel_name:str = 'python3', notebook_version = 4):
    import python_wizard as pw
    if isinstance(notebooks,str):
        notebooks_in = [notebooks]
    elif isinstance(notebooks,list):
        notebooks_in = list(notebooks)


    if pw.is_list_of_tuple(notebooks):
        # Run each notebook
        for notebook_info  in notebooks_in:
            notebook_name, is_to_run = notebook_info

            if is_to_run:
                if verbose >= 2:
                    print(f"Running {notebook_name}...")
                success = run_1_notebook(notebook,kernel_name = kernel_name, notebook_version = notebook_version)
                if success:
                    if verbose >= 2:
                        print(f"Successfully executed {notebook_name}")
                else:
                    if verbose >= 1:
                        print(f"Failed to execute {notebook_name}")
            else:
                if verbose >= 2:
                    #print skipping
                    print(f"Skipping {notebook_name}...")
    else:
        # Run each notebook
        for notebook in notebooks_in:
            if verbose >= 2:
                print(f"Running {notebook}...")
            success = run_1_notebook(notebook,kernel_name = kernel_name, notebook_version = notebook_version)
            if success:
                if verbose >= 2:
                    print(f"Successfully executed {notebook}")
            else:
                if verbose >= 1:
                    print(f"Failed to execute {notebook}")
    

