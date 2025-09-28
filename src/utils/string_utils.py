def string_converter(string, target_types):
    """
    Convert a string value to the first one in the target type list.
    If conversion is not possible, return the original string.
    """
    assert isinstance(string, str)
    if isinstance(target_types, type):
        target_types = [target_types]
    for target_type in target_types:
        converted = _string_converter(string, target_type)
        if type(converted) != type(string):
            return converted
    return string

def _string_converter(string, target_type):
    """
    Convert a string to the target type.
    If conversion is not possible, return the original string.
    """
    assert isinstance(string, str)
    try:
        if target_type == bool:
            if string.lower() in ['true', 't', '.true.', '1']:
                return True
            elif string.lower() in ['false', 'f', '.false.', '0']:
                return False
            else:
                return string
        elif target_type == list:
            return string.split()
        return target_type(string)
    except (ValueError, TypeError):
        return string
    
def string_type_finder(string):
    """
    Find the type of a string value.
    The order of types to check is: bool, int, float, str.
    """
    assert isinstance(string, str)
    if string.lower() in ['true', 't', '.true.', '1', 'false', 'f', '.false.', '0']:
        return bool
    try:
        int(string)
        return int
    except ValueError:
        pass
    try:
        float(string)
        return float
    except ValueError:
        pass
    return str

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
