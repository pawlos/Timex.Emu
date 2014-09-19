

class Bits(object):
	@staticmethod
	def count(value):
		return bin(value).count('1')

	@staticmethod
	def halfCarrySub(firstByte, secondByte):
		return True if ((firstByte & 0xf) - (secondByte & 0xf)) & 0x10 == 0x10 else False

	@staticmethod
	def halfCarrySub16(firstWord, secondWord):
		return True if max(firstWord, secondWord) - max(secondWord, 1) == 1 else False

	@staticmethod
	def overflow(firstPart, secondPart):
		return True if (secondPart < 0) and (firstPart > 0) else False

	@staticmethod
	def twos_comp(val, bits = 8):
		"""compute the 2's compliment of int value val"""
		if ((val & (1 << ( bits - 1 ))) != 0):
			val = val - (1 << bits )
		return val

	@staticmethod
	def isZero(val):
		return True if val == 0 else False

	@staticmethod
	def paritySet(val):
		return True if Bits.count(val) % 2 == 0 else False

	@staticmethod
	def carryFlag(val):
		return True if val < 0 else False

	@staticmethod
	def signInTwosComp(val, bits = 8):
		return True if Bits.twos_comp(val, bits) < 0 else False

	@staticmethod
	def signFlag(val, bits = 8):
		return Bits.signInTwosComp(val, bits)

	@staticmethod
	def borrow(val, bits = 8):
		return Bits.signInTwosComp(val, bits)

	@staticmethod
	def carryFlag16(oldValue, newValue, bits = 15):
		_1ToBits = 1 << bits
		return True if (oldValue & _1ToBits != 0) and (newValue & _1ToBits == 0) else False 

	@staticmethod
	def limitTo16bits(value):
		return value & 0xFFFF


class IndexToReg(object):
	@staticmethod
	def translate16bit(ind):
		if ind == 0:
			return "BC"
		if ind == 1:
			return "DE"
		if ind == 2:
			return "HL"
		if ind == 3:
			return "SP"