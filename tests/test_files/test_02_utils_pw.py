# v02 => import print_time
from typing import List, Literal, Union, Any, Tuple

def filter_text(input_list:List[str],start_with = "",end_with ="", contain = "", case_sensitive:bool=False) -> List[str]:
    """
    filter a list using text string
    currently only support 1 element of start_with, end_with, contain

    """
    # this is from print_col 
    # !!! TODO start_with, end_with, contain is list
    # add 2 logic options

    
    if start_with != "":
        if case_sensitive:
            out_list = [x for x in input_list if x.startswith(start_with) ]
        else:
            out_list = [x for x in input_list if x.lower().startswith(start_with.lower()) ]
        
    
    if end_with != "":
        if case_sensitive:
            out_list = [x for x in input_list if x.endswith(end_with) ]
        else:
            out_list = [x for x in input_list if x.lower().endswith(end_with.lower()) ]
    
    if contain != "":
        if case_sensitive:
            out_list = [x for x in input_list if contain in x]
        else:
            out_list = [x for x in input_list if contain.lower() in x.lower()]
    
    return out_list

def custom_sort(input_list:List[Any], begin_with, end_with,ascending=True, string_last = True):
    import py_string_tool as pst
    import re
    # medium tested
    
    # what if there's no begin_with or end_with?

    # cover when begin_with is string
    # cover when end_with is string
    
    sort_by = []
    
    have_begin = []
    have_end = []
    
    large_num = 2*len(input_list)
    count = 0
    # ['m.>30', 'b.-30to-20', 'a.<-30', 'l.21to30', 'd.-14to-10', 'j.11to15', 'i.6to10', 'h.1to5', 'e.-9to-5', 'f.-4to-1', 'c.-19to-15', 'g.0', 'k.16to20']
    # check only first element
    if isinstance(input_list[0], str):
        match = re.search(r'[a-zA-Z]\.', input_list[0])
    else:
        # If it's a number 
        match = False
    
    if match:
        sorted_list = sorted(input_list,reverse=not ascending)
        return sorted_list
    for val in input_list:
        try:
            num = float(val)
            sort_by.append(num)
        except ValueError:
            num_02 = val.split(" ")[0]
            num_03 = pst.get_num(num_02)
            
            # string case
            if val in begin_with:
                order_index = -large_num + begin_with.index(val)
                sort_by.append(order_index)
                
            elif val in end_with:
                order_index = large_num + begin_with.index(val)
                sort_by.append(order_index)
                
            else:
                if num_03 is False:
                    
                    # if val not in either begin_with nor end_with
                    if string_last:
                        # put string at the end
                        order_index = large_num + count
                        count += 1
                    else:
                        # put string at the beginning
                        order_index = -large_num + count
                        count += 1
                    sort_by.append(order_index)
                else:
                    sort_by.append(num_03)
                
                    
                    
    # sort_by.sort(reverse = not ascending)

                    
    
    sorted_list = [x for x, y in sorted(zip(input_list, sort_by), key=lambda pair: pair[1])]
    # print(sorted_list01)
    return sorted_list

def filter_dict(myDict,select_key):
    # should be in my lib
    ans = {key: value for key, value in myDict.items() if key in select_key}
    return ans

def reorder_dict(input_dict, new_order):
    from collections import OrderedDict
    return OrderedDict((key, input_dict[key]) for key in new_order)



def is_convertible_to_num(s):
    if isinstance(s,(int,float)):
        return True
    try:
        int(s)
        return True
    except ValueError:
        try:
            float(s)
            return True
        except ValueError:
            return False


def print_time(duration):
    # tested
    hours = duration // 3600
    minutes = (duration % 3600) / 60
    minutes_str = "{:.2f}".format(minutes)
    seconds = duration % 60
    seconds_str = "{:.2f}".format(seconds)
    if hours < 1:
        if minutes > 1:
            # only minutes
            print(f"{minutes_str} minutes", end="\n")
        else:
            # only seconds
            print(f"{seconds_str} seconds", end="\n")
    else:
        # hours with minutes
        print(f"{hours} hour", end=" ")
        print(f"{minutes_str} minutes", end="\n")

def package_version(package_name:str) -> Tuple[int,int,int]:
    # medium tested
    """
    
    Return the version of a Python package as a tuple of integers.
    
    Parameters
    ----------
    package_name : str
        The name of the Python package for which you want to retrieve the version.
    
    Returns
    -------
    package_version_tuple : tuple of ints
        The version of the package as a tuple of integers. If the package is not found,
        the tuple will be (0, 0, 0).
    
    Notes
    -----
    The function uses the `importlib_metadata` module to retrieve the package version
    from the package metadata. If the package is not found, it returns a tuple of (0, 0, 0).
    
    Examples
    --------
    >>> package_version('pandas')
    (1, 4, 3)
    
    >>> package_version('non_existent_package')
    (0, 0, 0)
    """
    import importlib_metadata
    try:
        package_version = importlib_metadata.version(package_name)
    except importlib_metadata.PackageNotFoundError:
        # Handle the case where the package is not found
        package_version = "package is not found"
        return "package is not found"
    
    package_version_tuple = tuple(map(int, package_version.split('.')))
    return package_version_tuple

def flatten(list_of_lists):
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 08_VocabList\VocatList_func01.py"
    """Flatten a 2D list to 1D"""
    return [item for sublist in list_of_lists for item in sublist]


def filter_dict(myDict,select_key):
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 02_Conjugation\Conju_PT.py"
    # should be in my lib
    ans = {key: value for key, value in myDict.items() if key in select_key}
    return ans


def reorder_dict(input_dict, new_order):
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 02_Conjugation\Conju_PT.py"
    from collections import OrderedDict
    return OrderedDict((key, input_dict[key]) for key in new_order)