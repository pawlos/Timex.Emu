# Aux class
from utility import Bits
from utility import IndexToReg, IndexToFlag


class Opcodes(object):

    @staticmethod
    def disableInterrupts(cpu, opcode, logger):
        cpu.iff1, cpu.iff2 = 0x00, 0x00
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DI")

    @staticmethod
    def enableInterrupts(cpu, opcode, logger):
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
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("XOR A")

    @staticmethod
    def ld16(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        loValue = cpu.ram[cpu.PC]
        hiValue = cpu.ram[cpu.PC]
        value = (hiValue << 8) + loValue

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
    def ld8n(cpu, opcode, logger):
        regInd = (opcode >> 3) & 7
        value = cpu.ram[cpu.PC]
        cpu.regs[regInd] = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD {}, {:02X}".format(
            IndexToReg.translate8Bit(regInd),
            value))

    @staticmethod
    def jp(cpu, opcode, logger):
        loValue = cpu.ram[cpu.PC]
        hiValue = cpu.ram[cpu.PC]
        value = (hiValue << 8) + loValue
        cpu.PC = value
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("JP {0:04X}".format(value))

    @staticmethod
    def out(cpu, opcode, logger):
        value = cpu.ram[cpu.PC]
        cpu.io[value] = cpu.A
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("OUT ({:02X}), A".format(value))

    @staticmethod
    def ldExt(cpu, opcode, logger):
        cpu.I = cpu.A
        cpu.m_cycles, cpu.t_states = 3, 9
        logger.info("LD I, A")

    @staticmethod
    def nop(cpu, opcode, logger):
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DEFB")

    @staticmethod
    def ld_addr(cpu, opcode, logger):
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
    def cp(cpu, opcode, logger):
        regInd = opcode & 7
        value = cpu.A - cpu.regs[regInd]
        cpu.ZFlag = Bits.isZero(value)
        cpu.CFlag = Bits.carryFlag(value)
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.halfCarrySub(cpu.A, value)
        cpu.SFlag = Bits.signFlag(value)
        cpu.PVFlag = Bits.overflow(value, cpu.A)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CP {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def jpnz(cpu, opcode, logger):
        pc = cpu.PC
        jumpOffset = Bits.twos_comp(cpu.ram[pc])

        no_jump = cpu.ZFlag

        if not no_jump:
            cpu.PC = pc + jumpOffset+1
            cpu.m_cycles, cpu.t_states = 1, 5

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR NZ, {0:04X}".format(pc+jumpOffset+1))

    @staticmethod
    def jpnc(cpu, opcode, logger):
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
        cpu.A = cpu.A & cpu.regs[regInd]
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("AND A")

    @staticmethod
    def _and_hl(cpu, opcode, logger):
        val = cpu.ram[cpu.HL]
        cpu.A = cpu.A & val

        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.signInTwosComp(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("AND (HL)")

    @staticmethod
    def sbc(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        value = cpu.Reg16(regInd)

        oldHL = cpu.HL

        cpu.HL = cpu.HL - value - (1 if cpu.CFlag else 0)

        cpu.SFlag = Bits.signFlag(cpu.HL, bits=16)
        cpu.ZFlag = Bits.isZero(cpu.HL)
        cpu.HFlag = Bits.halfCarrySub16(oldHL, cpu.HL)
        cpu.PVFlag = Bits.overflow(oldHL, cpu.HL, bits=16)
        cpu.NFlag = Bits.set()
        cpu.CFlag = Bits.borrow(cpu.HL, bits=16)

        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("SBC HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add16(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        value = cpu.Reg16(regInd)

        oldHL = cpu.HL
        cpu.HL = cpu.HL + value

        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag16(oldHL, cpu.HL)
        cpu.HFlag = Bits.carryFlag16(oldHL, cpu.HL, bits=11)
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("ADD HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def inc16(cpu, opcode, logger):

        regInd = (opcode & 0x30) >> 4
        cpu.Reg16(regInd, cpu.Reg16(regInd) + 1)

        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("INC {0}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def jrz(cpu, opcode, logger):
        pc = cpu.PC
        jumpTo = pc + Bits.twos_comp(cpu.ram[pc]) + 1

        no_jump = cpu.ZFlag is False

        if not no_jump:
            cpu.PC = jumpTo
            cpu.m_cycles, cpu.t_states = 1, 5

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR Z, {:04X}".format(jumpTo))

    @staticmethod
    def exx(cpu, opcode, logger):

        cpu.BC, cpu.BCPrim = cpu.BCPrim, cpu.BC
        cpu.DE, cpu.DEPrim = cpu.DEPrim, cpu.DE
        cpu.HL, cpu.HLPrim = cpu.HLPrim, cpu.HL

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EXX")

    @staticmethod
    def ldNnRr(cpu, opcode, logger):
        regInd = (opcode & 0x30) >> 4
        high = cpu.ram[cpu.PC]
        low = cpu.ram[cpu.PC]
        addr = (high << 8) + low

        value = cpu.Reg16(regInd)

        cpu.ram[addr + 1] = value >> 8
        cpu.ram[addr] = value & 0xFF
        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD ({:04X}), {}".format(addr, IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def ldNnHl(cpu, opcode, logger):
        high = cpu.ram[cpu.PC]
        low = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        cpu.ram[addr+1] = cpu.H
        cpu.ram[addr] = cpu.L

        cpu.m_cycles, cpu.t_states = 5, 16
        logger.info("LD ({:04X}), HL".format(addr))

    @staticmethod
    def inc8(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        oldValue = cpu.regs[index]
        cpu.regs[index] = Bits.limitTo8Bits(cpu.regs[index] + 1)

        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.regs[index])
        cpu.HFlag = Bits.halfCarrySub(oldValue, cpu.regs[index])
        cpu.PVFlag = True if oldValue == 0x7f else False
        cpu.SFlag = Bits.isNegative(cpu.regs[index])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("INC {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def ex_de_hl(cpu, opcode, logger):
        cpu.DE, cpu.HL = cpu.HL, cpu.DE

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("EX DE, HL")

    @staticmethod
    def ex_af_afprim(cpu, opcode, logger):
        cpu.AF, cpu.AFPrim = cpu.AFPrim, cpu.AF
        cpu.m_cycles, cpu.t_states = 1, 4

        logger.info("EX AF, AF'")

    @staticmethod
    def lddr(cpu, opcode, logger):
        isZero = cpu.BC == 0
        while True:
            cpu.ram[cpu.DE] = cpu.ram[cpu.HL]
            cpu.HL = cpu.HL - 1
            cpu.DE = cpu.DE - 1
            cpu.BC = cpu.BC - 1
            if cpu.BC == 0:
                cpu.NFlag = Bits.reset()
                cpu.HFlag = Bits.reset()
                cpu.PVFlag = Bits.reset()
                break

        cpu.m_cycles, cpu.t_states = 4 if isZero else 5, 16 if isZero else 21

        logger.info("LDDR")

    @staticmethod
    def ldHl_addr(cpu, opcode, logger):
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        cpu.L = cpu.ram[addr]
        cpu.H = cpu.ram[addr+1]
        cpu.m_cycles, cpu.t_states = 5, 16
        logger.info("LD HL, ({:04X})".format(addr))

    @staticmethod
    def ld_sp_hl(cpu, opcode, logger):
        cpu.SP = cpu.HL
        cpu.m_cycles, cpu.t_states = 1, 6
        logger.info("LD SP, HL")

    @staticmethod
    def im1(cpu, opcode, logger):
        cpu.im = 1

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 1")

    @staticmethod
    def ldiy(cpu, opcode, logger):
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        imm = (high << 8) + low
        cpu.IY = imm
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("LD IY, {:04X}".format(imm))

    @staticmethod
    def ldir(cpu, opcode, logger):
        wasZero = cpu.BC == 0
        while True:
            hl_mem = cpu.ram[cpu.HL]
            cpu.ram[cpu.DE] = hl_mem
            cpu.HL = cpu.HL + 1
            cpu.DE = cpu.DE + 1
            cpu.BC = cpu.BC - 1
            if cpu.BC == 0:
                break
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 4 if wasZero else 5, 16 if wasZero else 21
        logger.info("LDIR")

    @staticmethod
    def ldnn_a(cpu, opcode, logger):
        high = cpu.ram[cpu.PC]
        low = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        cpu.ram[addr] = cpu.A

        cpu.m_cycles, cpu.t_states = 4, 13
        logger.info("LD ({:04X}), A".format(addr))

    @staticmethod
    def dec_mem_at_iy(cpu, opcode, logger):
        displacement = cpu.ram[cpu.PC]
        addr = cpu.IY + displacement
        value = cpu.ram[addr]
        new_value = value - 1
        cpu.ram[addr] = new_value

        cpu.NFlag = Bits.set()
        cpu.SFlag = Bits.isNegative(new_value)
        cpu.ZFlag = Bits.isZero(new_value)
        cpu.PVFlag = True if value == 0x80 else False
        cpu.HFlag = Bits.halfCarrySub(value, new_value)
        logger.info("DEC (IY+{:2X})".format(displacement))

    @staticmethod
    def bit_set(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        val = cpu.ram[cpu.IY+index]
        val |= (1 << bit)
        cpu.ram[cpu.IY+index] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("SET {},(IY+{:02X})".format(bit, index))

    @staticmethod
    def bit_res(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        val = cpu.ram[cpu.IY+index]
        val = Bits.setNthBit(val, bit, 0)
        cpu.ram[cpu.IY+index] = val

        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("RES {}, (IY+{:02X})".format(bit, index))

    @staticmethod
    def bit_bit(cpu, opcode, logger):
        index = (opcode >> 8) & 255
        bit = (opcode >> 3) & 7
        cpu.ZFlag = cpu.ram[cpu.IY+index] & (1 << bit) != 0
        cpu.HFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 5, 20
        logger.info("BIT {:X}, (IY+{:02X})".format(bit, index))

    @staticmethod
    def call(cpu, opcode, logger):
        pc = cpu.PC
        addr_lo = cpu.ram[pc]
        pc += 1
        addr_hi = cpu.ram[pc]
        addr = (addr_hi << 8) + addr_lo
        pc += 1
        cpu.ram[cpu.SP - 1] = pc >> 8
        cpu.ram[cpu.SP - 2] = (pc & 255)
        cpu.SP = cpu.SP - 2
        cpu.PC = addr

        cpu.m_cycles, cpu.t_states = 5, 17
        logger.info("CALL {:04X}".format(addr))

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
    def djnz(cpu, opcode, logger):
        pc = cpu.PC
        e = cpu.ram[pc]
        cpu.B = cpu.B - 1
        pc = pc + Bits.twos_comp(e) + 1
        if cpu.B != 0:
            cpu.m_cycles, cpu.t_states = 1, 5
            cpu.PC = pc

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("DJNZ {:04X}".format(pc))

    @staticmethod
    def add_iy(cpu, opcode, logger):
        d = cpu.ram[cpu.PC]
        value = cpu.A + cpu.ram[cpu.IY+d]

        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.CFlag = Bits.carryFlag(value)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.overflow(cpu.A, value)
        cpu.HFlag = Bits.halfCarrySub(cpu.A, value)

        cpu.A = value
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD A, (IY+{:02X})".format(d))

    @staticmethod
    def sub_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        value = cpu.A - n

        cpu.NFlag = Bits.set()
        cpu.ZFlag = Bits.isZero(value)
        cpu.HFlag = Bits.halfCarrySub(cpu.A, value)
        cpu.PVFlag = Bits.overflow(cpu.A, value)
        cpu.CFlag = Bits.carryFlag(value)
        cpu.A = value

        logger.info("SUB {:02X}".format(n))

    @staticmethod
    def push(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        value = cpu.Reg16(regInd, af=True)

        cpu.ram[cpu.SP-1] = value >> 8
        cpu.ram[cpu.SP-2] = value & 255
        cpu.SP -= 2
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("PUSH {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def sub_r(cpu, opcode, logger):
        index = opcode & 7

        old_A = cpu.A
        cpu.A = cpu.A - cpu.regs[index]

        cpu.NFlag = Bits.set()
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.halfCarrySub(old_A, cpu.A)
        cpu.PVFlag = Bits.overflow(cpu.A, old_A)
        cpu.CFlag = Bits.carryFlag(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SUB {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def rrca(cpu, opcode, logger):
        cflag = Bits.getNthBit(cpu.A, 0)
        cpu.A = Bits.setNthBit(cpu.A >> 1, 7, cflag)
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 1, 4

        logger.info("RRCA")

    @staticmethod
    def rlca(cpu, opcode, logger):
        cflag = Bits.getNthBit(cpu.A, 7)
        cpu.A = Bits.setNthBit(cpu.A << 1, 0, cflag)
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RLCA")

    @staticmethod
    def rlc_b(cpu, opcode, logger):
        cflag = Bits.getNthBit(cpu.B, 7)
        cpu.B = Bits.setNthBit(cpu.B << 1, 0, cflag)
        cpu.CFlag = Bits.set() if cflag != 0 else Bits.reset()

        #cpu.m_cycles, cpu.t_states = ?, ?
        logger.info("RLC B")


    @staticmethod
    def and_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = cpu.A & n

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.set()
        cpu.PVFlag = Bits.overflow(old, cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("AND {:02X}".format(n))

    @staticmethod
    def or_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = cpu.A | n

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.overflow(old, cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("OR {:02X}".format(n))

    @staticmethod
    def ret(cpu, opcode, logger):
        low = cpu.ram[cpu.SP]
        high = cpu.ram[cpu.SP+1]
        addr = (high << 8) + low
        cpu.SP += 2
        cpu.PC = addr

        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("RET")

    @staticmethod
    def rst(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        pc = cpu.PC
        cpu.ram[cpu.SP - 1] = pc >> 8
        cpu.ram[cpu.SP - 2] = pc & 8
        cpu.SP -= 2

        cpu.PC = cpu.rst_jumps[index]
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("RST {:02X}".format(cpu.rst_jumps[index]))

    @staticmethod
    def pop(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        high = cpu.ram[cpu.SP+1]
        low = cpu.ram[cpu.SP]
        cpu.SP += 2
        val = (high << 8) + low

        cpu.Reg16(regInd, val, af=True)

        cpu.m_cycles, cpu.t_states = 3, 7
        logger.info("POP {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def ldiy_d_n(cpu, opcode, logger):
        d = cpu.ram[cpu.PC]
        n = cpu.ram[cpu.PC]
        cpu.ram[cpu.IY + d] = n
        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD (IY+{:02X}),{:02X}".format(d, n))

    @staticmethod
    def add_r(cpu, opcode, logger):
        index = (opcode & 7)
        old = cpu.A
        cpu.A = old + cpu.regs[index]

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.halfCarrySub(old, cpu.A)
        cpu.PVFlag = Bits.overflow(old, cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("ADD A, {}".format(IndexToReg.translate8Bit(index)))

    @staticmethod
    def add_r_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A

        value = cpu.A + n
        cpu.A = value

        cpu.SFlag = Bits.isNegative(value)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.halfCarrySub(old, cpu.A)
        cpu.PVFlag = Bits.overflow(old, cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(value)

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

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("OR {}".format(IndexToReg.translate8Bit(regInd)))

    @staticmethod
    def jr_e(cpu, opcode, logger):
        pc = cpu.PC
        jumpOffset = Bits.twos_comp(cpu.ram[pc])

        cpu.PC = pc + jumpOffset + 1
        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("JR {0:x}".format(jumpOffset))

    @staticmethod
    def ld16_nn(cpu, opcode, logger):
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        value_low = cpu.ram[addr]
        value_high = cpu.ram[addr+1]
        value = (value_high << 8) + value_low
        regInd = (opcode >> 4) & 3

        cpu.Reg16(regInd, value)

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD {},({:0X})".format(IndexToReg.translate16Bit(regInd), addr))

    @staticmethod
    def ld_a_bc(cpu, opcode, logger):
        value = cpu.ram[cpu.BC]
        cpu.A = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD A, (BC)")

    @staticmethod
    def ld_a_de(cpu, opcode, logger):
        value = cpu.ram[cpu.DE]
        cpu.A = value

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD A, (DE)")

    @staticmethod
    def ld_a_nn(cpu, opcode, logger):
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        cpu.A = cpu.ram[addr]
        cpu.m_cycles, cpu.t_states = 4, 13
        logger.info("LD A, ({:04X})".format(addr))

    @staticmethod
    def ld_bc_a(cpu, opcode, logger):
        cpu.ram[cpu.BC] = cpu.A
        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD (BC), A")

    @staticmethod
    def ld_de_a(cpu, opcode, logger):
        cpu.ram[cpu.DE] = cpu.A
        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("LD (DE), A")

    @staticmethod
    def lra(cpu, opcode, logger):
        cflag = Bits.getNthBit(cpu.A, 7)
        cpu.A = Bits.setNthBit((cpu.A << 1), 0, cpu.CFlag)
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("LRA")

    @staticmethod
    def rra(cpu, opcode, logger):
        cflag = Bits.getNthBit(cpu.A, 0)
        cpu.A = Bits.setNthBit((cpu.A >> 1), 7, cpu.CFlag)
        cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("RRA")

    @staticmethod
    def rld(cpu, opcode, logger):
        low_a = cpu.A & 0x0F
        mem_hl = cpu.ram[cpu.HL]
        low_hl = mem_hl & 0x0F
        high_hl = (mem_hl & 0xF0) >> 4
        cpu.A = ((cpu.A & 0xF0) | high_hl)
        mem_hl = (low_hl << 4) | low_a
        cpu.ram[cpu.HL] = mem_hl
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.m_cycles, cpu.t_states = 5, 18
        logger.info("RLD")

    @staticmethod
    def rrd(cpu, opcode, logger):
        low_a = cpu.A & 0x0F
        mem_hl = cpu.ram[cpu.HL]
        low_hl = mem_hl & 0x0F
        high_hl = (mem_hl & 0xF0) >> 4
        cpu.A = (cpu.A & 0xF0) | low_hl
        mem_hl = (low_a << 4) | high_hl
        cpu.ram[cpu.HL] = mem_hl
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.m_cycles, cpu.t_states = 5, 18
        logger.info("RRD")

    @staticmethod
    def neg(cpu, opcode, logger):
        old = cpu.A
        cpu.A = 0 - cpu.A
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.set() if old == 0x80 else Bits.reset()
        cpu.CFlag = Bits.isZero(old)
        cpu.HFlag = Bits.halfCarrySub(0x0, old)
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("NEG")

    @staticmethod
    def ld_r_iy_d(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        d = cpu.ram[cpu.PC]
        cpu.regs[index] = cpu.ram[cpu.IY + d]

        cpu.m_cycles, cpu.t_states = 5, 19
        logger.info("LD {}, (IY+{:02X})".format(IndexToReg.translate8Bit(index), d))

    @staticmethod
    def ld_ix_nn(cpu, opcode, logger):
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        addr = (high << 8) + low
        low_val = cpu.ram[addr]
        high_val = cpu.ram[addr+1]
        cpu.IX = (high_val << 8) + low_val

        cpu.m_cycles, cpu.t_states = 6, 20
        logger.info("LD IX, ({:04X})".format(addr))

    @staticmethod
    def ldra(cpu, opcode, logger):
        cpu.R = cpu.A
        cpu.m_cycles, cpu.t_states = 2, 9
        logger.info("LD R, A")

    @staticmethod
    def ldar(cpu, opcode, logger):
        cpu.A = cpu.R

        cpu.SFlag = Bits.isNegative(cpu.R)
        cpu.ZFlag = Bits.isZero(cpu.R)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.iff2 == 1 else Bits.reset()
        cpu.NFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 9
        logger.info("LD A, R")

    @staticmethod
    def im2(cpu, opcode, logger):
        cpu.im = 2

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 2")

    @staticmethod
    def im0(cpu, opcode, logger):
        cpu.im = 0

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 0")

    @staticmethod
    def pop_ix(cpu, opcode, logger):
        low = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        high = cpu.ram[cpu.SP]
        cpu.SP = cpu.SP + 1
        cpu.IX = (high << 8) + low
        cpu.m_cycles, cpu.t_states = 4, 14
        logger.info("POP IX")

    @staticmethod
    def jp_cond(cpu, opcode, logger):
        cond = (opcode >> 3) & 7
        low = cpu.ram[cpu.PC]
        high = cpu.ram[cpu.PC]
        addr = (high << 8) + low

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
            cpu.PC = addr

        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("JP {} {:04X}".format(IndexToFlag.translate(cond), addr))

    @staticmethod
    def call_cond(cpu, opcode, logger):
        cond = (opcode >> 3) & 7
        pc = cpu.PC
        addr_lo = cpu.ram[pc]
        pc += 1
        addr_hi = cpu.ram[pc]
        addr = (addr_hi << 8) + addr_lo
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

        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("CALL {}, {:04X}".format(
            IndexToFlag.translate(cond),
            addr))

    @staticmethod
    def dec8b(cpu, opcode, logger):
        reg_index = (opcode >> 3) & 7
        old_val = cpu.regs[reg_index]
        cpu.regs[reg_index] = cpu.regs[reg_index] - 1

        cpu.ZFlag = Bits.isZero(cpu.regs[reg_index])
        cpu.SFlag = Bits.isNegative(cpu.regs[reg_index])
        cpu.NFlag = Bits.set()
        cpu.PVFlag = Bits.halfCarrySub(old_val, cpu.regs[reg_index])
        cpu.HFlag = Bits.halfCarrySub(old_val, cpu.regs[reg_index])

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("DEC {}".format(IndexToReg.translate8Bit(reg_index)))

    @staticmethod
    def dec_at_hl(cpu, opcode, logger):
        old_val = cpu.ram[cpu.HL]
        new_val = old_val - 1
        cpu.ram[cpu.HL] = new_val
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.NFlag = Bits.set()
        cpu.PVFlag = Bits.halfCarrySub(old_val, new_val)
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("DEC (HL)")

    @staticmethod
    def dec_at_ix_d(cpu, opcode, logger):
        d = cpu.ram[cpu.PC]
        old_val = cpu.ram[cpu.IX+d]
        new_val = old_val - 1
        cpu.ram[cpu.IX+d] = new_val
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.NFlag = Bits.set()
        cpu.PVFlag = Bits.halfCarrySub(old_val, new_val)
        cpu.m_cycles, cpu.t_states = 6, 23
        logger.info("DEC (IX+{:02X})".format(d))

    @staticmethod
    def cpl(cpu, opcode, logger):
        old = cpu.A
        new = ~old
        cpu.A = new
        cpu.HFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CPL")

    @staticmethod
    def ccf(cpu, opcode, logger):
        cpu.CFlag = Bits.flip(cpu.CFlag)
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("CCF")

    @staticmethod
    def scf(cpu, opcode, logger):
        cpu.CFlag = Bits.set()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SCF")

    @staticmethod
    def hlt(cpu, opcode, logger):
        logger.info("HALT")
        cpu.m_cycles, cpu.t_states = 1, 4
        cpu.halted = Bits.set()

    @staticmethod
    def add_Hl_rr_c(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd)

        old = cpu.HL
        cpu.HL = cpu.HL + val + (1 if cpu.CFlag else 0)
        cpu.SFlag = Bits.signFlag(cpu.HL, bits=16)
        cpu.ZFlag = Bits.isZero(cpu.HL)
        cpu.HFlag = Bits.halfCarrySub16(old, cpu.HL)
        cpu.PVFlag = Bits.overflow(old, cpu.HL, bits=16)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.set() if (Bits.getNthBit(old, 15) == 1 and
                                   Bits.getNthBit(cpu.HL, 15) == 0) else Bits.reset()
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADC HL, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add_ix_rr(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd, ix=True)

        old = cpu.IX
        cpu.IX = cpu.IX + val
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.carryFlagAdd16(old, cpu.IX)
        cpu.CFlag = Bits.overflow(old, cpu.IX, bits=16)

        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD IX, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def add_iy_rr(cpu, opcode, logger):
        regInd = (opcode >> 4) & 3
        val = cpu.Reg16(regInd, iy=True)

        old = cpu.IY
        cpu.IY = cpu.IY + val
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.carryFlagAdd16(old, cpu.IY)
        cpu.CFlag = Bits.overflow(old, cpu.IY, bits=16)
        cpu.m_cycles, cpu.t_states = 4, 15
        logger.info("ADD IY, {}".format(IndexToReg.translate16Bit(regInd)))

    @staticmethod
    def jp_hl(cpu, opcode, logger):
        cpu.PC = cpu.HL
        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("JP HL")

    @staticmethod
    def jp_ix(cpu, opcode, logger):
        cpu.PC = cpu.IX
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("JP IX")

    @staticmethod
    def jp_iy(cpu, opcode, logger):
        cpu.PC = cpu.IY
        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("JP IY")

    @staticmethod
    def inc_at_hl(cpu, opcode, logger):
        old_val = cpu.ram[cpu.HL]
        new_val = old_val + 1
        cpu.ram[cpu.HL] = new_val
        cpu.ZFlag = Bits.isZero(new_val)
        cpu.SFlag = Bits.isNegative(new_val)
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.halfCarrySub(old_val, new_val)

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("INC (HL)")

    @staticmethod
    def jr_c(cpu, opcode, logger):
        pc = cpu.PC + 1
        jumpOffset = Bits.twos_comp(cpu.ram[pc]) - 2
        no_jump = cpu.CFlag is False
        pc = pc + jumpOffset
        if not no_jump:
            cpu.PC = pc
            cpu.m_cycles, cpu.t_states = 1, 5
        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JP C {0:04X}".format(pc))

    @staticmethod
    def portIn(cpu, opcode, logger):
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
            low = cpu.ram[cpu.SP]
            high = cpu.ram[cpu.SP+1]
            addr = (high << 8) + low
            cpu.SP += 2
            cpu.PC = addr
            cpu.m_cycles, cpu.t_states = 2, 6

        cpu.m_cycles, cpu.t_states = 1, 5
        logger.info("RET {}".format(cond_name))

    @staticmethod
    def srl_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        old_val = cpu.regs[reg_idx]
        cpu.regs[reg_idx] = (old_val >> 1)
        last_bit = Bits.getNthBit(old_val, 0)

        cpu.CFlag = Bits.set() if last_bit == 1 else Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.regs[reg_idx])
        cpu.PVFlag = Bits.isEvenParity(cpu.regs[reg_idx])
        cpu.SFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("SRL {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def adc_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        old_val = cpu.A
        cpu.A = old_val + cpu.regs[reg_idx] + (1 if cpu.CFlag else 0)

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.NFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("ADC A, {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def add_a_hl(cpu, opcode, logger):
        oldA = cpu.A
        value = cpu.A + cpu.ram[cpu.HL]
        cpu.A = value

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(value)
        cpu.PVFlag = Bits.overflow(oldA, cpu.A)
        cpu.HFlag = Bits.halfCarrySub(cpu.A, oldA)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("ADD A, (HL)")

    @staticmethod
    def cp_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        new = old - n
        cpu.SFlag = Bits.isNegative(new)
        cpu.ZFlag = Bits.isZero(new)
        cpu.HFlag = Bits.halfCarrySub(old, new)
        cpu.PVFlag = Bits.overflow(old, new)
        cpu.NFlag = Bits.set()
        cpu.CFlag = Bits.carryFlag(new)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("CP {:02X}".format(n))

    @staticmethod
    def xor_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old = cpu.A
        cpu.A = old ^ n

        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("XOR {:02X}".format(n))

    @staticmethod
    def in_a_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        cpu.A = cpu.io[n]

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("IN A, ({:02X}".format(n))

    @staticmethod
    def adc_a_hl(cpu, opcode, logger):
        v = cpu.ram[cpu.HL]
        old = cpu.A
        cpu.A += v

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.overflow(old, cpu.A)
        cpu.HFlag = Bits.halfCarrySub(cpu.A, old)
        cpu.CFlag = Bits.carryFlag(old + v)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("ADC A, (HL)")

    @staticmethod
    def sub_a_hl(cpu, opcode, logger):
        v = cpu.ram[cpu.HL]
        old_A = cpu.AFPrim
        cpu.A -= v

        cpu.NFlag = Bits.set()
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.halfCarrySub(old_A, cpu.A)
        cpu.PVFlag = Bits.overflow(old_A, cpu.A)
        cpu.CFlag = Bits.carryFlag(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("SUB A, (HL)")

    @staticmethod
    def sbc_r(cpu, opcode, logger):
        reg_idx = (opcode & 7)
        old_val = cpu.A
        cpu.A = old_val - cpu.regs[reg_idx] - (1 if cpu.CFlag else 0)

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.halfCarrySub(old_val, cpu.A)
        cpu.PVFlag = Bits.overflow(old_val, cpu.A)
        cpu.CFlag = Bits.carryFlag(cpu.A)

        cpu.m_cycles, cpu.t_states = 1, 4
        logger.info("SDC A, {}".format(IndexToReg.translate8Bit(reg_idx)))

    @staticmethod
    def sbc_hl(cpu, opcode, logger):
        old_val = cpu.A
        cpu.A = old_val - cpu.ram[cpu.HL] - (1 if cpu.CFlag else 0)

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.halfCarrySub(old_val, cpu.A)
        cpu.PVFlag = Bits.overflow(old_val, cpu.A)
        cpu.CFlag = Bits.carryFlag(cpu.A)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("SDC A, (HL)")

    @staticmethod
    def xor_hl(cpu, opcode, logger):
        cpu.A ^= cpu.ram[cpu.HL]

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.isEvenParity(cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("XOR (HL)")

    @staticmethod
    def cp_hl(cpu, opcode, logger):
        value = cpu.A - cpu.ram[cpu.HL]

        cpu.ZFlag = Bits.isZero(value)
        cpu.CFlag = Bits.carryFlag(value)
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.halfCarrySub(cpu.A, value)
        cpu.SFlag = Bits.signFlag(value)
        cpu.PVFlag = Bits.overflow(value, cpu.A)
        cpu.m_cycles, cpu.t_states = 1, 7
        logger.info("CP (HL)")

    @staticmethod
    def adc_n(cpu, opcode, logger):
        n = cpu.ram[cpu.PC]
        old_val = cpu.A
        new_val = cpu.A + n + (1 if cpu.CFlag else 0)
        cpu.A = new_val

        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.HFlag = Bits.halfCarrySub(old_val, cpu.A)
        cpu.PVFlag = Bits.overflow(old_val, cpu.A)
        cpu.NFlag = Bits.reset()
        cpu.CFlag = Bits.carryFlag(new_val)

        logger.info("ADC A, {:02X}".format(n))

    @staticmethod
    def _or_hl(cpu, opcode, logger):
        cpu.A = cpu.A | cpu.ram[cpu.HL]
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.ZFlag = Bits.isZero(cpu.A)
        cpu.SFlag = Bits.isNegative(cpu.A)
        cpu.PVFlag = Bits.isEvenParity(cpu.A)

        cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("OR (HL)")
