#Z80 RAM implementation
from utility import Bits


class RAM(object):
    def __init__(self):
        #64 kB RAM space
        self.ram = bytearray([0] * 65536)

    def load(self, rom):
        self.ram = self.ram[0:rom.mapAt] + rom[:] + self.ram[rom.mapAt+len(rom):]

    def loadProgramAt(self, program, startAt):
        with open(program, 'rb') as f:
            program_data = bytearray(f.read())
            self.ram = self.ram[0:startAt] + program_data[:] + self.ram[startAt+len(program):]

    def __setitem__(self, addr, value):
        self.ram[addr] = Bits.limitTo8Bits(value)

    def __getitem__(self, addr):
        return self.ram[addr]
