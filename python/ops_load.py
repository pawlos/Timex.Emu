# Z80 load opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsLoad(object):

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
        if regInd == 4:
            value = cpu.IX >> 8
        elif regInd == 5:
            value = cpu.IX & 255
        else:
            value = cpu.regs[regInd]
        cpu.IX = Bits.make16bit(high_val, value)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IXL, {}".format(
            IndexToReg.translate8Bit(regInd)))


    @staticmethod
    def ld_ixl_ixh(cpu, _, logger):
        ixh = cpu.IX >> 8
        cpu.IX = Bits.make16bit(ixh, ixh)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("LD IXL, IXH")


    @staticmethod
    def ld_iyl_iyh(cpu, _, logger):
        iyh = cpu.IY >> 8
        cpu.IY = Bits.make16bit(iyh, iyh)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("LD IYL, IYH")


    @staticmethod
    def ld_ixh_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        low_val = cpu.IX & 255
        if regInd == 4:
            value = cpu.IX >> 8
        elif regInd == 5:
            value = cpu.IX & 255
        else:
            value = cpu.regs[regInd]
        cpu.IX = Bits.make16bit(value, low_val)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IXH, {}".format(
            IndexToReg.translate8Bit(regInd)))


    @staticmethod
    def ld_iyl_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        high_val = cpu.IY >> 8
        if regInd == 4:
            value = cpu.IY >> 8
        elif regInd == 5:
            value = cpu.IY & 255
        else:
            value = cpu.regs[regInd]
        cpu.IY = Bits.make16bit(high_val, value)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LD IYL, {}".format(
            IndexToReg.translate8Bit(regInd)))


    @staticmethod
    def ld_iyh_r(cpu, opcode, logger):
        regInd = (opcode & 7)
        low_val = cpu.IY & 255
        if regInd == 4:
            value = cpu.IY >> 8
        elif regInd == 5:
            value = cpu.IY & 255
        else:
            value = cpu.regs[regInd]
        cpu.IY = Bits.make16bit(value, low_val)

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
    def ld_addr(cpu, _, logger):
        value = cpu.ram[cpu.PC]
        cpu.ram[cpu.HL] = value
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("LD (HL), {:02X}".format(value))


    @staticmethod
    def ld_nn_ix(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        value = cpu.IX

        cpu.ram[cpu.WZ] = value & 0xFF
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = value >> 8

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD ({:04X}), IX")


    @staticmethod
    def ld_nn_iy(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        value = cpu.IY

        cpu.ram[cpu.WZ] = value & 0xFF
        cpu.WZ += 1
        cpu.ram[cpu.WZ] = value >> 8

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD ({:04X}), IY")


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
    def ex_de_hl(cpu, _, logger):
        cpu.DE, cpu.HL = cpu.HL, cpu.DE

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EX DE, HL")


    @staticmethod
    def ex_sp_hl(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        high = cpu.ram[cpu.SP + 1]
        cpu.ram[cpu.SP] = cpu.L
        cpu.ram[cpu.SP + 1] = cpu.H
        cpu.L = low
        cpu.H = high
        cpu.WZ = cpu.HL

        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("EX (SP), HL")

    @staticmethod
    def ex_sp_ix(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        high = cpu.ram[cpu.SP + 1]
        cpu.ram[cpu.SP] = cpu.IX & 0xFF
        cpu.ram[cpu.SP + 1] = cpu.IX >> 8
        cpu.IX = (high << 8) | low
        cpu.WZ = cpu.IX

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("EX (SP), IX")

    @staticmethod
    def ex_sp_iy(cpu, _, logger):
        low = cpu.ram[cpu.SP]
        high = cpu.ram[cpu.SP + 1]
        cpu.ram[cpu.SP] = cpu.IY & 0xFF
        cpu.ram[cpu.SP + 1] = cpu.IY >> 8
        cpu.IY = (high << 8) | low
        cpu.WZ = cpu.IY

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("EX (SP), IY")

    @staticmethod
    def ld_sp_ix(cpu, _, logger):
        cpu.SP = cpu.IX
        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("LD SP, IX")

    @staticmethod
    def ld_sp_iy(cpu, _, logger):
        cpu.SP = cpu.IY
        cpu.m_cycles, cpu.t_states = 2, 10
        logger.info("LD SP, IY")

    @staticmethod
    def ex_af_afprim(cpu, _, logger):
        cpu.AF, cpu.AFPrim = cpu.AFPrim, cpu.AF
        cpu.m_cycles, cpu.t_states = 1, 4

        logger.info("EX AF, AF'")


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
    def ldiy(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]
        imm = cpu.WZ

        cpu.IY = imm

        cpu.WZ += 1
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("LD IY, {:04X}".format(imm))


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
    def ldiy_d_r(cpu, opcode, logger):
        regInd = opcode & 7
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
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
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
        n = cpu.ram[cpu.PC]

        cpu.WZ = cpu.IY + d
        cpu.ram[cpu.WZ] = n
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IY+{:02X}),{:02X}".format(d, n))


    @staticmethod
    def ld_r_hl(cpu, opcode, logger):
        index = (opcode >> 3) & 7

        value = cpu.ram[cpu.HL]

        cpu.regs[index] = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD {}, (HL)".format(IndexToReg.translate8Bit(index)))


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
    def ld_r_iy_d(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
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
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])

        cpu.WZ = cpu.IX + d
        cpu.regs[r] = cpu.ram[cpu.WZ]
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD {}, (IX+{})".format(IndexToReg.translate8Bit(r), d))


    @staticmethod
    def ld_at_ix_d_nn(cpu, _, logger):
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
        n = cpu.ram[cpu.PC]

        cpu.WZ = cpu.IX + d
        cpu.ram[cpu.WZ] = n
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IX+{}), {}".format(d,n))


    @staticmethod
    def ld_at_ix_d_r(cpu, opcode, logger):
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
        r = opcode & 7
        cpu.WZ = cpu.IX + d
        cpu.ram[cpu.WZ] = cpu.regs[r]
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IX+{}), {}".format(d, IndexToReg.translate8Bit(r)))


    @staticmethod
    def ld_at_iy_d_r(cpu, opcode, logger):
        d = Bits.from_twos_comp(cpu.ram[cpu.PC])
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

