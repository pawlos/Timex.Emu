#Z80 RAM implementation

class RAM(object):
	def __init__(self):
		#64 kB RAM sapce
		self.ram = [None] * 65536

	def storeAddr(self, addr, value):
		self.ram[addr] = value

	def readAddr(self, addr):
		return self.ram[addr]