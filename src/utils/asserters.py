def dict_contains_key(key, dictionary):
    assert isinstance(key, str)
    assert isinstance(dictionary, dict)
    assert key in dictionary.keys()

def value_type_checker(value, expected_types):
    if not isinstance(expected_types, list):
        expected_types = [expected_types]
    assert type(value) in expected_types, \
        f"Value {value} is of type {type(value)}, expected types are {expected_types}."

def list_contains_element(element, lst):
    assert isinstance(lst, list)
    assert element in lst, f"Element {element} is not in the list {lst}."