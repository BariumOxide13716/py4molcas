from input.module_dict import module_name_dict
from input.module_general import OpenMolcasModules as OMMs
import sys

inpfile = sys.argv[1] if len(sys.argv) > 1 else 'test.inp'

module_dicts = {}

lines = OMMs.openmolcas_input_to_list(inpfile)
#print(lines)

module_list, module_contents = OMMs.line_list_to_modules(lines)

#print(module_list)
#print(module_contents)

imod = -1
for mod, content in zip(module_list, module_contents):
    imod += 1
    module_dicts[imod] = module_name_dict[mod]()
    print(f"Module {imod}: {mod}")
    print(content)
    keywords, values = module_dicts[imod].line_list_to_keywords(content)
    for kwd, val in zip(keywords, values):
        #print(f"  {kwd}: {val}")
        module_dicts[imod].set_value_from_list(kwd, val)
    #print(module_dicts[str(imod)].module_kwd)
    module_dicts[imod].show_keywords()
print()

exit()

