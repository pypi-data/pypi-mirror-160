import os
from hexbytes import HexBytes
from collections import defaultdict

from blockpipe.types.abi import LogClass
from blockpipe.types.log import Log


class App:
    def __init__(self):
        self.finalizer = None
        self.handlers = defaultdict(lambda: defaultdict(list))
        self.config = {
            'ROOT': os.environ.get('ROOT'),
            'OUTPUT': os.environ.get('OUTPUT'),
        }

    def run(self):
        if self.finalizer is None:
            raise Exception('No finalizer specified')

        addresses = list(self.handlers.keys())
        if len(addresses) != 1:
            raise Exception('Only support subscribing exactly 1 address')

        with open(os.path.join(self.config['ROOT'], addresses[0].hex() + '.bin'), 'rb') as fp:
            logs = Log.from_bytes_multi(fp.read(), 0)

        for log in logs:
            if len(log.topics) > 0:
                for logcls, func in self.handlers[log.address][log.topics[0]]:
                    func(logcls.parse(log.topics, log.data), log)

        with open(self.config['OUTPUT'], 'w') as fp:
            self.finalizer(fp)

    def log(self, address, abi):
        logcls = LogClass.from_decl(abi)

        def wrapper(func):
            self.handlers[HexBytes(address)][logcls.topic0].append((logcls, func))
            return func
        return wrapper

    def finalize(self, func):
        if self.finalizer is not None:
            raise Exception('Finalizer already specified')

        self.finalizer = func
        return func
