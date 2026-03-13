# Z80 bitshift opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsBitshift(object):

    @staticmethod
    def bit_set_iy(cpu, opcode, logger):
        index = Bits.from_twos_comp((opcode >> 8) & 255)
        bit = (opcode >> 3) & 7
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        val |= (1 << bit)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("SET {},(IY+{:02X})".format(bit, index))


    @staticmethod
    def bit_set_ix(cpu, opcode, logger):
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        logger.info("SET {}, {}".format(b, IndexToReg.translate8Bit(r)))


    @staticmethod
    def bit_res(cpu, opcode, logger):
        index = Bits.from_twos_comp((opcode >> 8) & 255)
        bit = (opcode >> 3) & 7
        cpu.WZ = cpu.IY + index
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, bit, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RES {}, (IY+{:02X})".format(bit, index))


    @staticmethod
    def bit_bit_iy(cpu, opcode, logger):
        index = Bits.from_twos_comp((opcode >> 8) & 255)
        bit = (opcode >> 3) & 7

        cpu.WZ = cpu.IY + index
        Flags.ibit_flags(cpu, Bits.getNthBit(cpu.ram[cpu.WZ], bit), cpu.W, bit)

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("BIT {:X}, (IY+{:02X})".format(bit, index))


    @staticmethod
    def bit_bit_ix(cpu, opcode, logger):
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        index = Bits.from_twos_comp((opcode >> 8) & 255)
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
        n = Bits.from_twos_comp((opcode >> 8) & 0xff)

        cpu.WZ = cpu.IX + n
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, b, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RES {}, (IX+{:02X})".format(b, n))


    @staticmethod
    def bit_res_iy(cpu, opcode, logger):
        b = (opcode >> 3) & 7
        n = Bits.from_twos_comp((opcode >> 8) & 0xff)

        cpu.WZ = cpu.IY + n
        val = cpu.ram[cpu.WZ]
        val = Bits.setNthBit(val, b, 0)
        cpu.ram[cpu.WZ] = val

        cpu.m_cycles, cpu.t_states = 6, 23
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

