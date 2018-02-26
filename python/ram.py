#Z80 RAM implementation

class RAM(object):
	def __init__(self):
		#64 kB RAM space
		self.ram = [0] * 65536

	def load(self, rom):
		self.ram = [rom.readMemory(a) for a in range(len(rom))] + self.ram[len(rom):]

	def storeAddr(self, addr, value):
		self.ram[addr] = (value & 0xFF)

	def readAddr(self, addr):
		return self.ram[addr]