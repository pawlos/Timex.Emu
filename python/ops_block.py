# Z80 block opcodes

from utility import Bits, IndexToReg, IndexToFlag, Flags
from regs import XF, YF, HF, CF, PVF, SF


class OpsBlock(object):

    @staticmethod
    def ldd(cpu, _, logger):
        OpsBlock._ldd(cpu)

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
            OpsBlock._ldd(cpu)
            if cpu.BC == 0:
                break

        cpu.WZ = cpu.pc + 1
        cpu.m_cycles, cpu.t_states = 4 if isZero else 5, 16 if isZero else 21

        logger.info("LDDR")


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
        OpsBlock._ldi(cpu)

        cpu.m_cycles, cpu.t_states = 4, 16
        cpu.PVFlag = Bits.set() if cpu.BC != 0 else Bits.reset()
        logger.info("LDI")


    @staticmethod
    def ldir(cpu, _, logger):
        wasZero = cpu.BC == 0
        while True:
            OpsBlock._ldi(cpu)
            if cpu.BC == 0:
                break

        cpu.WZ = cpu.pc + 1
        cpu.m_cycles, cpu.t_states = 4 if wasZero else 5, 16 if wasZero else 21
        logger.info("LDIR")


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
        cpu.WZ = cpu.WZ - 1
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

