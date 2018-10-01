#Z80 RAM implementation
from utility import Bits


class RAM(object):
    def __init__(self):
        #64 kB RAM space
        self.ram = [0] * 65536

    def load(self, rom):
        self.ram = rom + self.ram[len(rom):]

    def __setitem__(self, addr, value):
        self.ram[addr] = Bits.limitTo8Bits(value)

    def __getitem__(self, addr):
        return self.ram[addr]
