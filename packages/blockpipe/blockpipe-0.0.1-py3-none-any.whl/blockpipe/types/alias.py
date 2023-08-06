NORMALIZE_MAPPING = {
    'uint': 'uint256',
    'int': 'int256',
}


def normalize_type(input_type):
    '''Returns Solidity type after normalization.'''
    return NORMALIZE_MAPPING.get(input_type, input_type)
