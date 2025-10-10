# This modules handles the emil commands in OpenMolcas input files.
# Emil commands are treated as modules in this package, although they do not
# actually represent a module in OpenMolcas.
# Emil commands are lines that starts with one or more '>' characters.
# For example:
# >>>>FOREACH
# >>>>COPY


class OpenMolcasEmil():
    emil_commands = ['>']
    
    def __init__(self):
        self.command_line = None

    @staticmethod
    def is_emil_command(line):
        assert isinstance(line, str)
        return line.strip()[0] in OpenMolcasEmil.emil_commands
    
    def line_list_to_keywords(self, input_list): # to be consistent with functions in real modules
        assert isinstance(input_list, list)
        print(f"EMIL input lines: {input_list}")
        return [None], input_list
    
    def set_value_from_list(self, keyword, value_list): # mimicking the behavior in real modules
        _ = keyword
        if isinstance(value_list, list):
            self.command_line = value_list[0] if value_list else None
        elif isinstance(value_list, str):
            self.command_line = value_list
        else:
            raise ValueError("Value should be a list or a string.")
    
    def show_keywords(self):
        assert self.command_line is not None, "EMIL command line is not set."
        print(f"  EMIL command: {self.command_line}")
        return self.command_line
    
