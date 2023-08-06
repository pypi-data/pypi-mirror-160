from blockpipe.types.alias import normalize_type
from blockpipe.types.types import U8, U16, U32, U64, U128, U256, Address, Bytes32


def type_from_string(string_type):
    normalized = normalize_type(string_type)
    return {
        'uint8': U8,
        'uint16': U16,
        'uint32': U32,
        'uint64': U64,
        'uint128': U128,
        'uint256': U256,
        'address': Address,
        'bytes32': Bytes32,
    }[normalized]
