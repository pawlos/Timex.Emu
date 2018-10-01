# IO ports


class IOPorts(object):

    def __init__(self):
        self.ports = [0x00]*0xff

    def __getitem__(self, port):
        return self.ports[port]

    def __setitem__(self, port, value):
        self.ports[port] = value
