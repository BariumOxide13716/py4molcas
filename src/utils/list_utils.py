def check_list_elements(my_list, allowed_types):
    assert isinstance(my_list, list)
    if isinstance(allowed_types, type):
        assert all([isinstance(type(elem), allowed_types) for elem in my_list])
    elif isinstance(allowed_types, list):
        assert all([isinstance(t, type) for t in allowed_types])
        assert all([type(elem) in allowed_types for elem in my_list])