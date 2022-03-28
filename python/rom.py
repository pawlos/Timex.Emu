#Z80 ROM implementation
from os import path


class ROM(object):
    def __init__(self, data=None, mapAt=0x0):
        self.mapAt = mapAt
        self.rom = bytearray() if data is None else bytearray(data)

    def loadFrom(self, file, validateSize = True):
        if validateSize and path.getsize(file) != 16384:
            raise Exception('Wrong rom size. Should be 16K bytes long.')
        with open(file, 'rb') as f:
            self.rom = bytearray(f.read())

    def __len__(self):
        return len(self.rom)

    def __getitem__(self, index):
        return self.rom[index]

    def __add__(self, data):
        return self.rom + bytearray(data)

    def mapAt(self):
        return self.mapAt
