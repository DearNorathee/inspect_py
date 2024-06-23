from inspect_py.sandbox1_inp import *
from typing import List, Tuple, Literal, Union
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
# TODO change to relative path in the future as this will throw error when I upload to git
test_folder = Path(r"C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\07 Inspect\inspect_py\tests\test_files")

def test_func_depend_table():
    path01 = r"C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\04 Python Excel Library\excel_toolkit\excel_toolkit\range.py"
    actual01 = func_depend_table(path01)
    expected01 = pd.DataFrame({
                'function': [
                    'find_all_range', 'find_all_range_slow', 'next_text_cell',
                    'next_no_text_cell', 'next_contain_num', 'next_numeric',
                    'next_cell', 'next_cell'
                ],
                'dependency': [
                    'ws_at_WB', 'ws_at_WB', 'next_cell', 'next_cell', 'next_cell',
                    'next_cell', '_offset_val', 'func_bool'
                ]
            })

    path02 = r"C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\06 General Python\python_wizard\python_wizard\utils_pw.py"
    actual02 = func_depend_table(path02)
    expected01 = ""

    assert_frame_equal(actual01,expected01)

def test_get_fun_names():
    
    path01_no_var = test_folder / "test_01_range.py"
    actual01 = get_fun_names(path01_no_var)
    expected01 = ['find_all_range', 'pick_til_end', 'find_all_range_slow', 'next_text_cell', 'next_no_text_cell', 'next_contain_num', 'next_numeric', 'next_cell', '_offset_val']

    path02_no_var = test_folder / "test_02_utils_pw.py"
    actual02 = get_fun_names(path02_no_var)
    expected02 = ['filter_text', 'custom_sort', 'filter_dict', 'reorder_dict', 'is_convertible_to_num', 'print_time', 'package_version', 'flatten', 'filter_dict', 'reorder_dict']

    path03_have_var = test_folder / "test_03_french_audio_shuffle_be_go_have.py"
    actual03 = get_fun_names(path03_have_var)
    expected03 = ['play_audio_slower', 'play_audio']

    # TODO add more useful assert statement
    assert actual01 == expected01
    assert actual02 == expected02
    assert actual03 == expected03

def main():
    test_get_fun_names()
    test_func_depend_table()

if __name__ == "__main__":
    main()
    