from typing import List
from dataclasses import dataclass
from hexbytes import HexBytes


def decode_uint(data, pos, size=4):
    return int.from_bytes(data[pos:pos+size], 'big'), pos+size


def decode_topics(data, pos):
    size, pos = decode_uint(data, pos, 1)
    topics = []
    for _idx in range(size):
        topic, pos = HexBytes(data[pos:pos+32]), pos+32
        topics.append(topic)
    return topics, pos


def decode_data(data, pos):
    size, pos = decode_uint(data, pos, 4)
    return HexBytes(data[pos:pos+size]), pos+size


@dataclass
class BlockMeta:
    block_number: int  # uint32
    timestamp: int  # uint32
    block_hash: HexBytes  # bytes32
    parent_hash: HexBytes  # bytes32

    def to_bytes(self):
        return b''.join([
            int.to_bytes(self.block_number, 4, 'big'),
            int.to_bytes(self.timestamp, 4, 'big'),
            self.block_hash,
            self.parent_hash,
        ])

    @classmethod
    def from_bytes(cls, data, pos):
        block_number, pos = decode_uint(data, pos)
        timestamp, pos = decode_uint(data, pos)
        block_hash, pos = HexBytes(data[pos:pos+32]), pos+32,
        parent_hash, pos = HexBytes(data[pos:pos+32]), pos+32,
        return cls(block_number, timestamp, block_hash, parent_hash), pos


@dataclass
class Log:
    address: HexBytes  # bytes20
    block_number: int  # uint32
    log_index: int  # uint32
    tx_index: int  # uint32
    tx_hash: HexBytes  # bytes32
    timestamp: int  # uint32
    topics: List[HexBytes]  # uint1 + len*bytes32
    data: HexBytes  # uint32 * len

    @property
    def index(self):
        return (self.block_number, self.log_index)

    def to_bytes(self):
        return b''.join([
            self.address,
            int.to_bytes(self.block_number, 4, 'big'),
            int.to_bytes(self.log_index, 4, 'big'),
            int.to_bytes(self.tx_index, 4, 'big'),
            self.tx_hash,
            int.to_bytes(self.timestamp, 4, 'big'),
            int.to_bytes(len(self.topics), 1, 'big'),
        ] + self.topics + [
            int.to_bytes(len(self.data), 4, 'big'),
            self.data,
        ])

    @classmethod
    def from_bytes(cls, data, pos):
        address, pos = HexBytes(data[pos:pos+20]), pos+20
        block_number, pos = decode_uint(data, pos)
        log_index, pos = decode_uint(data, pos)
        tx_index, pos = decode_uint(data, pos)
        tx_hash, pos = HexBytes(data[pos:pos+32]), pos+32
        timestamp, pos = decode_uint(data, pos)
        topics, pos = decode_topics(data, pos)
        data, pos = decode_data(data, pos)
        return cls(
            address, block_number, log_index,
            tx_index, tx_hash, timestamp, topics, data,
        ), pos

    @classmethod
    def from_bytes_multi(cls, data, pos):
        logs = []
        while pos < len(data):
            log, pos = cls.from_bytes(data, pos)
            logs.append(log)
        return logs
