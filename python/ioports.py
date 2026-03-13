# IO ports


class IOPorts(object):

    def __init__(self):
        self.ports = [0x00]*0x100

    def __getitem__(self, port):
        return self.ports[port]

    def __setitem__(self, port, value):
        self.ports[port] = value
