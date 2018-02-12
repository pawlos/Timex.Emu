import struct

class FakeRom(object):
	
	def __init__(self, romdata):
		self.data = romdata

	def readMemory(self, index):
		return struct.unpack("B", self.data[index])[0]

class FakeRam(object):

	def __init__(self, ramdata=[]):
		self.ram = ramdata

	def readAddr(self, addr):
		return self.ram[addr]

	def storeAddr(self, addr, value):
		self.ram[addr] = value & 0xFF


class FakeCpu(object):

	def __init__(self):
		self.logger = None
