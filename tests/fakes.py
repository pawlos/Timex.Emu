import struct

class FakeRom(object):
	
	def __init__(self, romdata):
		self.data = romdata

	def readMemory(self, index):
		return struct.unpack("B", self.data[index])[0]

	def __len__(self):
		return len(self.data)

class FakeRam(object):

	def __init__(self, ramdata=[]):
		self.ram = ramdata

	def load(self, rom):
		self.ram = [rom.readMemory(x) for x in range(len(rom))] + self.ram[len(rom):]

	def readAddr(self, addr):
		return self.ram[addr]

	def storeAddr(self, addr, value):
		self.ram[addr] = value & 0xFF


class FakeCpu(object):

	def __init__(self):
		self.logger = None
