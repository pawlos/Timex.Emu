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
        if value == 0xFE and cpu.display:
            cpu.display.set_border(cpu.A & 0x07)
            cpu.display.set_speaker((cpu.A >> 4) & 1, cpu.tstates)
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
        if cpu.C == 0xFE and cpu.display:
            cpu.A = cpu.display.read_keyboard(cpu.B)
        elif cpu.C == 0x1F and cpu.display:
            cpu.A = cpu.display.read_kempston()
        else:
            cpu.A = cpu.io[cpu.C]

        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("IN A, (C)")


    @staticmethod
    def in_a_n(cpu, _, logger):
        n = cpu.ram[cpu.PC]
        if n == 0xFE and cpu.display:
            cpu.A = cpu.display.read_keyboard(cpu.A)
        elif n == 0x1F and cpu.display:
            cpu.A = cpu.display.read_kempston()
        else:
            cpu.A = cpu.io[n]

        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("IN A, ({:02X}".format(n))

