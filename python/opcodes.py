# Aux class
from regs import *
from utility import Bits
from utility import IndexToReg

class Opcodes(object):

	@staticmethod
	def disableInterrupts(cpu, opcode, logger):
		"""DI"""
		cpu.iff = 0x00
		logger.info("DI")

	@staticmethod
	def enableInterrupts(cpu, opcode, logger):
		''' EI '''
		cpu.iff = 0x01
		logger.info("EI")

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

		logger.info("LD {}, 0x{:04X}".format(IndexToReg.translate16bit(regInd),value))

	@staticmethod
	def ld8(cpu, opcode, logger):
		regIndPrim = (opcode & 7)
		logger.info(regIndPrim)
		regInd     = (opcode >> 3) & 7
		cpu.regs[regInd] = cpu.regs[regIndPrim]
		logger.info("LD {}, {}'".format(IndexToReg.translate8bit(regInd), IndexToReg.translate8bit(regIndPrim)))

	@staticmethod
	def ld8n(cpu, opcode, logger):
		regInd = (opcode >> 3) & 7
		value = cpu.rom.readMemory(cpu.PC)
		cpu.regs[regInd] = value
		logger.info("LD {}, {:2X}".format(IndexToReg.translate8bit(IndexToReg), value))

	@staticmethod
	def jp(cpu, opcode, logger):
		loValue = cpu.rom.readMemory(cpu.PC)
		hiValue = cpu.rom.readMemory(cpu.PC)
		value = (hiValue << 8) + loValue
		cpu.PC = value

		logger.info("JP {0:X}".format(value))
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
		value = cpu.rom.readMemory(cpu.PC)
		cpu.ram.storeAddr(cpu.HL, value)
		logger.info("LD (HL), {:02X}".format(value))

	@staticmethod
	def dec16b(cpu, opcode, logger):
		regInd = (opcode >> 4) & 2
		#logger.info(regInd)
		value = 0
		if regInd == 0:
			cpu.BC = cpu.BC - 1
		elif regInd == 1:
			cpu.DE = cpu.DE - 1
		elif regInd == 2:
			cpu.HL = cpu.HL - 1
		elif regInd == 3:
			cpu.SP = cpu.SP - 1

		logger.info("DEC {}".format(IndexToReg.translate16bit(regInd)))

	@staticmethod
	def cp(cpu, opcode, logger):
		regInd = opcode & 7
		#logger.info(regInd)
		value = cpu.A - cpu.regs[regInd]
		"""Flags"""
		cpu.flags[ZF] = Bits.isZero(value)
		cpu.flags[CF] = Bits.carryFlag(value)
		cpu.flags[NF] = Bits.set()
		cpu.flags[HF] = Bits.halfCarrySub(cpu.A, value)
		cpu.flags[SF] = Bits.signFlag(value)
		cpu.flags[PVF] = Bits.overflow(cpu.A, value)
		logger.info("CP {}".format(IndexToReg.translate8bit(regInd)))

	@staticmethod
	def jpnz(cpu, opcode, logger):
		jumpOffset = cpu.rom.readMemory(cpu.PC)
		if cpu.ZFlag:
			return

		cpu.PC = cpu.PC + Bits.twos_comp(jumpOffset)
		logger.info("JPNZ 0x{0:04X}".format(jumpOffset))

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
		#logger.info("Old value of HL: " + str(oldHL))
		cpu.HL = cpu.HL - value - (1 if cpu.CFlag else 0)
		#logger.info("New value of HL: " + str(cpu.HL))

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
		
		regInd = (opcode & 0x30) >> 4
		logger.info("INC {0}".format(IndexToReg.translate16bit(regInd)))
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
		value = 0
		regInd = (opcode & 0x30) >> 4
		high = cpu.rom.readMemory(cpu.PC)
		low = cpu.rom.readMemory(cpu.PC)
		nn =  (high << 8) + low
		logger.info("Addr: 0x{0:x}".format(nn))
		if regInd == 0:
			value = cpu.BC
		elif regInd == 1:
			value = cpu.DE
		elif regInd == 2:
			value = cpu.HL
		elif regInd == 3:
			value = cpu.SP

		cpu.ram.storeAddr(nn + 1, value >> 8)
		cpu.ram.storeAddr(nn, value & 0xFF)
		logger.info("LD ({:04X}),{}".format(nn, IndexToReg.translate16bit(regInd)))

	@staticmethod
	def ldNnHl(cpu, opcode, logger):
		high = cpu.rom.readMemory(cpu.PC)
		low = cpu.rom.readMemory(cpu.PC)

		nn = (high << 8) + low
		logger.info("LD (0x{:04x}), HL".format(nn))
		cpu.ram.storeAddr(nn+1, cpu.H)
		cpu.ram.storeAddr(nn, cpu.L)

	@staticmethod
	def inc8(cpu, opcode, logger):
		index = ( opcode >> 3 ) & 7
		oldValue =  cpu.regs[index]
		cpu.regs[index] = (cpu.regs[index] + 1 ) & 0xFF

		cpu.NFlag = Bits.reset()
		cpu.ZFlag = Bits.isZero(cpu.regs[index])
		cpu.HFlag = Bits.halfCarrySub(oldValue, cpu.regs[index])
		cpu.PVFlag = True if oldValue == 0x7f else False
		cpu.SFlag = Bits.twos_comp(cpu.regs[index]) < 0
		logger.info("INC {}".format(IndexToReg.translate8bit(index)))

	@staticmethod
	def ex_de_hl(cpu, opcode, logger):
		logger.info("EX DE, HL")
		oldValue = cpu.DE
		cpu.DE = cpu.HL
		cpu.HL = oldValue

	@staticmethod
	def lddr(cpu, opcode, logger):
		logger.info("LDDR")
		while True:
			cpu.ram.storeAddr(cpu.DE, cpu.ram.readAddr(cpu.HL))
			cpu.HL = cpu.HL - 1
			cpu.DE = cpu.DE - 1
			cpu.BC = cpu.BC - 1
			cpu.NFlag = False
			cpu.HFlag = False
			cpu.PVFlag = False
			if cpu.BC == 0:
				break

	@staticmethod
	def ldHl_addr(cpu, opcode, logger):
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		addr = (high << 8) + low
		logger.info("LD HL, (0x{:04X})".format(addr))
		cpu.L = cpu.ram.readAddr(addr)
		cpu.H = cpu.ram.readAddr(addr+1)

	@staticmethod
	def ld_sp_hl(cpu, opcode, logger):
		logger.info("LD SP, HL")
		cpu.SP = cpu.HL

	@staticmethod
	def im1(cpu, opcode, logger):
		cpu.interruptMode = 1
		logger.info("IM 1")

	@staticmethod
	def ldiy(cpu, opcode, logger):
		''' Executes LD IY, nn opcode'''
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		imm = (high << 8) + low
		logger.info("LD IY, 0x{:4X}".format(imm))
		cpu.IY = imm

	@staticmethod
	def ldir(cpu, opcode, logger):
		logger.info("LDIR")
		''' (DE) <- (HL), DE = DE + 1, HL = HL + 1, BC F = BC - 1'''
		while True:
			hl_mem = cpu.ram.readAddr(cpu.HL)
			cpu.ram.storeAddr(cpu.DE, hl_mem)
			cpu.HL = cpu.HL + 1
			cpu.DE = cpu.DE + 1
			cpu.BC = cpu.BC - 1
			if cpu.BC == 0:
				break
		cpu.NFlag = Bits.reset()
		cpu.HFlag = Bits.reset()
		cpu.PVFlag = Bits.reset()

	@staticmethod
	def ldnn_a(cpu, opcode, logger):
		''' LD (nn),A '''
		high = cpu.rom.readMemory(cpu.PC)
		low = cpu.rom.readMemory(cpu.PC)
		addr = (high << 8) + low
		logger.info("LD (0x{:4X}), A".format(addr))
		cpu.ram.storeAddr(addr, cpu.A)

	@staticmethod
	def dec_mem_at_iy(cpu, opcode, logger):
		''' DEC (IY+d) '''
		displacement = cpu.rom.readMemory(cpu.PC)
		logger.info("DEC (IY+{:2X})".format(displacement))
		addr = cpu.IY + displacement
		value = cpu.ram.readAddr(addr)
		new_value = value - 1
		cpu.ram.storeAddr(addr, new_value)

		cpu.NFlag = Bits.set()
		cpu.SFlag = Bits.isNegative(new_value)
		cpu.ZFlag = Bits.isZero(new_value)
		cpu.PVFlag = True if value == 0x80 else False
		cpu.HFlag = Bits.halfCarrySub16(value, new_value)