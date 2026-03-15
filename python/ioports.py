# IO ports


class IOPorts(object):

    def __init__(self):
        self.ports = [0x00]*0x100
        self._read_handlers = {}
        self._write_handlers = {}

    def on_read(self, port, handler):
        self._read_handlers[port] = handler

    def on_write(self, port, handler):
        self._write_handlers[port] = handler

    def __getitem__(self, port):
        if port in self._read_handlers:
            return self._read_handlers[port]()
        return self.ports[port]

    def read(self, port, high_byte=0):
        if port in self._read_handlers:
            return self._read_handlers[port](high_byte)
        return self.ports[port]

    def __setitem__(self, port, value):
        self.ports[port] = value
        if port in self._write_handlers:
            self._write_handlers[port](value)
