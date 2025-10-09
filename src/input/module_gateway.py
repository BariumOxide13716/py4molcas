
from .basis_set_list import basis_set_list
from .module_general import OpenMolcasModules as modules
import numpy as np


gatewaykwd = {
        'COORD': {      'type': [ str, int ],
                        'required': True,
                        'structure':{
                                'n_atoms': [int],
                                'comments': [str],
                                'atoms': [str],
                                'coords': [np.ndarray]},
                        },
        'BASI': {'type': [str],
                         'required': True,
                         'allowed_value': basis_set_list
                        },
        'GROU': { 'type': [list],
                  'subtype': [str],
                          'required': True},
                'RICD': { 'type': [bool],
                         'required': False},
                'TEST': { 'type': [bool],
                         'required': False}
        }

class Gateway(modules):
    super.__init__()
    