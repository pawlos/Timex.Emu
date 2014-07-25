from regs import *
from utility import Bits

class Opcodes(object):

	@staticmethod
	def disableInterrupts(cpu, opcode):
		"""DI"""
		cpu.iff = 0x00;		
		cpu.debug("DI")

	@staticmethod
	def xorA(cpu, opcode):
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
		cpu.debug("XOR A")

	@staticmethod
	def ld16(cpu, opcode):
		regInd = (opcode & 0x30) >> 4
		cpu.pc += 1
		loValue = cpu.rom.readMemory(cpu.pc)
		cpu.pc += 1
		hiValue = cpu.rom.readMemory(cpu.pc)
		cpu._16bitRegs[regInd] = (hiValue << 8) + loValue
		cpu.debug("LD");

	@staticmethod
	def ld8(cpu, opcode):
		regIndPrim = (opcode & 7)
		cpu.debug(regIndPrim)
		regInd     = (opcode >> 3) & 7
		cpu.debug(regInd)
		cpu.regs[regInd] = cpu.regs[regIndPrim]
		cpu.debug("LD")

	@staticmethod
	def ld8n(cpu, opcode):
		regInd = (opcode >> 3) & 7
		cpu.pc += 1
		value = cpu.rom.readMemory(cpu.pc)
		cpu.regs[regInd] = value
		cpu.debug("LD")

	@staticmethod
	def jp(cpu, opcode):
		cpu.pc += 1
		loValue = cpu.rom.readMemory(cpu.pc)
		cpu.pc += 1
		hiValue = cpu.rom.readMemory(cpu.pc)
		cpu.pc = (hiValue << 8) + loValue
		cpu.debug("JP {0:x}".format(cpu.pc))
		return True

	@staticmethod
	def out(cpu, opcode):
		cpu.pc += 1
		value = cpu.rom.readMemory(cpu.pc)
		cpu.debug("OUT")
		cpu.ports[value] = cpu.A

	@staticmethod
	def ldExt(cpu, opcode):
		cpu.debug(cpu.A)
		cpu.I = cpu.A
		cpu.debug("LD I,A")

	@staticmethod
	def nop(cpu, opcode):
		cpu.debug("DEFB")
