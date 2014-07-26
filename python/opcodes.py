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
		cpu.regs[A] = cpu.regs[A] ^ cpu.regs[regInd]
		"""Flags"""
		cpu.flags[ZF] = True if cpu.regs[A] == 0 else False
		cpu.flags[CF] = False
		cpu.flags[NF] = False
		cpu.flags[HF] = False
		cpu.flags[SF] = True if cpu.regs[A] & 0x80 else False
		cpu.flags[PVF] = True if Bits.count(cpu.regs[A]) % 2 == 0 else False
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
