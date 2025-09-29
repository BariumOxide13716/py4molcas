def string_converter(string, target_types):
    """
    Convert a string value to the first one in the target type list.
    If conversion is not possible, return the original string.
    order of types: int, float, list/str
    """
    assert isinstance(string, str)
    if isinstance(target_types, type):
        if target_types == list:
            return string.split(), True
        target_types = [target_types]
    for target_type in target_types:
        converted, if_converted = _string_converter(string, target_type)
        if if_converted:
            return converted, True
    return string, False

def _string_converter(string, target_type):
    """
    Convert a string to the target type in [int, float, bool]
    For other types, return to string as is.
    If conversion is not possible, return the original string.
    """
    assert isinstance(string, str)
    if target_type == int:
        try:
            return int(string), True
        except ValueError:
            return string, False
    elif target_type == float:
        try:
            return float(string), True
        except ValueError:
            return string, False
    elif target_type == bool:
        if string.lower() in ['true', 't', '.true.', '1']:
            return True, True
        elif string.lower() in ['false', 'f', '.false.', '0']:
            return False, True
        else:
            return string, False
    elif target_type == list:
        return string.split(), True
    else:
        return string, False
    
   

def list_contains_string(string, lst, ignore_case=False, matching_start=False):
    assert isinstance(string, str)
    assert isinstance(lst, list)
    if ignore_case:
        string = string.lower()
        lst = [item.lower() if isinstance(item, str) else item for item in lst]
    if matching_start:
        for item in lst:
            if isinstance(item, str) and string.startswith(item):
                return True
        return False
    return string in lst

def find_string_in_list(orig_string, orig_lst, ignore_case=False, matching_start=False):
    """
     Find a string in a list, return the first matched element.
     If ignorecase is True, ignore case when comparing, but returning to the original case.
     """
    assert isinstance(orig_string, str)
    assert isinstance(orig_lst, list)
    if ignore_case:
        string = orig_string.lower()
        lst = [item.lower() if isinstance(item, str) else item for item in orig_lst]
    else:
        string = orig_string
        lst = orig_lst

    if matching_start:
        for orig_item, item in zip(orig_lst, lst):
            if isinstance(item, str) and string.startswith(item):
                return orig_item
        return None
    
    for orig_item, item in zip(orig_lst, lst):
        if string == item:
            return orig_item
    return None


def string_converter_with_value(string, allowed_types, allowed_values=[]):
    """
    Converting a string to the value of a keyword, by mimicking human reading.
    First split the string to a list, obtain the number of elements in the list.
    If the number of elements > 1, check if list is in allowed types. If so, return the list and True; if not,
    check if str is in allowed types, if so, return the string and True, otherwise return string and False.
    If the number of elements is 1, loop over each type in allowed_types.
    Try to convert the string to the type. 
    If conversion is successful, when the allowed_values is provided, check
    if the converted value is one of the allowed values, if so, return the allowed value and True, otherwise
    continue to the next type; when the allowed values is not provided, continue to the next type. 
    If the conversion fails, continue to the next type.
    If all types are checked, return the string and False.
    """

    if isinstance(allowed_types, type):
        allowed_types = [allowed_types]
    assert isinstance(allowed_types, list)
    assert all([isinstance(t, type) for t in allowed_types]), "allowed_types should be a type or a list of types."
    if allowed_values is None:
        allowed_values = []
    assert isinstance(allowed_values, list)

    if string is None or string == '':
        if bool in allowed_types:
            return False, True
        else:
            return string, False
    
    if not isinstance(string, str):
        return string, True
    
    assert isinstance(string, str)
    
    my_list = string.split()
    n_elem = len(my_list)

    if n_elem > 1:
        if list in allowed_types:
            return my_list, True
        elif str in allowed_types:
            return string, True
        else:
            return string, False
    else:
        for t in allowed_types:
            converted, if_converted = _string_converter(string, t)
            if if_converted:
                if allowed_values:
                    if converted in allowed_values:
                        return converted, True
                else:
                        return converted, True
    return string, False