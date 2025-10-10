import os
import re
from utils.asserters import dict_contains_key, value_type_checker, \
                            list_contains_element
from utils.string_utils import string_converter, list_contains_string,\
                                string_converter_with_value, string_list_converter,\
                                string_matrix_converter
from utils.list_utils import list_to_matrix
from input.module_emil import OpenMolcasEmil as ome

modules = {'&TEMPLATE': 'Template module for testing purposes.',
           '&GATEWAY': 'Geometry, basis set, point group, and other settings.',
           '&SCF': 'Self-consistent field (SCF) calculations.',
           '&RASSCF': 'Restricted active space self-consistent field (RASSCF) calculations.',
           '&CASPT2': 'Complete active space second-order perturbation theory (CASPT2) calculations.',
           "&SEWARD": "Integral calculations."}

templatekwd = {
    'BOOL': {'type': [bool],
                'required': False
                },
    'INT': {'type': [int],
                'required': False,
                'allowed_value': [0, 1, 2]
                },
    'FLOAT': {'type': [float],
                'required': False
                },
    'LIST': {'type': [list],
             'subtype': [int, float, str], # put str in the last place
                'required': False
                },
    'BLOCK': {'type': [list],
                'required': False,
                'nsubblock': 2,
                'block': [[list], [list]],  # each element in the list is a list of values in that line
                'subtype': [[int], [float]]  # each element in the subtype is a list of allowed types for each value in that line
            },
    'SUBKEY': {'type': [dict],
                 'required': False,
                'subkey': {'SK1': {'type': [int],
                                     'allowed_value': [0, 1, 2]},
                            'SK2': {'type': [bool]},
                            'SK3': {'type': [list],
                                    'subtype': [int]}}
                            },
    'SPECIAL': {'type': [dict],
                'required': False,
                'special': {'n_block': [int],
                            'key1': [list],
                            'key2': [list]}
                            }
}

class OpenMolcasModules():
    emil_commands = ome.emil_commands
    comment_chars = ['*']
    modules = modules
    emil_name = 'emil'
    block_name = 'block'
    subkey_name = 'subkey'
    special_name = 'special'
    def __init__(self):
        self.module_name = "TEMPLATE"
        self.module_kwd = templatekwd
        self.keywords = {}


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
            if line.startswith(tuple(OpenMolcasModules.comment_chars)):
                continue
            if line == '':
                continue
            line = re.split(r'[=;]+', line)
            new_lines.extend(line)
        #print(new_lines)
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
                checker_for_same_line = False
            elif list_contains_string(line[0], same_line_strings, ignore_case=True, matching_start=True):
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

    @staticmethod
    def line_list_to_modules(input_list):
        return OpenMolcasModules.convert_list_to_k_v_lists(
            input_list,
            new_line_strings=list(OpenMolcasModules.modules.keys()),
            same_line_strings=OpenMolcasModules.emil_commands
        )

    def line_list_to_keywords(self, input_list):
        assert isinstance(input_list, list)
        if input_list[0].strip()[0] in OpenMolcasModules.emil_commands:
            return [OpenMolcasModules.emil_name], input_list
        return OpenMolcasModules.convert_list_to_k_v_lists(
            input_list,
            new_line_strings=list(self.module_kwd.keys())
        )
    
