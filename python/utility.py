

class Bits(object):
	@staticmethod
	def count(value):
		return bin(value).count('1')

	@staticmethod
	def halfCarrySub(firstByte, secondByte):
		return True if ((firstByte & 0xf) - (secondByte & 0xf)) & 0x10 == 0x10 else False

	@staticmethod
	def overflow(firstByte, secondByte):
		return True if (secondByte < 0) and (firstByte > 0) else False

	@staticmethod
	def twos_comp(val, bits = 8):
		"""compute the 2's compliment of int value val"""
		if ((val & (1 << ( bits - 1 ))) != 0):
			val = val - (1 << bits )
		return val

	@staticmethod
	def isZero(val):
		return True if val == 0 else False