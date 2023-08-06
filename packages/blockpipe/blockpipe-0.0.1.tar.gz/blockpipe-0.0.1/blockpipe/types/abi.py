from collections import namedtuple
from dataclasses import dataclass
from eth_hash.auto import keccak
import eth_abi
from hexbytes import HexBytes


def topic_to_value(topic, stype):
    if stype in ('uint8', 'uint256'):
        return int.from_bytes(topic, 'big')
    elif stype in ('address',):
        return HexBytes(topic[-20:])
    else:
        raise Exception(f'Bad topic_to_value type {stype}')


def data_to_value(data, stype):
    if stype in ('uint8', 'uint64', 'uint256'):
        return data
    elif stype in ('address',):
        return HexBytes.fromhex(data[2:])
    elif stype in ('bytes32',):
        return data
    else:
        raise Exception(f'Bad data_to_value type: {stype}')


def sanitize_type(stype):
    return {
        'uint': 'uint256',
        'int': 'int256',
    }.get(stype, stype)


@dataclass
class LogArg:
    name: str
    stype: str
    indexed: bool


class LogClass:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.argclass = namedtuple(name, [arg.name for arg in args])
        key = f'{name}({",".join((arg.stype for arg in args))})'.encode()
        self.topic0 = HexBytes(keccak(key))

    @classmethod
    def from_decl(cls, decl):
        name = decl.split('(')[0]
        raw_args = [
            v.strip().split() for v in
            decl.split('(')[1].split(')')[0].split(',')
        ]
        args = []
        for raw_arg in raw_args:
            if len(raw_arg) > 2 and raw_arg[1] != 'indexed':
                raise ValueError('Bad event spec')
            args.append(LogArg(raw_arg[-1], sanitize_type(raw_arg[0]), len(raw_arg) > 2))
        return cls(name, args)

    def parse(self, topics, data):
        argvals = [None] * len(self.args)
        indexed_count = 0
        data_types = []
        for idx, arg in enumerate(self.args):
            if arg.indexed:
                indexed_count += 1
                if indexed_count >= len(topics):
                    raise ValueError('Not enough topics')
                argvals[idx] = topic_to_value(topics[indexed_count], arg.stype)
            else:
                data_types.append(arg.stype)
        data_values = eth_abi.decode_abi(data_types, data)
        data_count = 0
        for idx, argval in enumerate(argvals):
            if argval is None:
                argvals[idx] = data_to_value(data_values[data_count], data_types[data_count])
                data_count += 1
        return self.argclass(*argvals)