# keyword value getter from a list according to keyword type:

    @staticmethod
    def get_value_from_list_to_single(inplist, allowed_types, allowed_values=None):
        assert isinstance(inplist, list)
        assert all(isinstance(item, str) for item in inplist)
        assert isinstance(allowed_values, list) or allowed_values is None
        assert len(inplist) == 1, "Input list must contain exactly one element for single line."

        value, if_converted = string_converter_with_value(inplist[0], allowed_types, allowed_values)
        assert if_converted, f"Cannot convert '{inplist[0]}' to any of the allowed types {allowed_types} and values {allowed_values}."
        return value
    
    @staticmethod
    def single_value_to_molcas_input_string(key, value):
        assert isinstance(key, str)
        key = key.strip().upper()
        assert isinstance(value, (bool, int, float, str, list))
        if isinstance(value, bool):
            if value:
                return f" {key}\n"
            else:
                return None
        elif isinstance(value, (int, float, str)):
            return f" {key} = {value}\n"
        elif isinstance(value, list):
            value_str = ' '.join(str(v) for v in value)
            return f" {key} = {value_str}\n"
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")
        
    @staticmethod
    def block_value_to_molcas_input_string(key, matrix):
        assert isinstance(key, str)
        key = key.strip().upper()
        assert isinstance(matrix, list)
        assert all(isinstance(row, list) for row in matrix)
        nsubblock = len(matrix)
        nblock = len(matrix[0]) if nsubblock > 0 else 0
        assert nsubblock > 0 and nblock > 0, "Block matrix must have at least one row and one column."

        output = f" {key}\n  {nblock}\n"
        output_list = []
        for i in range(nblock):
            for j in range(nsubblock):
                row = matrix[j][i]
                assert isinstance(row, list)
                row_str = ' '.join(str(v) for v in row)
                output_list.append(f"  {row_str}")

        output += '\n'.join(output_list)
        return output + '\n'

    @staticmethod
    def dict_value_to_molcas_input_string(key,  inp_dict):
        assert isinstance(key, str)
        key = key.strip().upper()
        assert isinstance(inp_dict,  dict)
        output = f" {key}\n"
        for subkey, value in inp_dict.items():
            subkey = subkey.strip().upper()
            assert isinstance(value, (bool, int, float, str, list))
            if isinstance(value, list):
                value_str = ' '.join(str(v) for v in value)
                output += f"  {subkey} = {value_str}\n"
            elif isinstance(value, bool):
                if value:
                    output += f"  {subkey}\n"
            else:
                output += f"  {subkey} = {value}\n"
        output += f" END OF {key}\n"
        return output

    @staticmethod
    def get_value_from_list_to_block(inplist, allowed_types=[[]], nblock=1, nsubblock=1):
        """
        Convert a list of lines to a matrix of lines, with the shape from nblock*nsubblock to (nsubblock, nblock).
        Each line is further converted to the type according to the allowed_types.
        """
        assert isinstance(inplist, list)
        assert isinstance(nblock, int) and nblock >= 1
        assert isinstance(nsubblock, int) and nsubblock >= 1
        assert isinstance(allowed_types, list)
        assert all(isinstance(item, list) for item in allowed_types)
        assert len(allowed_types) == nsubblock, "Length of allowed_types must be equal to nsubblock."
        
        converted_list = []
        line_counter = 0
        block_counter = 0

        inplist = inplist[1:]

        for line_counter in range(len(inplist)):
            line = inplist[line_counter]
            if line_counter % nsubblock == 0 and line_counter > 0:
                block_counter += 1
            subblock_line_counter = line_counter % nsubblock
            converted_line, if_converted = string_converter(line, allowed_types[subblock_line_counter])
            assert if_converted, f"failed to convert input lines to subblock information. "\
            + f"expect {allowed_types[subblock_line_counter]}, got {line}"
            converted_list.append(converted_line)
        converted_matrix = list_to_matrix(converted_list, nblock, nsubblock, coulumn_first=True)
        return converted_matrix

    def set_value_from_list_boolean(self, keyword, values):
        assert isinstance(keyword, str)
        assert isinstance(values, list)
        assert len(values) == 1, f"Keyword '{keyword}' expects a single boolean value, but got {len(values)} values."
        value = values[0]
        dict_contains_key(keyword, self.module_kwd)
        assert bool in self.module_kwd[keyword]['type'], f"Keyword '{keyword}' is not of type bool."
        converted_value, if_converted = string_converter_with_value(value, [bool])
        assert if_converted, f"Cannot convert '{value}' to bool."
        self.keywords[keyword] = converted_value
    
    def set_value_from_list_single(self, keyword, inplist):
        assert isinstance(keyword, str)
        assert isinstance(inplist, list)
        dict_contains_key(keyword, self.module_kwd)
        assert len(inplist) == 1, f"Keyword '{keyword}' expects a single value, but got {len(inplist)} values."
        allowed_types = self.module_kwd[keyword]['type']
        allowed_values = self.module_kwd[keyword].get('allowed_value', None)
        value = OpenMolcasModules.get_value_from_list_to_single(inplist, allowed_types, allowed_values)
        if type(value) == list and 'subtype' in self.module_kwd[keyword]:
            value = string_list_converter(value, self.module_kwd[keyword]['subtype'])
        self.keywords[keyword] = value
    
    def set_value_from_list_block(self, keyword, inplist):
        assert isinstance(keyword, str)
        assert isinstance(inplist, list)
        dict_contains_key(keyword, self.module_kwd)
        nsubblock = self.module_kwd[keyword].get('nsubblock', 1)

        nblock = int(inplist[0])
        assert nblock * nsubblock == len(inplist) - 1, \
            f"Keyword '{keyword}' expects {nblock*nsubblock} lines of values, but got {len(inplist) - 1} lines."

        allowed_types = self.module_kwd[keyword].get('block', [[]]*nsubblock)
        assert len(allowed_types) == nsubblock, \
        f"Keyword '{keyword}' expects {nsubblock} subblocks, but got {len(allowed_types)} types."

        converted_value = OpenMolcasModules.get_value_from_list_to_block(inplist, allowed_types, nblock, nsubblock)
        #print(f"converted_value for {keyword}: {converted_value}")
        if 'subtype' in self.module_kwd[keyword]:
            subtype = self.module_kwd[keyword]['subtype']
            assert len(subtype) == nsubblock, \
            f"Keyword '{keyword}' expects {nsubblock} subblocks, but got {len(subtype)} subtypes."
            converted_matrix = []
            for i in range(nsubblock):
                converted_matrix.append(string_matrix_converter(converted_value[i], subtype[i]))
        else:
            converted_matrix = converted_value
        self.keywords[keyword] = converted_matrix
    
    def set_value_from_list_subkey(self, keyword, inplist):
        assert isinstance(keyword, str)
        assert isinstance(inplist, list)
        assert inplist[-1].strip().startswith('END OF'), f"Subkey block must end with 'END OF {keyword}'."
        inplist = inplist[:-1]  # remove the last line 'END OF ...'
        dict_contains_key(keyword, self.module_kwd)
        dict_contains_key(OpenMolcasModules.subkey_name, self.module_kwd[keyword])
        subkey_dict = self.module_kwd[keyword][OpenMolcasModules.subkey_name]
        
        subkey_list, subkey_contents = OpenMolcasModules.convert_list_to_k_v_lists(
            inplist,
            new_line_strings=list(subkey_dict.keys())
        )
        value_dict = {}
        for sk, content in zip(subkey_list, subkey_contents):
            dict_contains_key(sk, subkey_dict)
            allowed_types = subkey_dict[sk]['type']
            allowed_values = subkey_dict[sk].get('allowed_value', None)
            nline = len(content)
            if nline == 1:
                v = OpenMolcasModules.get_value_from_list_to_single(content, allowed_types, allowed_values)
                if 'subtype' in subkey_dict[sk]:
                    if type(v) is list:
                        v = string_list_converter(v, subkey_dict[sk]['subtype'])
            elif nline == 0:
                assert bool in allowed_types, f"Subkey '{sk}' expects a value, but got none."
                v = True
            else:
                raise ValueError(f"Subkey '{sk}' expects a single value, but got {nline} values.")
                
            value_dict[sk] = v
        self.keywords[keyword] = value_dict
    
    def set_value_from_list_SPECIAL(self, keyword, inplist):
        assert isinstance(keyword, str)
        assert isinstance(inplist, list)
        dict_contains_key(keyword, self.module_kwd)
        dict_contains_key(OpenMolcasModules.special_name, self.module_kwd[keyword])
        special_dict = self.module_kwd[keyword][OpenMolcasModules.special_name]

        special_values = {}
        
        line_counter = 0
        nkeys = 2
        special_values['n_block'] = int(inplist[0])
        special_values['key1'] = []
        special_values['key2'] = []
        for line_counter in range(nkeys):
            line = inplist[line_counter + 1]
            if line_counter % nkeys == 0:
                converted, if_converted = string_converter(line, special_dict['key1'][0])
                assert if_converted
                special_values['key1'] = converted
            else:
                converted, if_converted = string_converter(line, special_dict['key2'][0])
                assert if_converted
                special_values['key2'] = converted
        self.keywords[keyword] = special_values

    def set_value_from_list(self, keyword, inplist):
        assert isinstance(keyword, str)
        assert isinstance(inplist, list)
        
        if len(inplist) == 0:
            self.set_value_from_list_boolean(keyword, [True])
            return
        elif len(inplist) == 1:
            self.set_value_from_list_single(keyword, inplist)
        else:
            dict_contains_key(keyword, self.module_kwd)
            if OpenMolcasModules.block_name in self.module_kwd[keyword]:
                self.set_value_from_list_block(keyword, inplist)
            elif OpenMolcasModules.subkey_name in self.module_kwd[keyword]:
                self.set_value_from_list_subkey(keyword, inplist)
            elif OpenMolcasModules.special_name in self.module_kwd[keyword]:
                if keyword == 'SPECIAL':
                    self.set_value_from_list_SPECIAL(keyword, inplist)
                else:
                    raise NotImplementedError(f"Special handling for keyword '{keyword}' is not implemented.")
            else:
                raise ValueError(f"Keyword '{keyword}' with multiple lines is not recognized as BLOCK, SUBKEY, or SPECIAL.")
        
    def show_keywords(self):
        print(f"Keywords for module {self.module_name}:")
        string_to_print = ""
        for k, v in self.keywords.items():
            if isinstance(v, (bool, int, float, str)):
                string_to_print += f"{OpenMolcasModules.single_value_to_molcas_input_string(k, v)}"
            elif isinstance(v, list) and all(isinstance(row, list) for row in v):
                string_to_print += f"{OpenMolcasModules.block_value_to_molcas_input_string(k, v)}"
            elif isinstance(v, dict) and k != 'SPECIAL':
                string_to_print += f"{OpenMolcasModules.dict_value_to_molcas_input_string(k, v)}"
            else:
                continue
        print(string_to_print)
