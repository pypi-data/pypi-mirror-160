from decimal import Decimal
from blockpipe.types.types import U256


def test_types_u256():
    assert U256.PYTHONTYPE == int
    assert U256.as_solidity_value(123) == 123
    assert U256.from_solidity_value(123) == 123
    assert U256.as_sqlalchemy_value(456) == Decimal(456)
    assert U256.as_sqlalchemy_value(Decimal(456)) == 456
