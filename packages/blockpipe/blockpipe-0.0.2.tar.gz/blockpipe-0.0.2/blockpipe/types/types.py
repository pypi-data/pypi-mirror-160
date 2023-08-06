from decimal import Decimal
from hexbytes import HexBytes
import sqlalchemy


class Type:
    '''A class to represent Solidity type inside of a Blockpipe program.'''

    PYTHONTYPE: type
    SQLALCHEMY_COLUMN_TYPE: type

    def get_default(self):
        '''Returns the default value of this PYTHONTYPE.'''
        return self.PYTHONTYPE()

    def clone(self, value):
        '''Returns a new cloned version of the given PYTHONTYPE value.'''
        return value

    def as_solidity_value(self, value):
        '''Convert the value from PYTHONTYPE to something acceptable by Solidity library.'''
        return value  # Default implementation does nothing

    def from_solidity_value(self, value):
        '''Convert the value from what returns from Solidity library to PYTHONTYPE.'''
        return value  # Default implementation does nothing

    def as_sqlalchemy_value(self, value):
        '''Convert the value from PYTHONTYPE to something acceptable by SQLAlchemy.'''
        return value  # Default implementation does nothing

    def from_sqlalchemy_value(self, value):
        '''Convert the value from what returns from SQLAlchemy to PYTHONTYPE.'''
        return value  # Default implementation does nothing


class UnsignedIntegerType(Type):
    PYTHONTYPE = int
    SQLALCHEMY_COLUMN_TYPE: sqlalchemy.Numeric

    def __init__(self, size):
        self.size = size

    def as_sqlalchemy_value(self, value):
        if value < 0 or value >= 2**self.size:
            raise ValueError(f'Value out of u{self.size} range: {value}')
        return Decimal(value)

    def from_sqlalchemy_value(self, value):
        return int(value)

    def __repr__(self):
        return f'U{self.size}'


U8 = UnsignedIntegerType(8)
U16 = UnsignedIntegerType(16)
U32 = UnsignedIntegerType(32)
U64 = UnsignedIntegerType(64)
U128 = UnsignedIntegerType(128)
U256 = UnsignedIntegerType(256)


class FixedBytesType(Type):
    PYTHONTYPE = HexBytes
    SQLALCHEMY_COLUMN_TYPE = sqlalchemy.LargeBinary

    def __init__(self, name, size):
        # TODO: Size check
        self.name = name
        self.size = size

    def get_default(self):
        return HexBytes(b'\00' * self.size)

    def from_solidity_value(self, value):
        return HexBytes(value)

    def from_sqlalchemy_value(self, value):
        return HexBytes(value)

    def __repr__(self):
        return f'{self.name}'


Address = FixedBytesType('Address', 20)
Bytes32 = FixedBytesType('Bytes32', 32)
