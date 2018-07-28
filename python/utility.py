class Bits(object):
	@staticmethod
	def set():
		return True

	@staticmethod
	def reset():
		return False

	@staticmethod
	def count(value):
		return bin(value).count('1')

	@staticmethod
	def getNthBit(value, nth):
		return (value & (1 << nth)) >> nth

	@staticmethod
	def setNthBit(value, nth, bit_val):
		if bit_val == 0:
			return (value & ~(1 << nth))
		else:
			return (value | (1 << nth))

	@staticmethod
	def halfCarrySub(firstByte, secondByte):
		return True if ((firstByte & 0xf) - (secondByte & 0xf)) & 0x10 == 0x10 else False

	@staticmethod
	def halfCarrySub16(firstWord, secondWord):
		return True if max(firstWord, secondWord) - max(secondWord, 1) == 1 else False

	@staticmethod
	def carryFlagAdd16(oldValue, newValue):
		return oldValue <= 0xfff and newValue >= 0x1000

	@staticmethod
	def overflow(oldValue, newValue, bits = 8):
		return True if (Bits.twos_comp(oldValue, bits) < 0) and (Bits.twos_comp(newValue, bits) >= 0) else False

	@staticmethod
	def twos_comp(val, bits = 8):
		"""compute the 2's compliment of int value val"""
		if ((val & (1 << ( bits - 1 ))) != 0):
			val = val - (1 << bits )
		return val

	@staticmethod
	def isZero(val):
		return val == 0

	@staticmethod
	def isEvenParity(val):
		return Bits.count(val) % 2 == 0

	@staticmethod
	def carryFlag(val, bits = 8):
		return val >= (1 << bits) or Bits.twos_comp(val, bits) < 0

	@staticmethod
	def isNegative(val, bits = 8):
		return True if Bits.twos_comp(val, bits) < 0 else False

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
	def limitTo16Bits(value):
		return value & 0xFFFF

	@staticmethod
	def limitTo8Bits(value):
		return value & 0xFF


class IndexToReg(object):
	@staticmethod
	def translate16Bit(ind, ix = False, iy = False, af = False):
		if ind == 0:
			return "BC"
		if ind == 1:
			return "DE"
		if ind == 2 and not ix and not iy:
			return "HL"
		if ind == 2 and ix:
			return "IX"
		if ind == 2 and iy:
			return "IY"
		if ind == 3 and not af:
			return "SP"
		if ind == 3 and af:
			return "AF"

	@staticmethod
	def translate8Bit(ind):
		if ind == 0:
			return "B"
		if ind == 1:
			return "C"
		if ind == 2:
			return "D"
		if ind == 3:
			return "E"
		if ind == 4:
			return "H"
		if ind == 5:
			return "L"
		if ind == 7:
			return "A"

class IndexToFlag(object):
	@staticmethod
	def translate(ind):
		if ind == 0:
			return "NZ"
		if ind == 1:
			return "Z"
		if ind == 2:
			return "NC"
		if ind == 3:
			return "C"
		if ind == 4:
			return "NPV"
		if ind == 5:
			return "PV"
		if ind == 6:
			return "NS"
		if ind == 7:
			return "S"
