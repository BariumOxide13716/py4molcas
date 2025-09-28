

rasscfkwd = {
    # state information
                'SYMM': {'type': [int],
                            'required': False},
                'SPIN': {'type': [int],
                            'required': False},
                'CHARGE': {'type': [int],
                            'required': False},
    # MCSCF parameters
                'NACT': {'type': [list],
                         'required': True},
                'FROZ': {'type': [list],
                            'required': False},
                'INAC': {'type': [list],
                            'required': True},
                'RAS1': {'type': [list],
                          'required': False},
                'RAS2': {'type': [list],
                          'required': True},
                'RAS3': {'type': [list],
                          'required': False},
                'DELE': {'type': [list],
                            'required': False},
                'CIRO' : {'type': [list],
                            'required': True},
                'CION': {'type': [bool],
                            'required': False},
    # GASSCF parameters
                'GASS':{ 'type': [dict],
                         'required': False,
                         'structure':{
                                'n_gas': [int],
                                'orbital_indices': [list],
                                'accumulated_elecs': [int],
                                'accumulated_holes': [int]
                                },
                        },
    # previous orbital files
                'LUMO': {'type': [bool],
                           'required': False},
                'FILE': {'type': [str],
                                'required': False},
                'JOBI': {'type': [bool],
                            'required': False},
    # orbital alternation params
                'ALTE': {'type': [dict],
                         'required': False,
                         'structure':{
                                'n_alter': [int],
                                'orbital_indices': [list]
                                }
                        },
    # geometry optimization params
                'RLXR': { 'type': [int],
                          'required': False},
    
    # MS-PDFT part
                'ROST': {'type': [bool],
                            'required': False},
                'XMSI': {'type': [bool],
                            'required': False},
                'CMSI': {'type': [bool],
                            'required': False},

}