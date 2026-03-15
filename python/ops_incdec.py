# Z80 incdec opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsIncdec(object):

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
    def inc16(cpu, opcode, logger):

        regInd = (opcode & 0x30) >> 4
        newVal = cpu.Reg16(regInd) + 1
        cpu.Reg16(regInd, newVal)

        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("INC {}".format(IndexToReg.translate16Bit(regInd)))


    @staticmethod
    def inc_ix(cpu, _, logger):
        cpu.IX += 1

        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("INC IX")


    @staticmethod
    def inc_ixh(cpu, _, logger):
        old_high = cpu.IX >> 8
        low = cpu.IX & 255

        new_high = (old_high + 1) & 0xFF

        cpu.IX = Bits.make16bit(new_high, low)

        Flags.inc_flags(cpu, old_high, new_high)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("INC IXH")


    @staticmethod
    def dec_ixh(cpu, _, logger):
        old_high = cpu.IX >> 8
        low = cpu.IX & 255
        new_high = (old_high - 1) & 0xFF

        cpu.IX = Bits.make16bit(new_high, low)

        Flags.dec_flags(cpu, old_high, new_high)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DEC IXH")


    @staticmethod
    def dec_ixl(cpu, _, logger):
        high = cpu.IX >> 8
        old_low = cpu.IX & 255
        new_low = (old_low - 1) & 0xFF

        cpu.IX = Bits.make16bit(high, new_low)

        Flags.dec_flags(cpu, old_low, new_low)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DEC IXL")


    @staticmethod
    def inc_ixl(cpu, _, logger):
        high = cpu.IX >> 8
        old_low = cpu.IX & 255
        new_low = (old_low + 1) & 0xFF

        cpu.IX = Bits.make16bit(high, new_low)
        Flags.inc_flags(cpu, old_low, new_low)

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("INC IXL")


    @staticmethod
    def inc_iy(cpu, _, logger):
        cpu.IY += 1

        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("INC IY")

    @staticmethod
    def inc_iyh(cpu, _, logger):
        old_high = cpu.IY >> 8
        low = cpu.IY & 255
        new_high = (old_high + 1) & 0xFF
        cpu.IY = Bits.make16bit(new_high, low)
        Flags.inc_flags(cpu, old_high, new_high)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("INC IYH")

    @staticmethod
    def dec_iyh(cpu, _, logger):
        old_high = cpu.IY >> 8
        low = cpu.IY & 255
        new_high = (old_high - 1) & 0xFF
        cpu.IY = Bits.make16bit(new_high, low)
        Flags.dec_flags(cpu, old_high, new_high)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DEC IYH")

    @staticmethod
    def inc_iyl(cpu, _, logger):
        high = cpu.IY >> 8
        old_low = cpu.IY & 255
        new_low = (old_low + 1) & 0xFF
        cpu.IY = Bits.make16bit(high, new_low)
        Flags.inc_flags(cpu, old_low, new_low)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("INC IYL")

    @staticmethod
    def dec_iyl(cpu, _, logger):
        high = cpu.IY >> 8
        old_low = cpu.IY & 255
        new_low = (old_low - 1) & 0xFF
        cpu.IY = Bits.make16bit(high, new_low)
        Flags.dec_flags(cpu, old_low, new_low)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DEC IYL")

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
    def dec_mem_at_iy(cpu, _, logger):
        displacement = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IY + displacement
        value = cpu.ram[cpu.WZ]
        new_value = Bits.twos_comp(value-1)
        cpu.ram[cpu.WZ] = new_value

        Flags.dec_flags(cpu, value, new_value)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("DEC (IY+{:2X})".format(displacement))


    @staticmethod
    def inc_mem_at_iy(cpu, _, logger):
        displacement = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IY + displacement
        value = cpu.ram[cpu.WZ]
        new_value = Bits.twos_comp(value + 1)
        cpu.ram[cpu.WZ] = new_value

        Flags.inc_flags(cpu, value, new_value)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("INC (IY+{:2X})".format(displacement))


    @staticmethod
    def dec8b(cpu, opcode, logger):
        reg_index = (opcode >> 3) & 7
        old_val = cpu.regs[reg_index]
        cpu.regs[reg_index] = Bits.twos_comp(cpu.regs[reg_index]-1)

        Flags.dec_flags(cpu, old_val, cpu.regs[reg_index])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DEC {}".format(IndexToReg.translate8Bit(reg_index)))


    @staticmethod
    def dec_at_ix_d(cpu, _, logger):
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IX + d
        old_val = Bits.from_twos_comp(cpu.ram[cpu.WZ])
        new_val = Bits.twos_comp(old_val - 1)
        cpu.ram[cpu.WZ] = new_val

        Flags.dec_flags(cpu, old_val, new_val)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("DEC (IX+{:02X})".format(d))


    @staticmethod
    def inc_at_ix_d(cpu, _, logger):
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
        cpu.WZ = cpu.IX + d
        old_val = Bits.from_twos_comp(cpu.ram[cpu.WZ])
        new_val = Bits.twos_comp(old_val + 1)
        cpu.ram[cpu.WZ] = new_val

        Flags.inc_flags(cpu, old_val, new_val)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("INC (IX+{:02X})".format(d))


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

