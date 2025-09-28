from input.module_general import OpenMolcasModules as OMMs
import sys

inpfile = sys.argv[1] if len(sys.argv) > 1 else 'test.inp'

omm = OMMs()

lines = OMMs.openmolcas_input_to_list(inpfile)
#print(lines)

module_list, module_contents = omm.line_list_to_modules(lines)

#print(module_list)
#print(module_contents)

for mod, content in zip(module_list, module_contents):
    keywords, values = omm.line_list_to_keywords(content)
    print(f"Module: {mod}")
    print(keywords)
    print(values)

exit()

