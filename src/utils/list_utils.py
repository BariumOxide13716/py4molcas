def check_list_elements(my_list, allowed_types):
    assert isinstance(my_list, list)
    if isinstance(allowed_types, type):
        assert all([isinstance(type(elem), allowed_types) for elem in my_list])
    elif isinstance(allowed_types, list):
        assert all([isinstance(t, type) for t in allowed_types])
        assert all([type(elem) in allowed_types for elem in my_list])


def list_to_matrix(inplist, m, n, coulumn_first=False):
    # convert a list with lenght m*n to a matrix with m rows and n columns
    # if column_first is True, it means the input list is in column first order
    assert isinstance(m, int) and m > 0
    assert isinstance(n, int) and n > 0
    assert isinstance(inplist, list)
    assert len(inplist) == m * n
    if coulumn_first:
        matrix = [[inplist[i + j*m] for j in range(n)] for i in range(m)]
    else:
        matrix = [inplist[i*n : (i+1)*n] for i in range(m)]
    return matrix

