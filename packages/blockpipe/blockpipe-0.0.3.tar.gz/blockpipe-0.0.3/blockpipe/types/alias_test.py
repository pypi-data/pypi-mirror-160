from blockpipe.types.alias import normalize_type


def test_alias_unchanged():
    assert normalize_type('uint64') == 'uint64'


def test_alias_changed():
    assert normalize_type('uint') == 'uint256'
