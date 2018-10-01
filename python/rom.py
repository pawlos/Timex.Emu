#Z80 ROM
import os


class ROM(object):

    def __init__(self, data=None):
        self.rom = bytearray() if data is None else bytearray(data)

    def loadFrom(self, file):
        if os.path.getsize(file) != 16384:
            raise Exception('Wrong rom size. Should be 16K bytes long.')
        f = open(file, 'rb')
        self.rom = bytearray(f.read())

    def __len__(self):
        return len(self.rom)

    def __getitem__(self, index):
        return self.rom[index]

    def __add__(self, data):
        return self.rom + bytearray(data)
