# Aux class

from itertools import count
from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF

class Opcodes(object):

    @staticmethod
    def disableInterrupts(cpu, _, logger):
        cpu.iff1, cpu.iff2 = 0x00, 0x00
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DI")

    @staticmethod
    def enableInterrupts(cpu, _, logger):
        cpu.iff1, cpu.iff2 = 0x01, 0x01
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EI")

    @staticmethod
    def xorA(cpu, opcode, logger):
        regInd = opcode & 7
        cpu.A = cpu.A ^ cpu.regs[regInd]

        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A, {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld16(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        loValue = cpu.ram[cpu.PC]
        hiValue = cpu.ram[cpu.PC]
        value = Bits.make16bit(hiValue, loValue)

        cpu.Reg16(regInd, value)

        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("LD {}, {:04X}".format(
            IndexToReg.translate16Bit(regInd),
            value))

    @staticmethod
    def ld8(cpu, opcode, logger):
        regIndPrim = (opcode & 7)
        regInd = (opcode >> 3) & 7
        cpu.regs[regInd] = cpu.regs[regIndPrim]

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD {}, {}".format(
            IndexToReg.translate8Bit(regInd),
            IndexToReg.translate8Bit(regIndPrim)))

    @staticmethod
    def ld_r_ixh(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        cpu.regs[regInd] = cpu.IX >> 8

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD {}, IXH".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_r_ixl(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        cpu.regs[regInd] = cpu.IX & 255

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD {}, IXL".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_ixl_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        high_val = cpu.IX >> 8
        cpu.IX = Bits.make16bit(high_val, cpu.regs[regInd])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IXL, {}".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_ixl_ixh(cpu, _, logger):
        ixh = cpu.IX >> 8
        cpu.IX = Bits.make16bit(ixh, ixh)
        logger.info("LD IXL, IXH")

    @staticmethod
    def ld_iyl_iyh(cpu, _, logger):
        iyh = cpu.IY >> 8
        cpu.IY = Bits.make16bit(iyh, iyh)
        logger.info("LD IYL, IYH")

    @staticmethod
    def ld_ixh_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        low_val = cpu.IX & 255
        cpu.IX = Bits.make16bit(cpu.regs[regInd], low_val)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IXH, {}".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_iyl_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        high_val = cpu.IY >> 8
        cpu.IY = Bits.make16bit(high_val, cpu.regs[regInd])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IYL, {}".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_iyh_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        low_val = cpu.IY & 255
        cpu.IY = Bits.make16bit(cpu.regs[regInd], low_val)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IYH, {}".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_r_iyh(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        cpu.regs[regInd] = cpu.IY >> 8

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD {}, IYH".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld_r_iyl(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        cpu.regs[regInd] = cpu.IY & 255

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD {}, IYL".format(
            IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ld8n(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        value = cpu.ram[cpu.PC]
        cpu.regs[regInd] = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD {}, {:02X}".format(
            IndexToReg.translate8Bit(regInd),
            value))

    @staticmethod
    def jp(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        cpu.PC = cpu.WZ
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("JP {0:04X}".format(cpu.WZ))

    @staticmethod
    def out(cpu, _, logger):
        value = cpu.ram[cpu.PC]
        cpu.io[value] = cpu.A
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("OUT ({:02X}), A".format(value))

    @staticmethod
    def ldExt(cpu, _, logger):
        cpu.I = cpu.A
        cpu.m_cycles, cpu.t_states = 3, 9
        logger.info("LD I, A")

    @staticmethod
    def nop(cpu, _, logger):
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DEFB")

    @staticmethod
    def ld_addr(cpu, _, logger):
        value = cpu.ram[cpu.PC]
        cpu.ram[cpu.HL] = value
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("LD (HL), {:02X}".format(value))

    @staticmethod
    def dec16b(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3

        cpu.Reg16(regInd, cpu.Reg16(regInd) - 1)

        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("DEC {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def dec_ix(cpu, _, logger):
        cpu.IX = cpu.IX - 1
        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("DEC IX")

    @staticmethod
    def dec_iy(cpu, _, logger):
        cpu.IY = cpu.IY - 1
        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("DEC IY")

    @staticmethod
    def cp(cpu, opcode, logger):
        regInd = opcode & 7
        sub = cpu.regs[regInd]
        value = cpu.A - sub
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, sub, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP A, {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def cp_ixh(cpu, _, logger):
        sub = cpu.IX >> 8
        value = cpu.A - sub
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, sub, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP A, IXH")

    @staticmethod
    def cp_ixl(cpu, _, logger):
        sub = cpu.IX & 255
        value = cpu.A - sub
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, sub, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP A, IXL")

    @staticmethod
    def cp_iyh(cpu, _, logger):
        sub = cpu.IY >> 8
        value = cpu.A - sub
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, sub, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP A, IYH")

    @staticmethod
    def cp_iyl(cpu, _, logger):
        sub = cpu.IY & 255
        value = cpu.A - sub
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, sub, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP A, IYL")

    @staticmethod
    def jpnz(cpu, _, logger):
        pc = cpu.PC
        jumpOffset = Bits.from_twos_comp(cpu.ram[pc])

        no_jump = cpu.ZFlag

        if not no_jump:
            cpu.PC = pc + jumpOffset+1
            cpu.m_cycles, cpu.t_states = 1, 5

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR NZ, {0:04X}".format(pc+jumpOffset+1))

    @staticmethod
    def jpnc(cpu, _, logger):
        pc = cpu.PC
        jumpOffset = Bits.twos_comp(cpu.ram[pc])

        no_jump = cpu.CFlag

        if not no_jump:
            cpu.PC = pc + jumpOffset+1
            cpu.m_cycles, cpu.t_states = 1, 5

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR NC, {0:04X}".format(pc+jumpOffset+1))

    @staticmethod
    def _and(cpu, opcode, logger):
        regInd = opcode & 7

        val = cpu.regs[regInd]
        cpu.A = cpu.A & val
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A, {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def and_ixh(cpu, _, logger):
        cpu.A = cpu.A & (cpu.IX >> 8)
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A, IXH")

    @staticmethod
    def and_ixl(cpu, _, logger):
        cpu.A = cpu.A & (cpu.IX & 0xFF)
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A, IXL")

    @staticmethod
    def and_iyl(cpu, _, logger):
        cpu.A = cpu.A & (cpu.IY & 0xFF)
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A, IYL")

    @staticmethod
    def and_iyh(cpu, _, logger):
        cpu.A = cpu.A & (cpu.IY >> 8)
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A, IYH")

    @staticmethod
    def xor_ixh(cpu, _, logger):
        cpu.A = cpu.A ^ (cpu.IX >> 8)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A, IXH")

    @staticmethod
    def xor_ixl(cpu, _, logger):
        cpu.A = cpu.A ^ (cpu.IX & 0xFF)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A, IXL")

    @staticmethod
    def xor_iyh(cpu, _, logger):
        cpu.A = cpu.A ^ (cpu.IY >> 8)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A, IYH")

    @staticmethod
    def xor_iyl(cpu, _, logger):
        cpu.A = cpu.A ^ (cpu.IY & 0xFF)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A, IYL")

    @staticmethod
    def or_ixh(cpu, _, logger):
        cpu.A = cpu.A | (cpu.IX >> 8)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR A, IXH")

    @staticmethod
    def or_ixl(cpu, _, logger):
        cpu.A = cpu.A | (cpu.IX & 0xFF)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR A, IXL")

    @staticmethod
    def or_iyh(cpu, _, logger):
        cpu.A = cpu.A | (cpu.IY >> 8)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR A, IYH")

    @staticmethod
    def or_iyl(cpu, _, logger):
        cpu.A = cpu.A | (cpu.IY & 0xFF)
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR A, IYL")

    @staticmethod
    def _and_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]
        new_val = cpu.A & val
        cpu.A = new_val

        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("AND (HL)")

    @staticmethod
    def sbc(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        value = cpu.Reg16(regInd)

        oldHL = cpu.HL

        val = cpu.HL - value - (1 if cpu.CFlag else 0)

        cpu.HL = val
        cpu.SFlag = Bits.signFlag(cpu.HL, bits=16)
        cpu.ZFlag = Bits.isZero(cpu.HL)
        cpu.HFlag = Bits.set() if Bits.getNthBit((oldHL ^ value ^ cpu.HL) >> 8, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if (((value ^ oldHL) & (oldHL ^ val) & 0x8000) >> 13) != 0 else Bits.reset()
        cpu.NFlag = Bits.set()
        cpu.CFlag = Bits.set() if (val >> 16) != 0 else Bits.reset()
        cpu.YFlag = Bits.getNthBit(cpu.HL >> 8, YF)
        cpu.XFlag = Bits.getNthBit(cpu.HL >> 8, XF)

        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("SBC HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add16(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        value = cpu.Reg16(regInd)

        oldHL = cpu.HL
        newVal = cpu.HL + value
        cpu.HL = newVal
        cpu.WZ = oldHL + 1

        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(newVal, bits=16)
        cpu.HFlag = Bits.set() if Bits.getNthBit((oldHL ^ newVal ^ value) >> 8, HF) else Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.HL >> 8, XF)
        cpu.YFlag = Bits.getNthBit(cpu.HL >> 8, YF)

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("ADD HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def inc16(cpu, opcode, logger):

        regInd = (opcode & 0x30) >> 4
        newVal = cpu.Reg16(regInd) + 1
        cpu.Reg16(regInd, newVal)

        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("INC {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def inc_ix(cpu, _, logger):
        cpu.IX += 1

        logger.info("INC IX")

    @staticmethod
    def ld_nn_ix(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        value = cpu.IX

        cpu.ram[cpu.WZ] = value & 0xFF
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = value >> 8

        logger.info("LD ({:04X}), IX")

    @staticmethod
    def ld_nn_iy(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        value = cpu.IY

        cpu.ram[cpu.WZ] = value & 0xFF
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = value >> 8

        logger.info("LD ({:04X}), IY")

    @staticmethod
    def inc_ixh(cpu, _, logger):
        old_val = cpu.IX
        high = cpu.IX >> 8
        low = cpu.IX & 255

        high += 1

        cpu.IX = Bits.make16bit(high, low)

        Flags.inc_flags(cpu, old_val, cpu.IX)

        logger.info("INC IXH")

    @staticmethod
    def dec_ixh(cpu, _, logger):
        old = cpu.IX
        high = cpu.IX >> 8
        low = cpu.IX & 255
        high -= 1

        cpu.IX = Bits.make16bit(Bits.twos_comp(high), low)

        Flags.dec_flags(cpu, old, cpu.IX)

        logger.info("DEC IXH")

    @staticmethod
    def dec_ixl(cpu, _, logger):
        old = cpu.IX
        high = cpu.IX >> 8
        low = cpu.IX & 255

        low -= 1

        cpu.IX = Bits.make16bit(high, Bits.twos_comp(low))

        Flags.dec_flags(cpu, old, cpu.IX)

        logger.info("DEC IXL")

    @staticmethod
    def inc_ixl(cpu, _, logger):
        old = cpu.IX
        high = cpu.IX >> 8
        low = cpu.IX & 255

        low += 1

        cpu.IX = Bits.make16bit(high, low)
        Flags.inc_flags(cpu, old, cpu.IX)

        logger.info("INC IXL")

    @staticmethod
    def inc_iy(cpu, _, logger):
        cpu.IY += 1

        logger.info("INC IY")

    @staticmethod
    def jr_z(cpu, _, logger):
        pc = cpu.PC
        jumpTo = pc + Bits.twos_comp(cpu.ram[pc]) + 1

        no_jump = cpu.ZFlag is False

        if not no_jump:
            cpu.PC = jumpTo
            cpu.m_cycles, cpu.t_states = 1, 5

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR Z, {:04X}".format(jumpTo))

    @staticmethod
    def exx(cpu, _, logger):

        cpu.BC, cpu.BCPrim = cpu.BCPrim, cpu.BC
        cpu.DE, cpu.DEPrim = cpu.DEPrim, cpu.DE
        cpu.HL, cpu.HLPrim = cpu.HLPrim, cpu.HL

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EXX")

    @staticmethod
    def ldNnRr(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        addr = cpu.WZ

        value = cpu.Reg16(regInd)

        cpu.ram[cpu.WZ] = value & 0xFF
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = value >> 8

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD ({:04X}), {}".format(addr, IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def ldNnHl(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        addr = cpu.WZ


        cpu.ram[cpu.WZ] = cpu.L
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = cpu.H

        cpu.m_cycles, cpu.t_states = 5, 16
        logger.info("LD ({:04X}), HL".format(addr))

    @staticmethod
    def inc8(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        oldValue = cpu.regs[index]
        newValue = Bits.limitTo8Bits(cpu.regs[index] + 1)
        cpu.regs[index] = newValue

        Flags.inc_flags(cpu, oldValue, newValue)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("INC {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def ex_de_hl(cpu, _, logger):
        cpu.DE, cpu.HL = cpu.HL, cpu.DE

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EX DE, HL")

    @staticmethod
    def ex_af_afprim(cpu, _, logger):
        cpu.AF, cpu.AFPrim = cpu.AFPrim, cpu.AF
        cpu.m_cycles, cpu.t_states = 1, 4

        logger.info("EX AF, AF'")

    @staticmethod
    def ldd(cpu, _, logger):
        Opcodes._ldd(cpu)

        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("LDD")

    @staticmethod
    def _ldd(cpu):
        val = cpu.ram[cpu.HL]
        cpu.ram[cpu.DE] = val
        cpu.HL = cpu.HL - 1
        cpu.DE = cpu.DE - 1
        cpu.BC = cpu.BC - 1
        n = Bits.limitTo8Bits(val + cpu.A)

        cpu.PVFlag = Bits.set() if cpu.BC > 0 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.YFlag = Bits.set() if n & 0x02 != 0 else Bits.reset()
        cpu.XFlag = Bits.set() if n & 0x08 != 0 else Bits.reset()

    @staticmethod
    def lddr(cpu, _, logger):
        isZero = cpu.BC == 0
        while True:
            Opcodes._ldd(cpu)
            if cpu.BC == 0:
                break

        cpu.WZ = cpu.pc + 1
        cpu.m_cycles, cpu.t_states = 4 if isZero else 5, 16 if isZero else 21

        logger.info("LDDR")

    @staticmethod
    def ldHl_addr(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        addr = cpu.WZ
        cpu.L = cpu.ram[cpu.WZ]
        cpu.WZ += 1
        cpu.H = cpu.ram[cpu.WZ]
        cpu.m_cycles, cpu.t_states = 5, 16
        logger.info("LD HL, ({:04X})".format(addr))

    @staticmethod
    def ld_sp_hl(cpu, _, logger):
        cpu.SP = cpu.HL
        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("LD SP, HL")

    @staticmethod
    def im1(cpu, _, logger):
        cpu.im = 1

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 1")

    @staticmethod
    def ldiy(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        imm = cpu.WZ

        cpu.IY = imm

        cpu.WZ += 1
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("LD IY, {:04X}".format(imm))

    @staticmethod
    def _ldi(cpu):
        val = cpu.ram[cpu.HL]
        cpu.ram[cpu.DE] = val
        cpu.HL = cpu.HL + 1
        cpu.DE = cpu.DE + 1
        cpu.BC = cpu.BC - 1

        n = Bits.limitTo8Bits(cpu.A + val)
        cpu.PVFlag = Bits.set() if cpu.BC > 0 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()

        cpu.YFlag = Bits.set() if n & 0x02 != 0 else Bits.reset()
        cpu.XFlag = Bits.set() if n & 0x08 != 0 else Bits.reset()
        return val

    @staticmethod
    def ldi(cpu, _, logger):
        Opcodes._ldi(cpu)

        cpu.m_cycles, cpu.t_states = 4, 16
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        logger.info("LDI")

    @staticmethod
    def ldir(cpu, _, logger):
        wasZero = cpu.BC == 0
        while True:
            Opcodes._ldi(cpu)
            if cpu.BC == 0:
                break

        cpu.WZ = cpu.pc + 1
        cpu.m_cycles, cpu.t_states = 4 if wasZero else 5, 16 if wasZero else 21
        logger.info("LDIR")

    @staticmethod
    def ldnn_a(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        addr = cpu.WZ
        cpu.ram[addr] = cpu.A
        cpu.WZ += 1
        cpu.m_cycles, cpu.t_states = 4, 13
        logger.info("LD ({:04X}), A".format(addr))

    @staticmethod
    def dec_mem_at_iy(cpu, _, logger):
        displacement = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IY + displacement
        value = cpu.ram[cpu.WZ]
        new_value = Bits.twos_comp(value - 1)
        cpu.ram[cpu.WZ] = new_value

        Flags.dec_flags(cpu, value, new_value)
        logger.info("DEC (IY+{:2X})".format(displacement))

    @staticmethod
    def inc_mem_at_iy(cpu, _, logger):
        displacement = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IY + displacement
        value = cpu.ram[cpu.WZ]
        new_value = Bits.twos_comp(value + 1)
        cpu.ram[cpu.WZ] = new_value

        Flags.inc_flags(cpu, value, new_value)
        logger.info("INC (IY+{:2X})".format(displacement))

    @staticmethod
    def bit_set_iy(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        val |= (1 << bit)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("SET {},(IY+{:02X})".format(bit, index))

    @staticmethod
    def bit_set_ix(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        val = cpu.ram[cpu.IX+index]
        val |= (1 << bit)
        cpu.ram[cpu.IX+index] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("SET {},(IX+{:02X})".format(bit, index))

    @staticmethod
    def set_r_n(cpu, opcode, logger):
        r = opcode & 7
        b = (opcode >> 3) & 7
        regVal = cpu.regs[r]
        regVal |= (1 << b)
        cpu.regs[r] = Bits.limitTo8Bits(regVal)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("BIT {}, {}".format(b, IndexToReg.translate8Bit(r)))

    @staticmethod
    def bit_res(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, bit, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RES {}, (IY+{:02X})".format(bit, index))

    @staticmethod
    def bit_bit_iy(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7

        cpu.WZ = cpu.IY + index
        Flags.ibit_flags(cpu, Bits.getNthBit(cpu.ram[cpu.WZ], bit), cpu.W, bit)

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("BIT {:X}, (IY+{:02X})".format(bit, index))

    @staticmethod
    def bit_bit_ix(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7

        cpu.WZ = cpu.IX + index
        Flags.ibit_flags(cpu, Bits.getNthBit(cpu.ram[cpu.WZ], bit), cpu.W, bit)

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("BIT {:X}, (IX+{:02X})".format(bit, index))

    @staticmethod
    def bit_r_n(cpu, opcode, logger):
        r = opcode & 7
        b = (opcode >> 3) & 7
        regVal = cpu.regs[r]
        bitNvalue = Bits.getNthBit(regVal, b)

        Flags.bit_flags(cpu, bitNvalue, regVal, b)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("BIT {}, {}".format(b, IndexToReg.translate8Bit(r)))

    @staticmethod
    def sla_n(cpu, opcode, logger):
        index = opcode & 7
        val = cpu.regs[index]
        new_val = Bits.limitTo8Bits(val << 1)
        cpu.regs[index] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLA (IY+{:02X})".format(index))

    @staticmethod
    def sla_at_ix_n(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        cpu.WZ = cpu.IX + index
        val = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(val, 7)
        new_val = Bits.limitTo8Bits(val << 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLA (IX+{:02X})".format(index))

    @staticmethod
    def sla_at_iy_n(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(val, 7)
        new_val = Bits.limitTo8Bits(val << 1)

        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLA (IY+{:02X})".format(index))

    @staticmethod
    def sra_at_ix_n(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        cpu.WZ = cpu.IX + index
        val = cpu.ram[cpu.WZ]
        bit7 = Bits.getNthBit(val, 7)
        bit0 = Bits.getNthBit(val, 0)
        new_val = (bit7 << 7) | (val >> 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if bit0 == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SRA (IX+{:02X})".format(index))

    @staticmethod
    def sra_at_iy_n(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        bit7 = Bits.getNthBit(val, 7)
        bit0 = Bits.getNthBit(val, 0)
        new_val = (bit7 << 7) | (val >> 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if bit0 == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SRA (IY+{:02X})".format(index))

    @staticmethod
    def sla_at_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]
        new_val = Bits.limitTo8Bits(val << 1)
        cpu.ram[cpu.HL] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLA (HL)")

    @staticmethod
    def sra_at_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]
        bit7 = Bits.getNthBit(val, 7)
        new_val = val >> 1
        new_val = Bits.setNthBit(new_val, 7, bit7)
        cpu.ram[cpu.HL] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 0)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SRA (HL)")

    @staticmethod
    def sll_n(cpu, opcode, logger):
        index = opcode & 7
        val = cpu.regs[index]
        new_val = Bits.limitTo8Bits((val << 1) | 1)
        cpu.regs[index] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLL (IY+{:02X})".format(index))

    @staticmethod
    def sll_at_ix_n(cpu, opcode, logger):
        n = (opcode >> 8) & 255
        cpu.WZ = cpu.IX + n
        val = cpu.ram[cpu.WZ]
        new_val = Bits.limitTo8Bits((val << 1) | 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLL (IX+{:02X})".format(n))

    @staticmethod
    def sll_at_iy_n(cpu, opcode, logger):
        n = (opcode >> 8) & 255
        cpu.WZ = cpu.IY + n
        val = cpu.ram[cpu.WZ]
        new_val = Bits.limitTo8Bits((val << 1) | 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLL (IY+{:02X})".format(n))

    @staticmethod
    def srl_at_ix_n(cpu, opcode, logger):
        n = (opcode >> 8) & 255
        cpu.WZ = cpu.IX + n
        val = cpu.ram[cpu.WZ]
        last_bit = Bits.getNthBit(val, 0)
        new_val = Bits.limitTo8Bits(val >> 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if last_bit == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLR (IX+{:02X})".format(n))

    @staticmethod
    def srl_at_iy_n(cpu, opcode, logger):
        n = (opcode >> 8) & 255
        cpu.WZ = cpu.IY + n
        val = cpu.ram[cpu.WZ]
        last_bit = Bits.getNthBit(val, 0)
        new_val = Bits.limitTo8Bits(val >> 1)
        cpu.ram[cpu.WZ] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if last_bit == 1 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLR (IY+{:02X})".format(n))

    @staticmethod
    def sll_at_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]
        new_val = Bits.limitTo8Bits((val << 1) | 1)
        cpu.ram[cpu.HL] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 7)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SLL (HL)")

    @staticmethod
    def srl_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        val = cpu.regs[reg_idx]
        last_bit = Bits.getNthBit(val, 0)
        new_val = Bits.limitTo8Bits(val >> 1)
        cpu.regs[reg_idx] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.set() if last_bit != 0 else Bits.reset()
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("SRL {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def srl_at_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]

        new_val = Bits.limitTo8Bits(val >> 1)
        cpu.ram[cpu.HL] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 0)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SRL (HL)")

    @staticmethod
    def sra_n(cpu, opcode, logger):
        index = opcode & 7
        val = cpu.regs[index]
        bit7 = Bits.getNthBit(val, 7)
        new_val = val >> 1
        new_val = Bits.setNthBit(new_val, 7, bit7)
        cpu.regs[index] = new_val

        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.getNthBit(val, 0)
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.PVFlag = Bits.set() if Bits.count(new_val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.YFlag = Bits.getNthBit(new_val, YF)
        cpu.XFlag = Bits.getNthBit(new_val, XF)
        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("SRA (IY+{:02X})".format(index))

    @staticmethod
    def res_r_n(cpu, opcode, logger):
        r = opcode & 7
        b = (opcode >> 3) & 7
        regVal = cpu.regs[r]
        regVal = Bits.setNthBit(regVal, b, 0)
        cpu.regs[r] = regVal

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("RES {}, {}".format(b, IndexToReg.translate8Bit(r)))

    @staticmethod
    def bit_res_ix(cpu, opcode, logger):
        b = (opcode >> 3) & 7
        n = (opcode >> 8) & 0xff

        cpu.WZ = cpu.IX + n
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, b, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("RES {}, (IX+{:02X})".format(b, n))

    @staticmethod
    def bit_res_iy(cpu, opcode, logger):
        b = (opcode >> 3) & 7
        n = (opcode >> 8) & 0xff

        cpu.WZ = cpu.IY + n
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, b, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("RES {}, (IY+{:02X})".format(b, n))

    @staticmethod
    def bit_r_at_hl(cpu, opcode, logger):
        r = (opcode >> 3) & 7
        val_at_hl = cpu.ram[cpu.HL]
        bitNvalue = Bits.getNthBit(val_at_hl, r)

        Flags.ibit_flags(cpu, bitNvalue, cpu.W, r)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("BIT {}, (HL)".format(r))

    @staticmethod
    def res_r_at_hl(cpu, opcode, logger):
        r = (opcode >> 3) & 7
        val_at_hl = cpu.ram[cpu.HL]
        val_at_hl = Bits.setNthBit(val_at_hl, r, 0)
        cpu.ram[cpu.HL] = val_at_hl

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("RES {}, (HL)".format(r))

    @staticmethod
    def set_r_at_hl(cpu, opcode, logger):
        r = (opcode >> 3) & 7
        val_at_hl = cpu.ram[cpu.HL]
        val_at_hl = Bits.setNthBit(val_at_hl, r, 1)
        cpu.ram[cpu.HL] = val_at_hl

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("SET {}, (HL)".format(r))

    @staticmethod
    def cpir(cpu, _, logger):
        wasZero = cpu.BC == 0
        while True:
            val = cpu.ram[cpu.HL]
            cpu.HL = cpu.HL + 1
            cpu.BC = cpu.BC - 1
            if cpu.BC == 0 or val == cpu.A:
                break

        val = Bits.twos_comp(cpu.A - val)
        cpu.WZ = cpu.WZ + 1
        cpu.SFlag = Bits.set() if Bits.isNegative(val) else Bits.reset()
        cpu.HFlag = Bits.set() if (val & 0xf) > (cpu.A & 0xf) else Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.NFlag = Bits.set()

        if cpu.HFlag:
            val = Bits.from_twos_comp(val)
            val -= 1
            val = Bits.twos_comp(val)


        cpu.XFlag = Bits.set() if (val & 0x08) != 0 else Bits.reset()
        cpu.YFlag = Bits.set() if (val & 0x02) != 0 else Bits.reset()

        cpu.m_cycles, cpu.t_states = 4 if wasZero else 5, 16 if wasZero else 21
        logger.info("CPIR")

    @staticmethod
    def cpdr(cpu, _, logger):
        wasZero = cpu.BC == 0
        reg_a = cpu.A
        while True:
            hl_mem = cpu.ram[cpu.HL]
            cpu.HL = cpu.HL - 1
            cpu.BC = cpu.BC - 1
            if cpu.BC == 0 or hl_mem == cpu.A:
                break

        val = Bits.twos_comp(reg_a - hl_mem)
        cpu.SFlag = Bits.set() if Bits.isNegative(val) else Bits.reset()
        cpu.HFlag = Bits.set() if (val & 0xf) > (reg_a & 0xf) else Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.NFlag = Bits.set()

        if cpu.HFlag:
            val = Bits.from_twos_comp(val)
            val -= 1
            val = Bits.twos_comp(val)

        cpu.XFlag = Bits.set() if (val & 0x08) != 0 else Bits.reset()
        cpu.YFlag = Bits.set() if (val & 0x02) != 0 else Bits.reset()
        cpu.WZ = cpu.WZ + 1
        cpu.m_cycles, cpu.t_states = 4 if wasZero else 5, 16 if wasZero else 21
        logger.info("CPDR")

    @staticmethod
    def cpd(cpu, _, logger):
        reg_a = cpu.A
        mem_HL = cpu.ram[cpu.HL]

        val = Bits.twos_comp(reg_a - mem_HL)

        cpu.HL -= 1
        cpu.BC -= 1
        cpu.WZ -= 1

        cpu.SFlag = Bits.set() if Bits.isNegative(val) else Bits.reset()
        cpu.HFlag = Bits.set() if (val & 0xf) > (reg_a & 0xf) else Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.NFlag = Bits.set()

        if cpu.HFlag:
            val = Bits.from_twos_comp(val)
            val -= 1
            val = Bits.twos_comp(val)

        cpu.XFlag = Bits.set() if (val & 0x08) != 0 else Bits.reset()
        cpu.YFlag = Bits.set() if (val & 0x02) != 0 else Bits.reset()


        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("CPD")

    @staticmethod
    def cpi(cpu, _, logger):
        reg_a = cpu.A
        mem_HL = cpu.ram[cpu.HL]

        val = Bits.twos_comp(reg_a - mem_HL)

        cpu.HL += 1
        cpu.BC -= 1
        cpu.WZ += 1

        cpu.SFlag = Bits.set() if Bits.isNegative(val) else Bits.reset()
        cpu.HFlag = Bits.set() if (val & 0xf) > (reg_a & 0xf) else Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.NFlag = Bits.set()

        if cpu.HFlag:
            val = Bits.from_twos_comp(val)
            val -= 1
            val = Bits.twos_comp(val)

        cpu.XFlag = Bits.set() if (val & 0x08) != 0 else Bits.reset()
        cpu.YFlag = Bits.set() if (val & 0x02) != 0 else Bits.reset()

        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("CPI")

    @staticmethod
    def call(cpu, _, logger):
        pc = cpu.PC
        cpu.Z = cpu.ram[pc]
        pc += 1
        cpu.W = cpu.ram[pc]
        pc += 1
        cpu.ram[cpu.SP - 1] = pc >> 8
        cpu.ram[cpu.SP - 2] = (pc & 255)
        cpu.SP = cpu.SP - 2
        cpu.PC = cpu.WZ

        cpu.m_cycles, cpu.t_states = 5, 17
        logger.info("CALL {:04X}".format(cpu.WZ))

    @staticmethod
    def ldiy_d_r(cpu, opcode, logger):
        regInd = opcode & 7
        d = cpu.ram[cpu.PC]
        cpu.ram[cpu.IY + d] = cpu.regs[regInd]
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IY+{:02X}), {}".format(d, IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def ldhlr(cpu, opcode, logger):
        regInd = opcode & 7
        cpu.ram[cpu.HL] = cpu.regs[regInd]
        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD (HL), {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def djnz(cpu, _, logger):
        pc = cpu.PC
        e = cpu.ram[pc]
        cpu.B = cpu.B - 1
        pc = pc + Bits.from_twos_comp(e) + 1
        if cpu.B != 0:
            cpu.m_cycles, cpu.t_states = 1, 5
            cpu.PC = pc

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DJNZ {:04X}".format(pc))

    @staticmethod
    def add_a_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IY + d
        old = cpu.A
        val = cpu.ram[cpu.WZ]

        new = cpu.A + val
        cpu.A = new

        Flags.add_flags(cpu, old, cpu.A, new, val)
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD A, (IY+{:02X})".format(d))

    @staticmethod
    def sub_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        new = cpu.A - n
        cpu.A = Bits.twos_comp(new)


        Flags.sub_flags(cpu, old, cpu.A, new, n)


        logger.info("SUB A, {:02X}".format(n))

    @staticmethod
    def push(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        value = cpu.Reg16(regInd, af=True)

        cpu.ram[cpu.SP-1] = value >> 8
        cpu.ram[cpu.SP-2] = value & 255
        cpu.SP -= 2
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("PUSH {}".format(IndexToReg.translate16Bit(regInd, af=True)))


    @staticmethod
    def push_ix(cpu, _, logger):
        value = cpu.IX

        cpu.ram[cpu.SP-1] = value >> 8
        cpu.ram[cpu.SP-2] = value & 255
        cpu.SP -= 2
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("PUSH IX")

    @staticmethod
    def push_iy(cpu, _, logger):
        value = cpu.IY

        cpu.ram[cpu.SP-1] = value >> 8
        cpu.ram[cpu.SP-2] = value & 255
        cpu.SP -= 2
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("PUSH IY")

    @staticmethod
    def sub_r(cpu, opcode, logger):
        index = opcode & 7

        old_A = cpu.A
        sub = cpu.regs[index]
        new_val = cpu.A - sub
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, sub)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SUB {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def rrca(cpu, _, logger):
        cflag = Bits.getNthBit(cpu.A, 0)
        cpu.A = Bits.setNthBit(cpu.A >> 1, 7, cflag)
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 1, 4

        logger.info("RRCA")

    @staticmethod
    def rlca(cpu, _, logger):
        cflag = Bits.getNthBit(cpu.A, 7)
        cpu.A = Bits.setNthBit(cpu.A << 1, 0, cflag)

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RLCA")

    @staticmethod
    def rl_n(cpu, opcode, logger):
        index = opcode & 7
        value = cpu.regs[index]
        cflag = Bits.getNthBit(value, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(value << 1, 0, 1 if cpu.CFlag else 0))
        cpu.regs[index] = val

        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.set() if Bits.getNthBit(val, SF) != 0 else Bits.reset()
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.ZFlag = Bits.isZero(val)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RL {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def rl_at_hl(cpu, _, logger):
        value = cpu.ram[cpu.HL]
        cflag = Bits.getNthBit(value, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(value << 1, 0, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.HL] = val

        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.set() if Bits.getNthBit(val, SF) != 0 else Bits.reset()
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.ZFlag = Bits.isZero(val)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 2, 12
        logger.info("RL (HL)")

    @staticmethod
    def rr_at_hl(cpu, _, logger):
        value = cpu.ram[cpu.HL]
        cflag = Bits.getNthBit(value, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(value >> 1, 7, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.HL] = val

        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.set() if Bits.getNthBit(val, SF) != 0 else Bits.reset()
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.ZFlag = Bits.isZero(val)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 2, 12
        logger.info("RR (HL)")

    @staticmethod
    def rr_n(cpu, opcode, logger):
        index = opcode & 7
        value = cpu.regs[index]
        cflag = Bits.getNthBit(value, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(value >> 1, 7, 1 if cpu.CFlag else 0))
        cpu.regs[index] = val

        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.SFlag = Bits.set() if Bits.getNthBit(val, SF) != 0 else Bits.reset()
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.ZFlag = Bits.isZero(val)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RR {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def rlc_n(cpu, opcode, logger):
        n = opcode & 7
        r = cpu.regs[n]
        cflag = Bits.getNthBit(r, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(r << 1, 0, cflag))
        cpu.regs[n] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("RLC {}".format(IndexToReg.translate8Bit(r)))

    @staticmethod
    def rlc_at_hl(cpu, _, logger):
        hl = cpu.HL
        value = cpu.ram[hl]
        cflag = Bits.getNthBit(value, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(value << 1, 0, cflag))
        cpu.ram[hl] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 18
        logger.info("RLC (HL)")

    @staticmethod
    def rrc_n(cpu, opcode, logger):
        n = opcode & 7
        r = cpu.regs[n]
        cflag = Bits.getNthBit(r, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(r >> 1, 7, cflag))
        cpu.regs[n] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("RRC {}".format(IndexToReg.translate8Bit(r)))

    @staticmethod
    def rrc_at_hl(cpu, _, logger):
        hl = cpu.HL
        value = cpu.ram[hl]
        cflag = Bits.getNthBit(value, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(value >> 1, 7, cflag))
        cpu.ram[hl] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 18
        logger.info("RRC (HL)")

    @staticmethod
    def rlc_at_ix_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IX + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(r << 1, 0, cflag))
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RLC (IX+{:02X})".format(n))

    @staticmethod
    def rl_at_ix_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IX + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(r << 1, 0, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RL (IX+{:02X})".format(n))

    @staticmethod
    def rr_at_ix_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IX + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(r >> 1, 7, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RR (IX+{:02X})".format(n))

    @staticmethod
    def rr_at_iy_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IY + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 0)
        val = Bits.limitTo8Bits(Bits.setNthBit(r >> 1, 7, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.WZ] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RR (IY+{:02X})".format(n))

    @staticmethod
    def rl_at_iy_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IY + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(r << 1, 0, 1 if cpu.CFlag else 0))
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RL (IY+{:02X})".format(n))

    @staticmethod
    def rrc_at_ix_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IX + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 0)
        val =  Bits.setNthBit(r >> 1, 7, cflag)
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RRC (IX+{:02X})".format(n))

    @staticmethod
    def rlc_at_iy_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IY + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 7)
        val = Bits.limitTo8Bits(Bits.setNthBit(r << 1, 0, cflag))
        cpu.ram[cpu.WZ] = val

        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RLC (IY+{:02X})".format(n))

    @staticmethod
    def rrc_at_iy_n(cpu, opcode, logger):
        n = Bits.from_twos_comp((opcode >> 8) & 255)
        cpu.WZ = cpu.IY + n
        r = cpu.ram[cpu.WZ]
        cflag = Bits.getNthBit(r, 0)
        val = Bits.setNthBit(r >> 1, 7, cflag)
        cpu.ram[cpu.WZ] = val
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if val == 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(val) & 1 == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(val, XF)
        cpu.YFlag = Bits.getNthBit(val, YF)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(val)

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RRC (IY+{:02X})".format(n))

    @staticmethod
    def and_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = cpu.A & n

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("AND {:02X}".format(n))

    @staticmethod
    def or_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = cpu.A | n

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(cpu.A) & 1 == 0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("OR {:02X}".format(n))

    @staticmethod
    def ret(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.SP]
        cpu.W = cpu.ram[cpu.SP+1]

        cpu.SP += 2
        cpu.PC = cpu.WZ
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("RET")


    @staticmethod
    def retn(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        high = cpu.ram[cpu.SP+1]
        addr = Bits.make16bit(high, low)
        cpu.SP += 2
        cpu.PC = addr

        cpu.m_cycles = 14
        cpu.iff1 = cpu.iff2
        logger.info("RETN")

    @staticmethod
    def rst(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        pc = cpu.PC
        cpu.ram[cpu.SP - 1] = pc >> 8
        cpu.ram[cpu.SP - 2] = pc & 8
        cpu.SP -= 2

        cpu.WZ = cpu.rst_jumps[index]
        cpu.PC = cpu.WZ
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("RST {:02X}".format(cpu.rst_jumps[index]))

    @staticmethod
    def pop(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        high = cpu.ram[cpu.SP+1]
        low = cpu.ram[cpu.SP]
        cpu.SP += 2
        val = Bits.make16bit(high, low)

        cpu.Reg16(regInd, val, af=True)

        cpu.m_cycles, cpu.t_states = 3, 7
        logger.info("POP {}".format(IndexToReg.translate16Bit(regInd, af=True)))

    @staticmethod
    def ldiy_d_n(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        n = cpu.ram[cpu.PC]

        cpu.WZ = cpu.IY + d
        cpu.ram[cpu.WZ] = n
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IY+{:02X}),{:02X}".format(d, n))

    @staticmethod
    def add_r(cpu, opcode, logger):
        index = (opcode & 7)
        old = cpu.A
        value = cpu.regs[index]
        new = old + value
        cpu.A = new

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ value ^ cpu.A), HF) !=0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((old ^ value ^ 0x80) & (value ^ cpu.A)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("ADD A, {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def add_r_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A

        value = cpu.A + n
        cpu.A = value

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit(old ^ n ^ value, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit(((old ^ n ^ 0x80) & (n ^ value)) >> 5, PVF) != 0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(value)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("ADD A, {:02X}".format(n))

    @staticmethod
    def ld_r_hl(cpu, opcode, logger):
        index = (opcode >> 3) & 7

        value = cpu.ram[cpu.HL]

        cpu.regs[index] = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD {}, (HL)".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def _or(cpu, opcode, logger):
        regInd = opcode & 7
        cpu.A = cpu.A | cpu.regs[regInd]
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def jr_e(cpu, _, logger):
        pc = cpu.PC
        jumpOffset = Bits.twos_comp(cpu.ram[pc])

        cpu.PC = pc + jumpOffset + 1
        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("JR {:02X}".format(jumpOffset))

    @staticmethod
    def ld16_nn(cpu, opcode, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        addr = cpu.WZ
        value_low = cpu.ram[cpu.WZ]
        cpu.WZ += 1
        value_high = cpu.ram[cpu.WZ]
        value = Bits.make16bit(value_high, value_low)
        regInd = (opcode >> 4) & 3

        cpu.Reg16(regInd, value)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD {},({:0X})".format(IndexToReg.translate16Bit(regInd), addr))

    @staticmethod
    def ld_a_bc(cpu, _, logger):
        value = cpu.ram[cpu.BC]
        cpu.A = value
        cpu.WZ = cpu.BC + 1

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD A, (BC)")

    @staticmethod
    def ld_a_de(cpu, _, logger):
        value = cpu.ram[cpu.DE]
        cpu.A = value
        cpu.WZ = cpu.DE + 1

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD A, (DE)")

    @staticmethod
    def ld_a_nn(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        addr = cpu.WZ
        cpu.WZ += 1
        cpu.A = cpu.ram[addr]
        cpu.m_cycles, cpu.t_states = 4, 13
        logger.info("LD A, ({:04X})".format(addr))

    @staticmethod
    def ld_bc_a(cpu, _, logger):
        cpu.ram[cpu.BC] = cpu.A
        cpu.WZ = Bits.make16bit(cpu.A, Bits.limitTo8Bits(cpu.BC + 1))

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD (BC), A")

    @staticmethod
    def ld_de_a(cpu, _, logger):
        cpu.ram[cpu.DE] = cpu.A
        cpu.WZ = Bits.make16bit(cpu.A, Bits.limitTo8Bits(cpu.DE + 1))

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD (DE), A")

    @staticmethod
    def lra(cpu, _, logger):
        cflag = Bits.getNthBit(cpu.A, 7)
        cpu.A = Bits.setNthBit((cpu.A << 1), 0, cpu.CFlag)
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LRA")

    @staticmethod
    def rra(cpu, _, logger):
        cflag = Bits.getNthBit(cpu.A, 0)
        cpu.A = Bits.setNthBit((cpu.A >> 1), 7, cpu.CFlag)
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RRA")

    @staticmethod
    def rld(cpu, _, logger):
        addr = cpu.HL
        v = cpu.ram[addr]
        ah = cpu.A & 0xF0
        al = cpu.A & 0x0F

        low_hl = v & 0x0F
        high_hl = (v & 0xF0) >> 4
        cpu.A = ah | high_hl
        mem_hl = (low_hl << 4) | al
        cpu.ram[addr] = mem_hl
        cpu.WZ = addr + 1

        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 5, 18
        logger.info("RLD")

    @staticmethod
    def rrd(cpu, _, logger):
        addr = cpu.HL
        v = cpu.ram[addr]
        ah = cpu.A & 0xF0
        al = cpu.A & 0x0F

        low_hl = v & 0x0F
        high_hl = (v & 0xF0) >> 4
        cpu.A = ah | low_hl
        mem_hl = (al << 4) | high_hl
        cpu.ram[addr] = mem_hl
        cpu.WZ = addr + 1

        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 5, 18
        logger.info("RRD")

    @staticmethod
    def neg(cpu, _, logger):
        old = cpu.A
        cpuAfrom2s = Bits.from_twos_comp(cpu.A)
        new = 0 - cpuAfrom2s
        cpu.A = Bits.twos_comp(new)

        Flags.sub_flags(cpu, 0, cpu.A, new, old)
        cpu.CFlag = Bits.set() if old != 0 else Bits.reset()
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("NEG")

    @staticmethod
    def ld_r_iy_d(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IY + d
        cpu.regs[index] = cpu.ram[cpu.WZ]

        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD {}, (IY+{:02X})".format(IndexToReg.translate8Bit(index), d))

    @staticmethod
    def ld_ix_nn(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        val = cpu.WZ

        cpu.IX = val
        cpu.WZ += 1

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD IX, {:04X}".format(val))

    @staticmethod
    def ld_ix_at_nn(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        addr = cpu.WZ
        low_val = cpu.ram[cpu.WZ]
        cpu.WZ += 1
        high_val = cpu.ram[cpu.WZ]
        cpu.IX = Bits.make16bit(high_val, low_val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD IX, ({:04X})".format(addr))

    @staticmethod
    def ld_iy_at_nn(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        addr = cpu.WZ
        low_val = cpu.ram[cpu.WZ]
        cpu.WZ += 1
        high_val = cpu.ram[cpu.WZ]
        cpu.IY = Bits.make16bit(high_val, low_val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD IY, ({:04X})".format(addr))

    @staticmethod
    def ld_r_ix_d(cpu, opcode, logger):
        r = (opcode >> 3) & 7
        d = cpu.ram[cpu.PC]

        cpu.WZ = cpu.IX + d
        cpu.regs[r] = cpu.ram[cpu.WZ]
        logger.info("LD {}, (IX+{})".format(IndexToReg.translate8Bit(r), d))

    @staticmethod
    def ld_at_ix_d_nn(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        n = cpu.ram[cpu.PC]

        cpu.WZ = cpu.IX + d
        cpu.ram[cpu.WZ] = n
        logger.info("LD (IX+{}), {}".format(d,n))

    @staticmethod
    def ld_at_ix_d_r(cpu, opcode, logger):
        d = cpu.ram[cpu.PC]
        r = opcode & 7
        cpu.WZ = cpu.IX + d
        cpu.ram[cpu.WZ] = cpu.regs[r]
        logger.info("LD (IX+{}), {}".format(d, IndexToReg.translate8Bit(r)))

    @staticmethod
    def ld_at_iy_d_r(cpu, opcode, logger):
        d = cpu.ram[cpu.PC]
        r = opcode & 7
        cpu.WZ = cpu.IY + d
        cpu.ram[cpu.WZ] = cpu.regs[r]

        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IY+{}), {}".format(d, IndexToReg.translate8Bit(r)))

    @staticmethod
    def ld_ixh_nn(cpu, _, logger):
        val = cpu.ram[cpu.PC]
        low_val = cpu.IX & 255
        cpu.IX = Bits.make16bit(val, low_val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD HX, {:04X}".format(cpu.IX))

    @staticmethod
    def ld_ixl_nn(cpu, _, logger):
        val = cpu.ram[cpu.PC]
        high_val = cpu.IX >> 8
        cpu.IX = Bits.make16bit(high_val, val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD LX, {:04X}".format(cpu.IX))

    @staticmethod
    def ld_iyl_nn(cpu, _, logger):
        val = cpu.ram[cpu.PC]
        high_val = cpu.IY >> 8
        cpu.IY = Bits.make16bit(high_val, val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD LY, {:04X}".format(cpu.IY))

    @staticmethod
    def ld_ihy_nn(cpu, _, logger):
        val = cpu.ram[cpu.PC]
        low_val = cpu.IY & 255
        cpu.IY = Bits.make16bit(val, low_val)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD HY, {:04X}".format(cpu.IY))

    @staticmethod
    def ldra(cpu, _, logger):
        cpu.R = cpu.A
        cpu.m_cycles, cpu.t_states = 2, 9
        logger.info("LD R, A")

    @staticmethod
    def ldar(cpu, _, logger):
        cpu.A = cpu.R

        cpu.SFlag = Bits.isNegative(cpu.R)
        cpu.ZFlag = Bits.isZero(cpu.R)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.iff2 == 1 else Bits.reset()
        cpu.NFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 9
        logger.info("LD A, R")

    @staticmethod
    def im2(cpu, _, logger):
        cpu.im = 2

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 2")

    @staticmethod
    def im0(cpu, _, logger):
        cpu.im = 0

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 0")

    @staticmethod
    def pop_ix(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        high = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        cpu.IX = Bits.make16bit(high, low)
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("POP IX")

    @staticmethod
    def pop_iy(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        high = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        cpu.IY = Bits.make16bit(high, low)
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("POP IY")

    @staticmethod
    def jp_cond(cpu, opcode, logger):
        cond = (opcode >> 3) & 7
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        taken = False

        if cond == 0 and cpu.ZFlag is False:
            taken = True
        if cond == 1 and cpu.ZFlag:
            taken = True
        if cond == 2 and cpu.CFlag is False:
            taken = True
        if cond == 3 and cpu.CFlag:
            taken = True
        if cond == 4 and cpu.PVFlag is False:
            taken = True
        if cond == 5 and cpu.PVFlag:
            taken = True
        if cond == 6 and cpu.SFlag is False:
            taken = True
        if cond == 7 and cpu.SFlag:
            taken = True

        if taken:
            cpu.PC = cpu.WZ

        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("JP {} {:04X}".format(IndexToFlag.translate(cond), cpu.WZ))

    @staticmethod
    def call_cond(cpu, opcode, logger):
        cond = (opcode >> 3) & 7
        pc = cpu.PC
        cpu.Z = cpu.ram[pc]
        pc += 1
        cpu.W = cpu.ram[pc]
        addr = cpu.WZ
        pc += 1

        taken = False

        if cond == 0 and cpu.ZFlag is False:
            taken = True
        elif cond == 1 and cpu.ZFlag:
            taken = True
        elif cond == 2 and cpu.CFlag is False:
            taken = True
        elif cond == 3 and cpu.CFlag:
            taken = True
        elif cond == 4 and cpu.PVFlag is False:
            taken = True
        elif cond == 5 and cpu.PVFlag:
            taken = True
        elif cond == 6 and cpu.SFlag is False:
            taken = True
        elif cond == 7 and cpu.SFlag:
            taken = True

        if taken:
            cpu.ram[cpu.SP - 1] = pc >> 8
            cpu.ram[cpu.SP - 2] = (pc & 255)
            cpu.SP = cpu.SP - 2
            cpu.PC = addr
            cpu.m_cycles, cpu.t_states = 2, 7
        else:
            cpu.PC += 1

        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("CALL {}, {:04X}".format(
            IndexToFlag.translate(cond),
            addr))

    @staticmethod
    def dec8b(cpu, opcode, logger):
        reg_index = (opcode >> 3) & 7
        old_val = cpu.regs[reg_index]
        cpu.regs[reg_index] = Bits.twos_comp(cpu.regs[reg_index] - 1)

        Flags.dec_flags(cpu, old_val, cpu.regs[reg_index])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DEC {}".format(IndexToReg.translate8Bit(reg_index)))

    @staticmethod
    def dec_at_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IX + d
        old_val = Bits.from_twos_comp(cpu.ram[cpu.WZ])
        new_val = Bits.twos_comp(old_val - 1)
        cpu.ram[cpu.WZ] = new_val

        Flags.dec_flags(cpu, old_val, new_val)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("DEC (IX+{:02X})".format(d))

    @staticmethod
    def inc_at_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IX + d
        old_val = Bits.from_twos_comp(cpu.ram[cpu.WZ])
        new_val = Bits.twos_comp(old_val + 1)
        cpu.ram[cpu.WZ] = new_val

        Flags.inc_flags(cpu, old_val, new_val)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("INC (IX+{:02X})".format(d))

    @staticmethod
    def cpl(cpu, _, logger):
        old = cpu.A
        new = ~old & 0xff
        cpu.A = new
        cpu.HFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CPL")

    @staticmethod
    def ccf(cpu, _, logger):
        prevCarry = cpu.CFlag
        cpu.CFlag = Bits.flip(cpu.CFlag)
        cpu.NFlag = Bits.reset()
        cpu.HFlag = prevCarry
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CCF")

    @staticmethod
    def scf(cpu, _, logger):
        cpu.CFlag = Bits.set()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SCF")

    @staticmethod
    def hlt(cpu, _, logger):
        logger.info("HALT")
        cpu.m_cycles, cpu.t_states = 1, 4
        cpu.halted = Bits.set()

    @staticmethod
    def add_Hl_rr_c(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd)

        old = cpu.HL
        newVal = cpu.HL + val + (1 if cpu.CFlag else 0)
        cpu.HL = newVal

        cpu.SFlag = Bits.signFlag(cpu.HL, bits=16)
        cpu.ZFlag = Bits.isZero(cpu.HL)
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ val ^ cpu.HL) >> 8, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if (((val ^ old ^ 0x8000) & (val ^ newVal) & 0x8000) >> 13) != 0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.set() if Bits.getNthBit((newVal >> 16), CF) != 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.HL >> 8, XF)
        cpu.YFlag = Bits.getNthBit(cpu.HL >> 8, YF)
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADC HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add_a_ixh(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IX >> 8
        new = oldA + value
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADD A, HX")

    @staticmethod
    def adc_a_ixh(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IX >> 8
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, HX")

    @staticmethod
    def adc_a_ixl(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IX & 255
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, LX")

    @staticmethod
    def adc_a_ix_d(cpu, _, logger):
        oldA = cpu.A
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, (IX+{:02X})".format(d))

    @staticmethod
    def adc_a_iy_d(cpu, _, logger):
        oldA = cpu.A
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, (IY+{:02X})".format(d))

    @staticmethod
    def adc_a_iyl(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IY & 255
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, LY")

    @staticmethod
    def sub_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value
        cpu.A = new

        Flags.sub_flags(cpu, oldA, cpu.A, new, value)

        logger.info("SUB A, (IX+{:02X})".format(d))

    @staticmethod
    def sub_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value
        cpu.A = new

        Flags.sub_flags(cpu, oldA, cpu.A, new, value)

        logger.info("SUB A, (IY+{:02X})".format(d))

    @staticmethod
    def sbc_a_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value - (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.sub_flags(cpu, oldA, cpu.A, new, value)

        logger.info("SBC A, (IX+{:02X})".format(d))

    @staticmethod
    def sbc_a_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value - (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.sub_flags(cpu, oldA, cpu.A, new, value)

        logger.info("SBC A, (IY+{:02X})".format(d))

    @staticmethod
    def and_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA & value
        cpu.A = new

        Flags.and_flags(cpu, cpu.A)

        logger.info("AND A, (IX+{:02X})".format(d))

    @staticmethod
    def or_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA | value
        cpu.A = new

        Flags.or_flags(cpu, cpu.A)

        logger.info("OR A, (IX+{:02X})".format(d))

    @staticmethod
    def xor_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA ^ value
        cpu.A = new

        Flags.xor_flags(cpu, cpu.A)

        logger.info("XOR A, (IX+{:02X})".format(d))

    @staticmethod
    def cp_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IX + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value
        newIn2s = Bits.twos_comp(new)


        Flags.cp_flags(cpu, value, oldA, new, newIn2s)

        logger.info("CP A, (IX+{:02X})".format(d))

    @staticmethod
    def and_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A

        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA & value
        cpu.A = new

        Flags.and_flags(cpu, cpu.A)

        logger.info("AND A, (IY+{:02X})".format(d))

    @staticmethod
    def or_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA | value
        cpu.A = new

        Flags.or_flags(cpu, cpu.A)

        logger.info("OR A, (IY+{:02X})".format(d))

    @staticmethod
    def xor_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A
        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA ^ value
        cpu.A = new

        Flags.xor_flags(cpu, cpu.A)

        logger.info("XOR A, (IY+{:02X})".format(d))

    @staticmethod
    def cp_iy_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        oldA = cpu.A

        cpu.WZ = cpu.IY + d
        value = cpu.ram[cpu.WZ]
        new = oldA - value
        newIn2s = Bits.twos_comp(new)

        Flags.cp_flags(cpu, value, oldA, new, newIn2s)

        logger.info("CP A, (IY+{:02X})".format(d))

    @staticmethod
    def add_a_ixl(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IX & 255
        new = oldA + value
        cpu.A = new
        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADD A, LX")

    @staticmethod
    def add_a_iyh(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IY >> 8
        new = oldA + value
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADD A, HY")

    @staticmethod
    def adc_a_iyh(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IY >> 8
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADC A, HY")

    @staticmethod
    def add_a_iyl(cpu, _, logger):
        oldA = cpu.A
        value = cpu.IY & 255
        new = oldA + value
        cpu.A = new

        Flags.add_flags(cpu, oldA, cpu.A, new, value)

        logger.info("ADD A, LY")

    @staticmethod
    def add_a_ix_d(cpu, _, logger):
        d = cpu.ram[cpu.PC]
        cpu.WZ = cpu.IX + d
        old = cpu.A
        val = cpu.ram[cpu.WZ]
        new = cpu.A + val
        cpu.A = new
        Flags.add_flags(cpu, old, cpu.A, new, val)
        logger.info("ADD A, (IX+{})".format(d))

    @staticmethod
    def add_ix_rr(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd, ix=True)

        old = cpu.IX
        newVal = cpu.IX + val
        cpu.IX = newVal
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ newVal ^ val) >> 8, HF) else Bits.reset()
        cpu.CFlag = Bits.carryFlag(newVal, bits=16)
        cpu.XFlag = Bits.getNthBit(cpu.IX >> 8, XF)
        cpu.YFlag = Bits.getNthBit(cpu.IX >> 8, YF)

        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD IX, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add_iy_rr(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd, iy=True)

        old = cpu.IY
        newVal = cpu.IY + val
        cpu.IY = newVal
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.set() if Bits.getNthBit((old ^ newVal ^ val) >> 8, HF) else Bits.reset()
        cpu.CFlag = Bits.carryFlag(newVal, bits=16)
        cpu.XFlag = Bits.getNthBit(cpu.IY >> 8, XF)
        cpu.YFlag = Bits.getNthBit(cpu.IY >> 8, YF)
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD IY, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def jp_hl(cpu, _, logger):
        cpu.PC = cpu.HL
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("JP HL")

    @staticmethod
    def jp_ix(cpu, _, logger):
        cpu.PC = cpu.IX
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("JP IX")

    @staticmethod
    def jp_iy(cpu, _, logger):
        cpu.PC = cpu.IY
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("JP IY")

    @staticmethod
    def dec_at_hl(cpu, _, logger):
        old_val = Bits.from_twos_comp(cpu.ram[cpu.HL])
        new_val = old_val - 1
        new_val = Bits.limitTo8Bits(new_val)
        cpu.ram[cpu.HL] = new_val

        Flags.dec_flags(cpu, old_val, new_val)

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("DEC (HL)")

    @staticmethod
    def inc_at_hl(cpu, _, logger):
        old_val = Bits.from_twos_comp(cpu.ram[cpu.HL])
        new_val = old_val + 1
        limited_value = Bits.limitTo8Bits(new_val)
        cpu.ram[cpu.HL] = limited_value

        Flags.inc_flags(cpu, old_val, limited_value)

        cpu.m_cycles, cpu.t_states = 3, 11

        logger.info("INC (HL)")

    @staticmethod
    def jr_c(cpu, _, logger):
        pc = cpu.PC + 1
        jumpOffset = Bits.twos_comp(cpu.ram[pc]) - 2
        no_jump = cpu.CFlag is False
        cpu.WZ = pc + jumpOffset
        if not no_jump:
            cpu.PC = cpu.WZ
            cpu.m_cycles, cpu.t_states = 1, 5
        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JP C {0:04X}".format(cpu.WZ))

    @staticmethod
    def portIn(cpu, _, logger):
        cpu.A = cpu.io[cpu.C]

        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("IN A, (C)")

    @staticmethod
    def ret_cc(cpu, opcode, logger):
        cond = (opcode >> 3) & 7

        cond_name = ''
        jump = None
        if cond == 0:
            cond_name = 'NZ'
            jump = cpu.ZFlag == Bits.reset()
        if cond == 1:
            cond_name = 'Z'
            jump = cpu.ZFlag == Bits.set()
        if cond == 2:
            cond_name = 'NC'
            jump = cpu.CFlag == Bits.reset()
        if cond == 3:
            cond_name = 'C'
            jump = cpu.CFlag == Bits.set()
        if cond == 4:
            cond_name = 'PO'
            jump = cpu.PVFlag == Bits.reset()
        if cond == 5:
            cond_name = 'PE'
            jump = cpu.PVFlag == Bits.set()
        if cond == 6:
            cond_name = 'P'
            jump = cpu.SFlag == Bits.reset()
        if cond == 7:
            cond_name = 'M'
            jump = cpu.SFlag == Bits.set()

        if jump:
            cpu.Z = cpu.ram[cpu.SP]
            cpu.W = cpu.ram[cpu.SP+1]
            addr = cpu.WZ
            cpu.SP += 2
            cpu.PC = addr
            cpu.m_cycles, cpu.t_states = 2, 6

        cpu.m_cycles, cpu.t_states = 1, 5
        logger.info("RET {}".format(cond_name))

    @staticmethod
    def adc_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        old_val = cpu.A
        value = cpu.regs[reg_idx]
        new_val = old_val + value + (1 if cpu.CFlag else 0)
        cpu.A = new_val

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit((old_val ^ value ^ cpu.A), HF) !=0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((old_val ^ value ^ 0x80) & (value ^ cpu.A)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new_val)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("ADC A, {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def add_a_hl(cpu, _, logger):
        oldA = cpu.A
        value = cpu.ram[cpu.HL]
        new = cpu.A + value
        cpu.A = new

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit((oldA ^ value ^ cpu.A), HF) !=0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((oldA ^ value ^ 0x80) & (value ^ cpu.A)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("ADD A, (HL)")

    @staticmethod
    def cp_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        new = old - n
        newIn2s = Bits.twos_comp(old - n)

        Flags.cp_flags(cpu, n, old, new, newIn2s)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("CP A, {:02X}".format(n))

    @staticmethod
    def xor_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = old ^ n

        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("XOR A, {:02X}".format(n))

    @staticmethod
    def in_a_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        cpu.A = cpu.io[n]

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("IN A, ({:02X}".format(n))

    @staticmethod
    def adc_a_hl(cpu, _, logger):
        value = cpu.ram[cpu.HL]
        oldA = cpu.A
        new = oldA + value + (1 if cpu.CFlag else 0)
        cpu.A = new

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit((oldA ^ value ^ cpu.A), HF) !=0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit((((oldA ^ value ^ 0x80) & (value ^ cpu.A)) >> 5), PVF) !=0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("ADC A, (HL)")

    @staticmethod
    def sub_a_hl(cpu, _, logger):
        v = cpu.ram[cpu.HL]
        old_A = cpu.A
        new_val = old_A - v
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, v)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, (HL)")

    @staticmethod
    def sub_ixh(cpu, _, logger):
        old_A = cpu.A
        new_val = old_A - (cpu.IX >> 8)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, cpu.IX >> 8)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, IXH")

    @staticmethod
    def sub_ixl(cpu, _, logger):
        old_A = cpu.A
        new_val = old_A - (cpu.IX & 0xFF)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, cpu.IX & 0xFF)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, IXL")

    @staticmethod
    def sub_iyh(cpu, _, logger):
        old_A = cpu.A
        new_val = old_A - (cpu.IY >> 8)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, cpu.IY >> 8)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, IYH")

    @staticmethod
    def sbc_a_ixh(cpu, _, logger):
        v = cpu.IX >> 8
        old_A = cpu.A
        new_val = old_A - v - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, v)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SBC A, IXH")

    @staticmethod
    def sbc_a_ixl(cpu, _, logger):
        v = cpu.IX & 0xFF
        old_A = cpu.A
        new_val = old_A - v - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, v)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SBC A, IXL")

    @staticmethod
    def sbc_a_iyh(cpu, _, logger):
        v = cpu.IY >> 8
        old_A = cpu.A
        new_val = old_A - v - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, v)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SBC A, IYH")

    @staticmethod
    def sbc_a_iyl(cpu, _, logger):
        v = cpu.IY & 0xFF
        old_A = cpu.A
        new_val = old_A - v - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, v)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SBC A, IYL")

    @staticmethod
    def sub_iyl(cpu, _, logger):
        old_A = cpu.A
        new_val = old_A - (cpu.IY & 0xFF)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_A, cpu.A, new_val, cpu.IY & 0xFF)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, IYL")

    @staticmethod
    def sbc_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        old_val = cpu.A
        value = cpu.regs[reg_idx]
        new_val = old_val - value - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_val, cpu.A, new_val, value)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SBC A, {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def sbc_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]

        old_val = cpu.A
        new_val = old_val - n - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_val, cpu.A, new_val, n)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("SBC A, {}".format(n))

    @staticmethod
    def sbc_hl(cpu, _, logger):
        old_val = cpu.A
        value = cpu.ram[cpu.HL]
        new_val = old_val - value - (1 if cpu.CFlag else 0)
        cpu.A = new_val

        Flags.sub_flags(cpu, old_val, cpu.A, new_val, value)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("SBC A, (HL)")

    @staticmethod
    def xor_hl(cpu, _, logger):
        old = cpu.ram[cpu.HL]
        oldA = cpu.A
        cpu.A ^= old

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("XOR A, (HL)")

    @staticmethod
    def cp_hl(cpu, _, logger):
        n = cpu.ram[cpu.HL]
        value = cpu.A - n
        valueIn2s = Bits.twos_comp(value)

        Flags.cp_flags(cpu, n, cpu.A, value, valueIn2s)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("CP (HL)")

    @staticmethod
    def adc_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        old_val = cpu.A
        new_val = cpu.A + n + (1 if cpu.CFlag else 0)
        cpu.A = new_val

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set() if Bits.getNthBit(old_val ^ n ^ new_val, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.getNthBit(((old_val ^ n ^ 0x80) & (n ^ new_val)) >> 5, PVF) != 0 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new_val)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        logger.info("ADC A, {:02X}".format(n))

    @staticmethod
    def _or_hl(cpu, _, logger):
        val = cpu.ram[cpu.HL]
        new_val = cpu.A | val
        cpu.A = new_val

        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.XFlag = Bits.getNthBit(cpu.A, XF)
        cpu.YFlag = Bits.getNthBit(cpu.A, YF)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("OR (HL)")

    @staticmethod
    def daa(cpu, _, logger):
        oldA = cpu.A
        reg_a = cpu.A
        if cpu.NFlag:
            if (oldA & 0xF) > 0x9 or cpu.HFlag:
                reg_a = (reg_a - 0x06) & 0xFF
            if oldA > 0x99 or cpu.CFlag:
                reg_a = (reg_a - 0x60) & 0xFF
        else:
            if (oldA & 0xF) > 0x9 or cpu.HFlag:
                reg_a = (reg_a + 0x06) & 0xFF
            if oldA > 0x99 or cpu.CFlag:
                reg_a = (reg_a + 0x60) & 0xFF
        cpu.A = reg_a

        oldCF = cpu.CFlag
        cpu.CFlag = Bits.set() if oldA > 0x99 else oldCF
        cpu.HFlag = Bits.set() if Bits.getNthBit(oldA ^ reg_a, HF) != 0 else Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(reg_a) & 1 == 0 else Bits.reset()
        cpu.ZFlag = Bits.set() if reg_a == 0 else Bits.reset()
        cpu.XFlag = Bits.getNthBit(reg_a, XF)
        cpu.YFlag = Bits.getNthBit(reg_a, YF)
        cpu.SFlag = Bits.isNegative(cpu.A)
        logger.info("DAA")
