

caspt2kwd = {
    # CASPT2 shifts
    'SHIF': {'type': [float],
                'required': False},
    'IPEA': {'type': [float],
                'required': False},
    'IMAG': {'type': [float],
                'required': False},
    'SIG1': {'type': [float],
                'required': False},
    'SIG2': {'type': [float],
                'required': False},
    
    # multistate options
    'MULT': {'type': [dict, str],
                'required': False,
                'allowed_value': ['all'],
                'structure':{
                        'n_mult': [int],
                        'states': [list]
                }
            },
    'XMUL': {'type': [dict, str],
                'required': False,
                'allowed_value': ['all'],
                'structure':{
                        'n_mult': [int],
                        'states': [list]
                }
            }
}