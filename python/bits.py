# Z80 bit manipulation utilities


class Bits(object):
    @staticmethod
    def set():
        return True

    @staticmethod
    def reset():
        return False

    @staticmethod
    def flip(val):
        return not val

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
    def halfCarryAdd(firstByte, secondByte):
        return True if ((firstByte&0xf) + (secondByte&0xf))&0x10 == 0x10 else False

    @staticmethod
    def halfCarrySub(firstByte, secondByte):
        return True if ((firstByte & 0xf)
                       - (secondByte & 0xf)) \
                       & 0x10 == 0x10 else False

    @staticmethod
    def overflow(oldValue, newValue, bits=8):
        prev = Bits.from_twos_comp(oldValue, bits)
        curr = Bits.from_twos_comp(newValue, bits)

        return Bits.set() if (prev < 0 and curr >= 0) or (prev >= 0 and curr < 0) else Bits.reset()

    @staticmethod
    def twos_comp(val, bits=8):
        """compute the 2's compliment of int value val"""
        if ((val & (1 << bits)) != 0):
            val = ((1 << bits) - 1) & val
        return val

    @staticmethod
    def from_twos_comp(val, bits=8):
        if val & (1 << (bits - 1)):
            return val - (1 << bits)
        else:
            return val

    @staticmethod
    def isZero(val):
        return val == 0

    @staticmethod
    def isEvenParity(val):
        return Bits.count(val) % 2 == 0

    @staticmethod
    def carryFlag(val, bits=8):
        return (val >> bits) != 0

    @staticmethod
    def isNegative(val, bits=8):
        '''value provided is in a 2's component format'''
        return Bits.set() if val >= (1 << (bits - 1)) else Bits.reset()

    @staticmethod
    def signInTwosComp(val, bits=8):
        return True if Bits.from_twos_comp(val, bits) < 0 else False

    @staticmethod
    def signFlag(val, bits=8):
        return Bits.signInTwosComp(val, bits)

    @staticmethod
    def borrow(val, bits=8):
        return Bits.signInTwosComp(val, bits)

    @staticmethod
    def carryFlag16(oldValue, newValue, bits=15):
        _1ToBits = 1 << bits
        return True if (oldValue & _1ToBits != 0) \
                       and (newValue & _1ToBits == 0) else False

    @staticmethod
    def limitTo16Bits(value):
        value = Bits.twos_comp(value, 16)
        assert value >= 0, f'{value} should be >= 0'
        return value & 0xFFFF

    @staticmethod
    def limitTo8Bits(value):
        value = Bits.twos_comp(value)
        assert value >= 0, f'{value} should be >= 0'
        return value & 0xFF

    @staticmethod
    def make16bit(high, low):
        return (high << 8) | low
