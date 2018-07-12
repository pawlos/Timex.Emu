#Z80 ROM
import struct

class ROM(object):
	def __init__(self, logger = None):
		f = open('../rom/tc2048.rom','rb')
		self.rom = bytearray(f.read())
		if len(self.rom) != 16384:
			raise Exception('Wrong rom size. Should be 16K bytes long.')

	def __len__(self):
		return len(self.rom)
	
	def __getitem__(self, index):
		return self.rom[index]