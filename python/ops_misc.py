# Z80 misc opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsMisc(object):

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
    def im1(cpu, _, logger):
        cpu.im = 1

        cpu.m_cycles, cpu.t_states = 2, 8
        logger.info("IM 1")


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
    def ldai(cpu, _, logger):
        cpu.A = cpu.I

        cpu.SFlag = Bits.isNegative(cpu.I)
        cpu.ZFlag = Bits.isZero(cpu.I)
        cpu.HFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if cpu.iff2 == 1 else Bits.reset()
        cpu.NFlag = Bits.reset()

        cpu.m_cycles, cpu.t_states = 2, 9
        logger.info("LD A, I")


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
    def hlt(cpu, _, logger):
        logger.info("HALT")
        cpu.m_cycles, cpu.t_states = 1, 4
        cpu.halted = Bits.set()


    @staticmethod
    def portIn(cpu, _, logger):
        cpu.A = cpu.io.read(cpu.C, cpu.B)

        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("IN A, (C)")

    @staticmethod
    def in_r_c(cpu, opcode, logger):
        reg = (opcode >> 3) & 7
        value = cpu.io.read(cpu.C, cpu.B)
        if reg != 6:  # reg 6 = (HL) slot, affects flags only
            cpu.regs[reg] = value
        cpu.SFlag = Bits.isNegative(value)
        cpu.ZFlag = Bits.isZero(value)
        cpu.HFlag = Bits.reset()
        cpu.NFlag = Bits.reset()
        cpu.PVFlag = Bits.set() if Bits.count(value) & 1 == 0 else Bits.reset()

        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("IN {}, (C)".format(IndexToReg.translate8Bit(reg)))

    @staticmethod
    def out_c_r(cpu, opcode, logger):
        reg = (opcode >> 3) & 7
        value = cpu.regs[reg] if reg != 6 else 0
        cpu.io[cpu.C] = value

        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("OUT (C), {}".format(IndexToReg.translate8Bit(reg)))


    @staticmethod
    def ini(cpu, _, logger):
        value = cpu.io.read(cpu.C, cpu.B)
        cpu.ram[cpu.HL] = value
        cpu.B = (cpu.B - 1) & 0xFF
        cpu.HL = (cpu.HL + 1) & 0xFFFF
        cpu.ZFlag = Bits.isZero(cpu.B)
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("INI")

    @staticmethod
    def inir(cpu, _, logger):
        while True:
            value = cpu.io.read(cpu.C, cpu.B)
            cpu.ram[cpu.HL] = value
            cpu.B = (cpu.B - 1) & 0xFF
            cpu.HL = (cpu.HL + 1) & 0xFFFF
            if cpu.B == 0:
                break
        cpu.ZFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("INIR")

    @staticmethod
    def ind(cpu, _, logger):
        value = cpu.io.read(cpu.C, cpu.B)
        cpu.ram[cpu.HL] = value
        cpu.B = (cpu.B - 1) & 0xFF
        cpu.HL = (cpu.HL - 1) & 0xFFFF
        cpu.ZFlag = Bits.isZero(cpu.B)
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("IND")

    @staticmethod
    def indr(cpu, _, logger):
        while True:
            value = cpu.io.read(cpu.C, cpu.B)
            cpu.ram[cpu.HL] = value
            cpu.B = (cpu.B - 1) & 0xFF
            cpu.HL = (cpu.HL - 1) & 0xFFFF
            if cpu.B == 0:
                break
        cpu.ZFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("INDR")

    @staticmethod
    def outi(cpu, _, logger):
        value = cpu.ram[cpu.HL]
        cpu.B = (cpu.B - 1) & 0xFF
        cpu.io[cpu.C] = value
        cpu.HL = (cpu.HL + 1) & 0xFFFF
        cpu.ZFlag = Bits.isZero(cpu.B)
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("OUTI")

    @staticmethod
    def otir(cpu, _, logger):
        while True:
            value = cpu.ram[cpu.HL]
            cpu.B = (cpu.B - 1) & 0xFF
            cpu.io[cpu.C] = value
            cpu.HL = (cpu.HL + 1) & 0xFFFF
            if cpu.B == 0:
                break
        cpu.ZFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("OTIR")

    @staticmethod
    def outd(cpu, _, logger):
        value = cpu.ram[cpu.HL]
        cpu.B = (cpu.B - 1) & 0xFF
        cpu.io[cpu.C] = value
        cpu.HL = (cpu.HL - 1) & 0xFFFF
        cpu.ZFlag = Bits.isZero(cpu.B)
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("OUTD")

    @staticmethod
    def otdr(cpu, _, logger):
        while True:
            value = cpu.ram[cpu.HL]
            cpu.B = (cpu.B - 1) & 0xFF
            cpu.io[cpu.C] = value
            cpu.HL = (cpu.HL - 1) & 0xFFFF
            if cpu.B == 0:
                break
        cpu.ZFlag = Bits.set()
        cpu.NFlag = Bits.set()
        cpu.m_cycles, cpu.t_states = 4, 16
        logger.info("OTDR")

    @staticmethod
    def in_a_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        cpu.A = cpu.io.read(n, cpu.A)

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("IN A, ({:02X}".format(n))

