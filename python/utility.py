from regs import XF, YF, HF, CF, PVF

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
    def halfCarrySub16(firstWord, secondWord):
        return True if max(firstWord, secondWord) \
                       - max(secondWord, 1) == 1 else False

    @staticmethod
    def carryFlagAdd16(oldValue, newValue):
        return oldValue <= 0xfff and newValue >= 0x1000

    @staticmethod
    def overflow(oldValue, newValue, bits=8):
        prev = Bits.from_twos_comp(oldValue, bits)
        curr = Bits.from_twos_comp(newValue, bits)

        return Bits.set() if (prev < 0 and curr >= 0) or (prev >= 0 and curr < 0) else Bits.reset()

    @staticmethod
    def twos_comp(val, bits=8):
        """compute the 2's compliment of int value val"""
        if ((val & (1 << (bits - 1))) != 0):
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
        return value & 0xFFFF

    @staticmethod
    def limitTo8Bits(value):
        return value & 0xFF


class IndexToReg(object):
    @staticmethod
    def translate16Bit(ind, ix=False, iy=False, af=False):
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


class Flags(object):
    @staticmethod
    def cp_flags(cpu, n, old, new, newIn2Comp):
        cpu.SFlag = Bits.isNegative(newIn2Comp)
        cpu.ZFlag = Bits.isZero(new)
        cpu.HFlag = Bits.halfCarrySub(old, new)
        cpu.PVFlag = Bits.set() if Bits.getNthBit(((old ^ n) & (new ^ old)) >> 5, PVF) != 0 else Bits.reset()
        cpu.CFlag = Bits.set() if old < n else Bits.reset()
        cpu.NFlag = Bits.set()
        cpu.XFlag = Bits.getNthBit(n, XF)
        cpu.YFlag = Bits.getNthBit(n, YF)

    @staticmethod
    def dec_flags(cpu, old, new):
        cpu.ZFlag = Bits.isZero(new)
        cpu.SFlag = Bits.isNegative(new)
        cpu.NFlag = Bits.set()
        cpu.PVFlag = Bits.set() if old == 0x80 else Bits.reset()
        cpu.HFlag = Bits.halfCarrySub(old, new)
        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.YFlag = Bits.getNthBit(new, YF)

    @staticmethod
    def sub_flags(cpu, old, newIn2s, new, val):
        ''' all values in 2-s complement format except new '''
        cpu.NFlag = Bits.set()
        cpu.ZFlag = Bits.isZero(newIn2s)
        cpu.SFlag = Bits.isNegative(newIn2s)
        cpu.HFlag = Bits.set() if Bits.getNthBit(old ^ val ^ newIn2s, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((old ^ val) & (newIn2s ^ old)) >> 5), PVF) != 0 else Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)
        cpu.XFlag = Bits.getNthBit(newIn2s, XF)
        cpu.YFlag = Bits.getNthBit(newIn2s, YF)

    @staticmethod
    def add_flags(cpu, old, newIn2S, new, value):
        cpu.SFlag = Bits.isNegative(newIn2S)
        cpu.ZFlag = Bits.isZero(new)
        cpu.YFlag = Bits.getNthBit(new, YF)
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ value ^ new), HF) !=0 else Bits.reset()

        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((old ^ value ^ 0x80) & (value ^ new)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)

    @staticmethod
    def bit_flags(cpu, bitValue, regValue):
        #let f = HF | (self.reg.f() & CF) | (if res == 0 {ZF | PF} else {res & SF}) |
        #    (val & (XF | YF));
        cpu.SFlag = Bits.reset()
        cpu.ZFlag = Bits.set() if bitValue == 0 else Bits.reset()
        cpu.YFlag = Bits.getNthBit(regValue, YF)
        cpu.HFlag = Bits.set()

        cpu.XFlag = Bits.getNthBit(regValue, XF)
        cpu.PVFlag = Bits.set() if bitValue == 0 else Bits.reset()
        #NFlag not affected
        #CFlag not affected
