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
    
# reader, setter, and printer for each keyword can be added here
# boolean
    def set_bool_keyword(self, key, value=True):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [bool])
        if 'allowed_value' in self.module_kwd[key]:
            list_contains_element(value, self.module_kwd[key]['allowed_value'])
        self.keywords[key] = value
    
    @staticmethod
    def bool_to_molcas_input(key, value=True):
        return f"{key}" if value else None
    
# integer, float, and string
    def set_keyword_single_value_from_string(self, key, value):
        dict_contains_key(key, self.module_kwd)
        assert isinstance(value, str)
        allowed_types = self.module_kwd[key]['type']
        value = string_converter(value, allowed_types)
        value_type_checker(value, allowed_types)
        if 'allowed_value' in self.module_kwd[key]:
            list_contains_element(value, self.module_kwd[key]['allowed_value'])
        self.keywords[key] = value

    def set_keyword_int(self, key, value):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [int])
        if 'allowed_value' in self.module_kwd[key]:
            list_contains_element(value, self.module_kwd[key]['allowed_value'])
        self.keywords[key] = value
    
    def set_keyword_float(self, key, value):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [float])
        if 'allowed_value' in self.module_kwd[key]:
            list_contains_element(value, self.module_kwd[key]['allowed_value'])
        self.keywords[key] = value
    
    def set_keyword_str(self, key, value):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [str])
        if 'allowed_value' in self.module_kwd[key]:
            list_contains_element(value, self.module_kwd[key]['allowed_value'])
        self.keywords[key] = value

    @staticmethod
    def single_value_to_molcas_input(key, value):
        value_str = string_converter(value)
        return f"{key} = {value_str}" if value_str is not None else None
    
# list
    def set_keyword_list_from_str(self, key, value_string):
        value_type_checker(value_string, [str])
        return self.set_keyword_list_from_list(key, value_string.split())
    
    def set_keyword_list_from_list(self, key, value):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [list])
        new_list = []
        if 'subtype' in self.module_kwd[key]:
            subtypes = self.module_kwd[key]['subtype']
            for elem in value:
                elem = string_converter(elem, subtypes)
                new_list.append(elem)
        else:
            new_list = [string_type_finder(elem)(elem) for elem in value]
        self.keywords[key] = new_list

    @staticmethod
    def list_to_molcas_input(key, value):
        assert isinstance(value, list)
        assert all(isinstance(item, (int, float, str)) for item in value)
        if len(value) == 0:
            return None
        value_str = ' '.join([string_converter(item) for item in value])
        return f"{key} = {value_str}" if value_str is not None else None

# multiline
    def set_keyword_multiline_from_input_list(self, key, input_list):
        assert isinstance(input_list, list)        
        n_lines = len(input_list)
        n_line_written = int(input_list[0])
        assert n_lines == n_line_written + 1, \
            f"The first element of the input list for key {key} should be the number of lines to write, "\
            f"but got {n_line_written} and {n_lines} lines."

        self.set_keyword_multiline_from_list(key, input_list[1:])
    
    def set_keyword_multiline_from_list(self, key, value):
        dict_contains_key(key, self.module_kwd)
        value_type_checker(value, [list])
        assert all(isinstance(item, str) for item in value)

        self.keywords[key] = value

    @staticmethod
    def multiline_to_molcas_input(key, value):
        assert isinstance(value, list)
        assert all(isinstance(item, str) for item in value)
        if len(value) == 0:
            return None
        n_lines = len(value)
        lines = [f"{key} = {n_lines}"]
        lines.extend(value)
        return '\n'.join(lines) if lines is not None else None

    # subkey
    def set_keyword_subkey_from_input_list(self, key, input_list):
        assert isinstance(input_list, list)        
        dict_contains_key(key, self.module_kwd)
        value_type_checker(input_list, [list])
        assert 'subkey' in self.module_kwd[key], \
            f"Keyword {key} does not have subkey definition."
        assert "END OF" in input_list[-1], \
            f"The last element of the input list for key {key} should be 'END OF {key}', "\
            f"but got '{input_list[-1]}'."
        
        subkey_dict = self.module_kwd[key]['subkey']
        subkeys, subvalues = OpenMolcasModules.convert_list_to_k_v_lists(
            input_list,
            new_line_strings=list(subkey_dict.keys())
        )

        subdict = {}
        for subk, subv in zip(subkeys, subvalues):
            dict_contains_key(subk, subkey_dict)
            allowed_types = subkey_dict[subk]['type']
            n_value = len(subv)
            if n_value == 0:
                assert list_contains_element(bool, allowed_types), \
                    f"Subkey {subk} requires a value."
                subdict[subk] = True
            elif n_value == 1:
                converted = string_converter(subv[0], allowed_types)
                value_type_checker(converted, allowed_types)
                subdict[subk] = converted
            else:
                subdict[subk] = subv
            
        self.keywords[key] = subdict



