import struct
from utility import Bits

class FakeRom(object):
	
	def __init__(self, romdata):
		self.data = romdata

	def readMemory(self, index):
		return struct.unpack("B", self.data[index])[0]

	def __len__(self):
		return len(self.data)

class FakeCpu(object):

	def __init__(self):
		self.logger = None
