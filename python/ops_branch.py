# Z80 branch opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsBranch(object):

    @staticmethod
    def jp(cpu, _, logger):
        cpu.Z = cpu.ram[cpu.PC]
        cpu.W = cpu.ram[cpu.PC]

        cpu.PC = cpu.WZ
        cpu.m_cycles, cpu.t_states = 3, 10
        logger.info("JP {0:04X}".format(cpu.WZ))


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
        jumpOffset = Bits.from_twos_comp(cpu.ram[pc])

        no_jump = cpu.CFlag

        if not no_jump:
            cpu.PC = pc + jumpOffset+1
            cpu.m_cycles, cpu.t_states = 3, 12
        else:
            cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR NC, {0:04X}".format(pc+jumpOffset+1))


    @staticmethod
    def jr_z(cpu, _, logger):
        pc = cpu.PC
        jumpTo = pc + Bits.from_twos_comp(cpu.ram[pc]) + 1

        no_jump = cpu.ZFlag is False

        if not no_jump:
            cpu.PC = jumpTo
            cpu.m_cycles, cpu.t_states = 3, 12
        else:
            cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR Z, {:04X}".format(jumpTo))


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

        cpu.m_cycles, cpu.t_states = 4, 14
        cpu.iff1 = cpu.iff2
        logger.info("RETN")


    @staticmethod
    def rst(cpu, opcode, logger):
        index = (opcode >> 3) & 7
        pc = cpu.PC
        cpu.ram[cpu.SP - 1] = pc >> 8
        cpu.ram[cpu.SP - 2] = pc & 0xFF
        cpu.SP -= 2

        cpu.WZ = cpu.rst_jumps[index]
        cpu.PC = cpu.WZ
        cpu.m_cycles, cpu.t_states = 3, 11
        logger.info("RST {:02X}".format(cpu.rst_jumps[index]))


    @staticmethod
    def jr_e(cpu, _, logger):
        pc = cpu.PC
        jumpOffset = Bits.from_twos_comp(cpu.ram[pc])

        cpu.PC = pc + jumpOffset + 1
        cpu.m_cycles, cpu.t_states = 3, 12
        logger.info("JR 0x{:02X}".format(cpu.ram[pc]))


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
    def jr_c(cpu, _, logger):
        pc = cpu.PC
        jumpOffset = Bits.from_twos_comp(cpu.ram[pc])
        no_jump = cpu.CFlag is False
        cpu.WZ = pc + jumpOffset + 1
        if not no_jump:
            cpu.PC = cpu.WZ
            cpu.m_cycles, cpu.t_states = 3, 12
        else:
            cpu.m_cycles, cpu.t_states = 2, 7
        logger.info("JR C, {0:04X}".format(cpu.WZ))


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

