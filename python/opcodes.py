# Aux class
from regs import *
from utility import Bits

class Opcodes(object):

	@staticmethod
	def disableInterrupts(cpu, opcode, logger):
		"""DI"""
		cpu.iff = 0x00;		
		logger.info("DI")

	@staticmethod
	def xorA(cpu, opcode, logger):
		"""XOR A"""
		regInd = opcode & 7
		cpu.A = cpu.A ^ cpu.regs[regInd]
		"""Flags"""
		cpu.flags[ZF] = Bits.isZero(cpu.A)
		cpu.flags[CF] = False
		cpu.flags[NF] = False
		cpu.flags[HF] = False
		cpu.flags[SF] = Bits.signInTwosComp(cpu.A)
		cpu.flags[PVF] = Bits.paritySet(cpu.A)
		logger.info("XOR A")

	@staticmethod
	def ld16(cpu, opcode, logger):
		regInd = (opcode & 0x30) >> 4
		loValue = cpu.rom.readMemory(cpu.PC)
		hiValue = cpu.rom.readMemory(cpu.PC)
		value = (hiValue << 8) + loValue

		if regInd == 0:
			cpu.BC = value
		elif regInd == 1:
			cpu.DE = value
		elif regInd == 2:
			cpu.HL = value
		elif regInd == 3:
			cpu.SP = value

		logger.info("LD");

	@staticmethod
	def ld8(cpu, opcode, logger):
		regIndPrim = (opcode & 7)
		logger.info(regIndPrim)
		regInd     = (opcode >> 3) & 7
		logger.info(regInd)
		cpu.regs[regInd] = cpu.regs[regIndPrim]
		logger.info("LD")

	@staticmethod
	def ld8n(cpu, opcode, logger):
		regInd = (opcode >> 3) & 7
		value = cpu.rom.readMemory(cpu.PC)
		cpu.regs[regInd] = value
		logger.info("LD")

	@staticmethod
	def jp(cpu, opcode, logger):
		loValue = cpu.rom.readMemory(cpu.PC)
		hiValue = cpu.rom.readMemory(cpu.PC)
		value = (hiValue << 8) + loValue
		cpu.PC = value

		logger.info("JP {0:x}".format(value))
		return True

	@staticmethod
	def out(cpu, opcode, logger):
		value = cpu.rom.readMemory(cpu.PC)
		logger.info("OUT")
		cpu.ports[value] = cpu.A

	@staticmethod
	def ldExt(cpu, opcode, logger):
		logger.info(cpu.A)
		cpu.I = cpu.A
		logger.info("LD I,A")

	@staticmethod
	def nop(cpu, opcode, logger):
		logger.info("DEFB")

	@staticmethod
	def ld_addr(cpu, opcode, logger):
		logger.info("LD (HL), n")
		value = cpu.rom.readMemory(cpu.PC)
		cpu.ram.storeAddr(cpu.HL, value)

	@staticmethod
	def dec16b(cpu, opcode, logger):
		regInd = (opcode >> 4) & 2
		logger.info(regInd)
		value = 0
		if regInd == 0:
			cpu.BC = cpu.BC - 1
		elif regInd == 1:
			cpu.DE = cpu.DE - 1
		elif regInd == 2:
			cpu.HL = cpu.HL - 1
		elif regInd == 3:
			cpu.SP = cpu.SP - 1

		logger.info("DEC (rr)")

	@staticmethod
	def cp(cpu, opcode, logger):
		regInd = opcode & 7
		logger.info(regInd)
		value = cpu.A - cpu.regs[regInd]
		"""Flags"""
		cpu.flags[ZF] = Bits.isZero(value)
		cpu.flags[CF] = Bits.carryFlag(value)
		cpu.flags[NF] = True
		cpu.flags[HF] = Bits.halfCarrySub(cpu.A, value)
		cpu.flags[SF] = Bits.signFlag(value)
		cpu.flags[PVF] = Bits.overflow(cpu.A, value)
		logger.info("CP r")

	@staticmethod
	def jpnz(cpu, opcode, logger):
		jumpOffset = cpu.rom.readMemory(cpu.PC)
		if cpu.ZFlag:
			return

		cpu.PC = cpu.PC + Bits.twos_comp(jumpOffset)
		logger.info("JPNZ {0:x}".format(jumpOffset))

	@staticmethod
	def jpnc(cpu, opcode, logger):
		jumpOffset = Bits.twos_comp(cpu.rom.readMemory(cpu.PC)) - 2
		if cpu.CFlag:
			return

		cpu.PC = cpu.PC + jumpOffset
		logger.info("JP NC {0:x}".format(jumpOffset))

	@staticmethod
	def _and(cpu, opcode, logger):
		logger.info("AND A")
		regInd = opcode & 7
		cpu.A = cpu.A & cpu.regs[regInd]
		cpu.flags[HF] = True
		cpu.flags[CF] = False
		cpu.flags[NF] = False
		cpu.flags[ZF] = Bits.isZero(cpu.A)
		cpu.flags[SF] = Bits.signInTwosComp(cpu.A)
		cpu.flags[PVF] = Bits.paritySet(cpu.A)

	@staticmethod
	def sbc(cpu, opcode, logger):
		logger.info("SBC HL")
		regInd = (opcode & 0x30) >> 4
		value = 0
		if regInd == 0:
			value = cpu.BC
		elif regInd == 1:
			value = cpu.DE
		elif regInd == 2:
			value = cpu.HL
		elif regInd == 3:
			value = cpu.SP

		oldHL = cpu.HL
		logger.info("Old value of HL: " + str(oldHL))
		cpu.HL = cpu.HL - value - (1 if cpu.CFlag else 0)
		logger.info("New value of HL: " + str(cpu.HL))

		cpu.flags[SF] = Bits.signFlag(cpu.HL, bits=16)
		cpu.flags[ZF] = Bits.isZero(cpu.HL)
		cpu.flags[HF] = Bits.halfCarrySub16(oldHL, cpu.HL)
		cpu.flags[PVF] = Bits.overflow(Bits.twos_comp(oldHL, bits=16), 
									   Bits.twos_comp(cpu.HL, bits=16))
		cpu.flags[NF] = True
		cpu.flags[CF] = Bits.borrow(cpu.HL, bits=16)

	@staticmethod
	def add16(cpu, opcode, logger):
		logger.info("ADD HL, rr")
		regInd = (opcode & 0x30) >> 4
		value = 0
		if regInd == 0:
			value = cpu.BC
		elif regInd == 1:
			value = cpu.DE
		elif regInd == 2:
			value = cpu.HL
		elif regInd == 3:
			value = cpu.SP

		oldHL = cpu.HL
		cpu.HL = cpu.HL + value

		cpu.flags[NF] = False
		cpu.flags[CF] = Bits.carryFlag16(oldHL, cpu.HL)
		cpu.flags[HF] = Bits.carryFlag16(oldHL, cpu.HL, bits=11)

	@staticmethod
	def inc16(cpu, opcode, logger):
		logger.info("INC rr")
		regInd = (opcode & 0x30) >> 4

		if regInd == 0:
			cpu.BC = cpu.BC + 1
		elif regInd == 1:
			cpu.DE = cpu.DE + 1
		elif regInd == 2:
			cpu.HL = cpu.HL + 1
		elif regInd == 3:
			cpu.SP = cpu.SP + 1

	@staticmethod
	def jrz(cpu, opcode, logger):

		jumpOffset = Bits.twos_comp(cpu.rom.readMemory(cpu.PC))
		if cpu.ZFlag == False:
			return

		cpu.PC = cpu.PC + jumpOffset
		logger.info("JR Z {0:x}".format(jumpOffset))

	@staticmethod
	def exx(cpu, opcode, logger):
		logger.info("EXX")
		
		tempBC = cpu.BC
		tempDE = cpu.DE
		tempHL = cpu.HL
		
		cpu.BC = cpu.BCPrim
		cpu.DE = cpu.DEPrim
		cpu.HL = cpu.HLPrim

		cpu.BCPrim = tempBC
		cpu.DEPrim = tempDE
		cpu.HLPrim = tempHL

	@staticmethod
	def ldNnRr(cpu, opcode, logger):
		logger.info("LD (nn),rr")
		value = 0
		regInd = (opcode & 0x30) >> 4
		nn = cpu.rom.readMemory(cpu.PC) << 8 + cpu.rom.readMemory(cpu.PC)
		logger.info("Addr: {0:x}".format(nn))
		if regInd == 0:
			value = cpu.BC
		elif regInd == 1:
			value = cpu.DE
		elif regInd == 2:
			value = cpu.HL
		elif regInd == 3:
			value = cpu.SP

		cpu.ram.storeAddr(nn, value >> 8)
		cpu.ram.storeAddr(nn+1, value & 0xFF)