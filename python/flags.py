# Z80 flag computation utilities

from bits import Bits
from regs import XF, YF, HF, PVF, SF


class Flags(object):
    @staticmethod
    def xor_flags(cpu, new):
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(new)
        cpu.SFlag = Bits.isNegative(new)
        cpu.PVFlag = Bits.isEvenParity(new)
        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.YFlag = Bits.getNthBit(new, YF)

    @staticmethod
    def or_flags(cpu, new):
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(new)
        cpu.SFlag = Bits.isNegative(new)
        cpu.PVFlag = Bits.isEvenParity(new)
        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.YFlag = Bits.getNthBit(new, YF)

    @staticmethod
    def and_flags(cpu, new):
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(new)
        cpu.SFlag = Bits.signInTwosComp(new)
        cpu.PVFlag = Bits.isEvenParity(new)
        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.YFlag = Bits.getNthBit(new, YF)

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
        cpu.PVFlag = Bits.set() if new == 0x7f else Bits.reset()
        cpu.HFlag = Bits.set() if Bits.getNthBit(old ^ new, HF) != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.YFlag = Bits.getNthBit(new, YF)

    @staticmethod
    def inc_flags(cpu, old, new):
        cpu.ZFlag = Bits.isZero(new)
        cpu.SFlag = Bits.isNegative(new)
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if new == 0x80 else Bits.reset()
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ new), HF) != 0 else Bits.reset()
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
        cpu.ZFlag = Bits.isZero(newIn2S)
        cpu.YFlag = Bits.getNthBit(new, YF)
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ value ^ newIn2S), HF) !=0 else Bits.reset()

        cpu.XFlag = Bits.getNthBit(new, XF)
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((old ^ value ^ 0x80) & (value ^ new)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)

    @staticmethod
    def bit_flags(cpu, bitValue, regValue, bit):
        cpu.SFlag = Bits.set() if bit == SF and bitValue == 1 else Bits.reset()
        cpu.ZFlag = Bits.set() if bitValue == 0 else Bits.reset()
        cpu.YFlag = Bits.getNthBit(regValue, YF)
        cpu.HFlag = Bits.set()

        cpu.XFlag = Bits.getNthBit(regValue, XF)
        cpu.PVFlag = Bits.set() if bitValue == 0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        #CFlag not affected

    @staticmethod
    def ibit_flags(cpu, bitValue, wReg, bit):
        cpu.HFlag = Bits.set()
        cpu.ZFlag = Bits.set() if bitValue == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if bitValue == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(wReg, XF)
        cpu.YFlag = Bits.getNthBit(wReg, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.set() if bit == SF and bitValue == 1 else Bits.reset()
