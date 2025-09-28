import os
import re
import json
from utils.asserters import dict_contains_key, value_type_checker, list_contains_element
from utils.string_utils import string_converter, list_contains_string, string_type_finder


modules = {'&TEMPLATE': 'Template module for testing purposes.',
           '&GATEWAY': 'Geometry, basis set, point group, and other settings.'}

templatekwd = {
    'BOOL': {'type': [bool],
                'required': False},
    'INT': {'type': [int],
                'required': False,
                'allowed_value': [0, 1, 2]},
    'FLOAT': {'type': [float],
                'required': False},
    'LIST': {'type': [list],
             'subtype': [int, float, str], # put str in the last place
                'required': False},
    'MULTILINE': {'type': [list],
                'required': False,
                'multiline': [list]  # each element in the list is a list of values in that line
            },
    'SUBKEY': {'type': [dict],
                 'required': False,
                'subkey': {'SK1': {'type': [int],
                                     'allowed_value': [0, 1, 2]},
                            'SK2': {'type': [bool]},
                            'SK3': {'type': [list]}}
                            },
    'SPECIAL': {'type': [dict],
                'required': False,
                'special': {'n_block': [int],
                            'key1': [list],
                            'key2': [list]}
                            }
}

class OpenMolcasModules():
    def __init__(self):
        self.module_name = "TEMPLATE"
        self.module_kwd = templatekwd
        self.keywords = {}
        OpenMolcasModules.emil_commands = ['>']
        OpenMolcasModules.comment_chars = ['*']
        OpenMolcasModules.modules = modules


    @staticmethod
    def openmolcas_input_to_list(filename):
        assert isinstance(filename, str)
        assert os.path.isfile(filename)
        with open(filename, 'r') as f:
            lines = f.readlines()
        # if a line contains '=' or ';', split it to multiple lines
        new_lines = []
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            line = re.split(r'[=;]+', line)
            new_lines.extend(line)
        print(new_lines)
        return new_lines

    @staticmethod
    def convert_list_to_k_v_lists(input_list, new_line_strings=[], same_line_strings=[]):
        """
        Convert a list of strings to two lists: keys and values.
        Loop over the input list, 
        (1) If a line starts with an element in new_line_string,
        it is considered as a new key, and the following lines are considered as its values
        until another line starts with an element in new_line_string,
        starts with an element in same_line_string,
        or the end of the list is reached;
        (2) If a line starts with an element in same_line_string,
        it is considered as a new key, and the rest of the line is considered as its value,
        and the following lines should either be empty or start with an element 
        in new_line_string or same_line_string;
        (3) If a line does not start with any element in new_line_string 
        or same_line_string,
        it is considered as a continuation of the previous key's value.
        """

        assert isinstance(input_list, list)
        assert all(isinstance(item, str) for item in input_list)
        assert isinstance(new_line_strings, list)
        assert isinstance(same_line_strings, list)

        if not new_line_strings and not same_line_strings:
            raise ValueError("At least one of new_line_strings or same_line_strings must be provided.")

        list_keys = []
        list_values = []
        current_key = None
        current_values = []
        checker_for_same_line = False

        for line in input_list:
            line = line.strip()
            if line == '':
                continue
            if list_contains_string(line, new_line_strings, ignore_case=True, matching_start=True):
                if current_key is not None:
                    list_keys.append(current_key)
                    list_values.append(current_values)
                current_key = line
                current_values = []
            elif list_contains_string(line, same_line_strings, ignore_case=True, matching_start=True):
                if current_key is not None:
                    list_keys.append(current_key)
                    list_values.append(current_values)
                current_key = line[0]
                current_values = [line]
                checker_for_same_line = True
            else:
                if checker_for_same_line:
                    raise ValueError(f"Line '{line}' is not expected after a same-line key '{current_values[0]}'.")
                if current_key is None:
                    raise ValueError(f"Line '{line}' does not belong to any key.")
                current_values.append(line)
                checker_for_same_line = False

        if current_key is not None:
            list_keys.append(current_key)
            list_values.append(current_values)
        return list_keys, list_values

    def line_list_to_modules(self, input_list):
        return OpenMolcasModules.convert_list_to_k_v_lists(
            input_list,
            new_line_strings=list(self.modules.keys()),
            same_line_strings=OpenMolcasModules.emil_commands
        )

    def line_list_to_keywords(self, input_list):
        return OpenMolcasModules.convert_list_to_k_v_lists(
            input_list,
            new_line_strings=list(self.module_kwd.keys())
        )
    
# keyword value getter from a list according to keyword type:
    @staticmethod
    def get_value_from_list(list, allowed_values):
        assert isinstance(list, list)
        assert all(isinstance(item, str) for item in list)
        assert isinstance(allowed_values, list) or allowed_values is None

        if len(list) == 0:
            assert bool in allowed_values, "Empty list is not allowed for this keyword."
            return True  # empty list is considered as True for boolean type
        elif len(list) == 1: