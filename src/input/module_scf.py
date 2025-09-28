from .ks_dft_list import ks_dft_list


scfkwd = {
                'UHF': {'type': [bool],
                        'required': False},
                'SPIN': {'type': [int],
                         'required': False},
                'ZSPIN': {'type': [int],
                          'required': False},
                'CHAR': {'type': [int],
                            'required': False},
                'KSDFT': {'type': [str],
                          'required': False,
                          'allowed_value': ks_dft_list},
                'LUMORB': {'type': [bool],
                           'required': False},
                'FILEORB': {'type': [str],
                             'required': False}
            }