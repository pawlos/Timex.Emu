# Aux class
from regs import *
from utility import Bits
from utility import IndexToReg

class Opcodes(object):

	@staticmethod
	def disableInterrupts(cpu, opcode, logger):
		"""DI"""
		cpu.iff1 = 0x00
		cpu.iff2
		logger.info("DI")

	@staticmethod
	def enableInterrupts(cpu, opcode, logger):
		''' EI '''
		cpu.iff1 = 0x01
		cpu.iff2 = 0x01
		logger.info("EI")

	@staticmethod
	def xorA(cpu, opcode, logger):
		"""XOR A"""
		regInd = opcode & 7
		cpu.A = cpu.A ^ cpu.regs[regInd]
		"""Flags"""
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.CFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		cpu.HFlag = Bits.reset()
		cpu.SFlag = Bits.signInTwosComp(cpu.A)
		cpu.PVFlag = Bits.paritySet(cpu.A)
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
		regInd     = (opcode >> 3) & 7
		cpu.regs[regInd] = cpu.regs[regIndPrim]
		logger.info("LD {}, {}".format(IndexToReg.translate8bit(regInd), IndexToReg.translate8bit(regIndPrim)))

	@staticmethod
	def ld8n(cpu, opcode, logger):
		regInd = (opcode >> 3) & 7
		value = cpu.rom.readMemory(cpu.PC)
		cpu.regs[regInd] = value
		logger.info("LD {}, {:2X}".format(IndexToReg.translate8bit(regInd), value))

	@staticmethod
	def jp(cpu, opcode, logger):
		loValue = cpu.rom.readMemory(cpu.PC)
		hiValue = cpu.rom.readMemory(cpu.PC)
		value = (hiValue << 8) + loValue
		cpu.PC = value

		logger.info("JP {0:X}".format(value))

	@staticmethod
	def out(cpu, opcode, logger):
		value = cpu.rom.readMemory(cpu.PC)
		logger.info("OUT {:04X}, A".format(value))
		cpu.ports[value] = cpu.A

	@staticmethod
	def ldExt(cpu, opcode, logger):
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
		regInd = (opcode >> 4) & 3
		
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
		cpu.ZFlag = Bits.isZero(value)
		cpu.CFlag = Bits.carryFlag(value)
		cpu.NFlag = Bits.set()
		cpu.HFlag = Bits.halfCarrySub(cpu.A, value)
		cpu.SFlag = Bits.signFlag(value)
		cpu.PVFlag = Bits.overflow(cpu.A, value)
		logger.info("CP {}".format(IndexToReg.translate8bit(regInd)))

	@staticmethod
	def jpnz(cpu, opcode, logger):
		jumpOffset = cpu.rom.readMemory(cpu.PC)
		logger.info("JPNZ {0:04X}".format(jumpOffset))
		if cpu.ZFlag:
			return

		cpu.PC = cpu.PC + Bits.twos_comp(jumpOffset)

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
		cpu.HFlag = Bits.set()
		cpu.CFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.SFlag = Bits.signInTwosComp(cpu.A)
		cpu.PVFlag = Bits.paritySet(cpu.A)

	@staticmethod
	def sbc(cpu, opcode, logger):
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

		cpu.HL = cpu.HL - value - (1 if cpu.CFlag else 0)

		logger.info("SBC HL, {}".format(IndexToReg.translate16bit(regInd)))
		cpu.SFlag = Bits.signFlag(cpu.HL, bits=16)
		cpu.ZFlag = Bits.isZero(cpu.HL)
		cpu.HFlag = Bits.halfCarrySub16(oldHL, cpu.HL)
		cpu.PVFlag = Bits.overflow(Bits.twos_comp(oldHL, bits=16), 
									   Bits.twos_comp(cpu.HL, bits=16))
		cpu.NFlag = Bits.set()
		cpu.CFlag = Bits.borrow(cpu.HL, bits=16)

	@staticmethod
	def add16(cpu, opcode, logger):
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

		logger.info("ADD HL, {}".format(IndexToReg.translate16bit(regInd)))
		oldHL = cpu.HL
		cpu.HL = cpu.HL + value

		cpu.NFlag = Bits.reset()
		cpu.CFlag = Bits.carryFlag16(oldHL, cpu.HL)
		cpu.HFlag = Bits.carryFlag16(oldHL, cpu.HL, bits=11)

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
		logger.info("JR Z {0:x}".format(jumpOffset))
		if cpu.ZFlag == False:
			return

		cpu.PC = cpu.PC + jumpOffset

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
		#logger.info("Addr: 0x{0:x}".format(nn))
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
			cpu.NFlag = Bits.reset()
			cpu.HFlag = Bits.reset()
			cpu.PVFlag = Bits.reset()
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
		cpu.HFlag = Bits.halfCarrySub(value, new_value)

	@staticmethod
	def bit_set(cpu, opcode, logger):
		index = (opcode >> 8) & 255
		logger.info("SET 1,(IY+{:02X})".format(index))
		val = cpu.ram.readAddr(cpu.IY+index)
		val |= (1 << 1)
		cpu.ram.storeAddr(cpu.IY+index, val)

	@staticmethod
	def bit_res(cpu, opcode, logger):
		index = (opcode >> 8) & 255
		bit = (opcode >> 3) & 7
		logger.info("RES {}, (IY+{:02X})".format(bit, index))
		val = cpu.ram.readAddr(cpu.IY+index)
		val &= (0 << bit)
		cpu.ram.storeAddr(cpu.IY+index, val)

	@staticmethod
	def bit_bit(cpu, opcode, logger):
		index = (opcode >> 8) & 255
		bit = (opcode >> 3) & 7
		cpu.ZFlag = cpu.ram.readAddr(cpu.IY+index) & (1 << bit) != 0
		cpu.HFlag = Bits.reset()
		logger.info("BIT {:02X}, (IY+{:02X})".format(bit, index))

	@staticmethod
	def call(cpu, opcode, logger):
		''' CALL '''
		pc = cpu.PC
		addr_lo = cpu.rom.readMemory(pc)
		pc += 1
		addr_hi = cpu.rom.readMemory(pc)
		addr = (addr_hi << 8) + addr_lo
		pc += 1
		cpu.ram.storeAddr(cpu.SP - 1, pc >> 8)
		cpu.ram.storeAddr(cpu.SP - 2, (pc & 255))
		cpu.SP = cpu.SP - 2
		cpu.PC = addr
		logger.info("CALL {:04X}".format(addr)) 

	@staticmethod
	def ldiy_d_r(cpu, opcode, logger):
		''' LD (IY+d),r '''
		regInd = opcode & 7
		d = cpu.rom.readMemory(cpu.PC)
		cpu.ram.storeAddr(cpu.IY + d, cpu.regs[regInd])
		logger.info("LD (IY+{:02X}),{}".format(d, IndexToReg.translate8bit(regInd)))

	@staticmethod
	def ldhlr(cpu, opcode, logger):
		regInd = opcode & 7
		cpu.ram.storeAddr(cpu.HL, cpu.regs[regInd])
		logger.info("LD (HL), {}".format(IndexToReg.translate8bit(regInd)))

	@staticmethod
	def djnz(cpu, opcode, logger):
		e = cpu.rom.readMemory(cpu.PC)
		cpu.B = cpu.B - 1
		if cpu.B != 0:
			cpu.PC = cpu.PC + Bits.twos_comp(e)

		logger.info("DJNZ {:04X}".format(e))

	@staticmethod
	def add_iy(cpu, opcode, logger):
		d = cpu.rom.readMemory(cpu.PC)
		value = cpu.A + cpu.ram.readAddr(cpu.IY+d)

		cpu.NFlag = Bits.reset()
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.CFlag = Bits.carryFlag(value)
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.PVFlag = Bits.overflow(cpu.A, value)
		cpu.HFlag = Bits.halfCarrySub(cpu.A, value)

		cpu.A = value

		logger.info("ADD A, (IY+{:02X})".format(d))

	@staticmethod
	def sub_n(cpu, opcode, logger):
		n = cpu.rom.readMemory(cpu.PC)
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
		index = (opcode >> 4) & 3
		reg = ""
		value = 0
		if index == 0:
			reg = "BC"
			value = cpu.BC
		elif index == 1:
			reg = "DE"
			value = cpu.DE
		elif index == 2:
			reg = "HL"
			value = cpu.HL
		else:
			reg = "AF"
			value = cpu.AF

		cpu.ram.storeAddr(cpu.SP-1, value >> 8)
		cpu.ram.storeAddr(cpu.SP-2, value & 255)
		cpu.SP -= 2
		logger.info("PUSH {}".format(reg))

	@staticmethod
	def sub_r(cpu, opcode, logger):
		index = opcode & 3

		old_A = cpu.A
		cpu.A = cpu.A - cpu.regs[index]

		cpu.NFlag = Bits.set()
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.HFlag = Bits.halfCarrySub(old_A, cpu.A)
		cpu.PVFlag = Bits.overflow(old_A, cpu.A)
		cpu.CFlag = Bits.carryFlag(cpu.A)

		logger.info("SUB {}".format(IndexToReg.translate8bit(index)))

	@staticmethod
	def rrca(cpu, opcode, logger):
		cflag = cpu.A & 1
		cpu.A = (cpu.A >> 1) | (cflag << 7)
		cpu.CFlag = True if cflag != 0 else False
		cpu.HFlag = Bits.reset()
		cpu.NFlag = Bits.reset()

		logger.info("RRCA")

	@staticmethod
	def and_n(cpu, opcode, logger):
		n = cpu.rom.readMemory(cpu.PC)
		old = cpu.A
		cpu.A = cpu.A & n

		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.HFlag = Bits.set()
		cpu.PVFlag = Bits.overflow(old, cpu.A)
		cpu.NFlag = Bits.reset()
		cpu.CFlag = Bits.reset()

		logger.info("AND {:02X}".format(n))

	@staticmethod
	def or_n(cpu, opcode, logger):
		n = cpu.rom.readMemory(cpu.PC)
		old = cpu.A
		cpu.A = cpu.A | n

		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.HFlag = Bits.reset()
		cpu.PVFlag = Bits.overflow(old, cpu.A)
		cpu.NFlag = Bits.reset()
		cpu.CFlag = Bits.reset()

		logger.info("OR {:02X}".format(n))

	@staticmethod
	def ret(cpu, opcode, logger):
		low = cpu.ram.readAddr(cpu.SP)
		high = cpu.ram.readAddr(cpu.SP+1)
		addr = (high << 8) + low
		cpu.SP += 2
		cpu.PC = addr
		logger.info("RET")

	@staticmethod
	def rst(cpu, opcode, logger):
		index = (opcode >> 3) & 7
		pc = cpu.PC
		cpu.ram.storeAddr(cpu.SP - 1, pc >> 8)
		cpu.ram.storeAddr(cpu.SP - 2, pc & 8)
		cpu.SP -= 2
		rst_jumps = {0:0x00, 1:0x08, 2:0x10, 3:0x18, 4:0x20, 5:0x28, 6:0x30, 7:0x38}

		cpu.PC = rst_jumps[index]
		logger.info("RST {:02X}".format(rst_jumps[index]))

	@staticmethod
	def pop(cpu, opcode, logger):
		index = (opcode >> 4) & 3
		high = cpu.ram.readAddr(cpu.SP+1)
		low = cpu.ram.readAddr(cpu.SP)
		cpu.SP += 2
		val = (high << 8) + low
		reg = ""
		if index == 0:
			cpu.BC = val
			reg = "BC"
		elif index == 1:
			cpu.DE = val
			reg = "DE"
		elif index == 2:
			cpu.HL = val
			reg = "HL"
		elif index == 3:
			cpu.AF = val
			reg = "AF"

		logger.info("POP {}".format(reg))

	@staticmethod
	def ldiy_d_n(cpu, opcode, logger):
		''' LD (IY+d),n '''
		d = cpu.rom.readMemory(cpu.PC)
		n = cpu.rom.readMemory(cpu.PC)
		cpu.ram.storeAddr(cpu.IY + d, n)
		logger.info("LD (IY+{:02X}),{:02X}".format(d, n))

	@staticmethod
	def add_r(cpu, opcode, logger):
		''' ADD A,r '''
		index = (opcode & 7)
		old = cpu.A
		cpu.A = old + cpu.regs[index]
		logger.info("ADD A,{}".format(IndexToReg.translate8bit(index)))

		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.HFlag = Bits.halfCarrySub(old, cpu.A)
		cpu.PVFlag = Bits.overflow(old, cpu.A)
		cpu.NFlag = Bits.reset()
		cpu.CFlag = Bits.carryFlag(cpu.A)

	@staticmethod
	def add_r_n(cpu, opcode, logger):
		''' ADD A,n '''
		n = cpu.rom.readMemory(cpu.PC)
		old = cpu.A

		value = cpu.A + n
		cpu.A = value

		cpu.SFlag = Bits.isNegative(value)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.HFlag = Bits.halfCarrySub(old, cpu.A)
		cpu.PVFlag = Bits.overflow(old, cpu.A)
		cpu.NFlag = Bits.reset()
		cpu.CFlag = Bits.carryFlag(value)

		logger.info("ADD A, {:02X}".format(n))

	@staticmethod
	def ld_r_hl(cpu, opcode, logger):
		''' LD r, (HL) '''

		index = (opcode >> 3) & 7

		value = cpu.ram.readAddr(cpu.HL)
		old = cpu.regs[index]

		cpu.regs[index] = value

		logger.info("LD {},(HL)".format(IndexToReg.translate8bit(index)))

	@staticmethod
	def _or(cpu, opcode, logger):
		''' OR r '''
		regInd = opcode & 7
		cpu.A = cpu.A | cpu.regs[regInd]
		cpu.HFlag = Bits.reset()
		cpu.CFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.PVFlag = Bits.paritySet(cpu.A)
		logger.info("OR {}".format(IndexToReg.translate8bit(regInd)))

	@staticmethod
	def jr_e(cpu, opcode, logger):

		jumpOffset = Bits.twos_comp(cpu.rom.readMemory(cpu.PC))
		logger.info("JR {0:x}".format(jumpOffset))

		cpu.PC = cpu.PC + jumpOffset

	@staticmethod
	def ld16_nn(cpu, opcode, logger):
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		addr = ( high << 8 ) + low
		value = cpu.ram.readAddr(addr)
		reg = ( opcode >> 4 ) & 3

		if reg == 0:
			cpu.BC = value
		elif reg == 1:
			cpu.DE = value
		elif reg == 2:
			cpu.HL = value
		else:
			cpu.SP = value 

		logger.info("LD {},({:0X})".format(IndexToReg.translate16bit(reg), addr))

	@staticmethod
	def ld_a_bc(cpu, opcode, logger):
		value = cpu.ram.readAddr(cpu.BC)
		cpu.A = value
		logger.info("LD A, (BC)")

	@staticmethod
	def ld_a_de(cpu, opcode, logger):
		value = cpu.ram.readAddr(cpu.DE)
		cpu.A = value
		logger.info("LD A, (DE)")

	@staticmethod
	def ld_a_nn(cpu, opcode, logger):
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		addr = (high << 8) + low
		cpu.A = cpu.ram.readAddr(addr)
		logger.info("LD A, ({:04X})".format(addr))

	@staticmethod
	def ld_bc_a(cpu, opcode, logger):
		cpu.ram.storeAddr(cpu.BC, cpu.A)
		logger.info("LD (BC), A")

	@staticmethod
	def ld_de_a(cpu, opcode, logger):
		cpu.ram.storeAddr(cpu.DE, cpu.A)
		logger.info("LD (DE), A")

	@staticmethod
	def lra(cpu, opcode, logger):
		cflag = (cpu.A >> 7) & 1
		cpu.A = Bits.setNthBit((cpu.A << 1), 0, cpu.CFlag)
		cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
		logger.info("LRA")

	@staticmethod
	def rra(cpu, opcode, logger):
		cflag = (cpu.A & 1)
		cpu.A = Bits.setNthBit((cpu.A >> 1), 7, cpu.CFlag)
		cpu.CFlag = Bits.set() if cflag == 1 else Bits.reset()
		cpu.HFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		logger.info("RRA")

	@staticmethod
	def rld(cpu, opcode, logger):
		low_a = cpu.A & 0x0F
		mem_hl = cpu.ram.readAddr(cpu.HL)
		low_hl = mem_hl & 0x0F
		high_hl = (mem_hl & 0xF0) >> 4
		cpu.A = ((cpu.A & 0xF0) | high_hl)
		mem_hl = (mem_hl << 4) | low_a
		cpu.ram.storeAddr(cpu.HL, mem_hl)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.HFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		cpu.PVFlag = Bits.paritySet(cpu.A)
		logger.info("RLD")

	@staticmethod
	def rrd(cpu, opcode, logger):
		low_a = cpu.A & 0x0F
		mem_hl = cpu.ram.readAddr(cpu.HL)
		low_hl = mem_hl & 0x0F
		high_hl = (mem_hl & 0xF0) >> 4
		cpu.A = (cpu.A & 0xF0) | low_hl
		mem_hl = (low_a << 4) | high_hl
		cpu.ram.storeAddr(cpu.HL, mem_hl)
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.HFlag = Bits.reset()
		cpu.NFlag = Bits.reset()
		cpu.PVFlag = Bits.paritySet(cpu.A)
		logger.info("RRD")

	@staticmethod
	def neg(cpu, opcode, logger):
		old = cpu.A
		cpu.A = 0 - cpu.A
		cpu.NFlag = Bits.reset()
		cpu.ZFlag = Bits.isZero(cpu.A)
		cpu.SFlag = Bits.isNegative(cpu.A)
		cpu.PVFlag = old == 0x80	
		cpu.CFlag = Bits.isZero(old)
		cpu.HFlag = Bits.halfCarrySub(0x0, old)
		logger.info("NEG")

	@staticmethod
	def ld_r_iy_d(cpu, opcode, logger):
		index = (opcode >> 3 ) & 7
		d = cpu.rom.readMemory(cpu.PC)
		cpu.regs[index] = cpu.ram.readAddr(cpu.IY + d)
		logger.info("LD {}, (IY+{:02X})".format(IndexToReg.translate8bit(index), d))

	@staticmethod
	def ld_ix_nn(cpu, opcode, logger):
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		addr = (high << 8) + low
		low_val = cpu.ram.readAddr(addr)
		high_val = cpu.ram.readAddr(addr+1)
		cpu.IX = (high_val << 8) + low_val
		logger.info("LD IX, ({:04X})".format(addr))

	@staticmethod
	def ldra(cpu, opcode, logger):
		cpu.R = cpu.A
		logger.info("LD R, A")

	@staticmethod
	def ldar(cpu, opcode, logger):
		cpu.A = cpu.R

		cpu.SFlag = Bits.isNegative(cpu.R)
		cpu.ZFlag = Bits.isZero(cpu.R)
		cpu.HFlag = Bits.reset()
		cpu.PVFlag = cpu.iff2
		cpu.NFlag = Bits.reset()
		logger.info("LD A, R")

	@staticmethod
	def im2(cpu, opcode, logger):
		cpu.interruptMode = 2
		logger.info("IM 2")

	@staticmethod
	def im0(cpu, opcode, logger):
		cpu.interruptMode = 0
		logger.info("IM 0")

	@staticmethod
	def pop_ix(cpu, opcode, logger):
		low = cpu.ram.readAddr(cpu.SP)
		cpu.SP = cpu.SP + 1
		high = cpu.ram.readAddr(cpu.SP)
		cpu.SP = cpu.SP + 1
		cpu.IX = (high << 8) + low
		logger.info("POP IX")

	@staticmethod
	def jp_cond(cpu, opcode, logger):
		cond = (opcode >> 3) & 7
		low = cpu.rom.readMemory(cpu.PC)
		high = cpu.rom.readMemory(cpu.PC)
		addr = (high << 8) + low

		taken = False
		flag = ""
		if cond == 0:
			flag = "NZ"
		if cond == 1:
			flag == "Z"
		if cond == 2:
			flag = "NC"
		if cond == 3:
			flag = "C"
		if cond == 4:
			flag = "NPV"
		if cond == 5:
			flag = "PV"
		if cond == 6:
			flag = "NS"
		if cond == 7:
			flag = "S"
		if cond == 0 and cpu.ZFlag == False:
			taken = True
		if cond == 1 and cpu.ZFlag:
			taken = True
		if cond == 2 and cpu.CFlag == False:
			taken = True
		if cond == 3 and cpu.CFlag:
			taken = True
		if cond == 4 and cpu.PVFlag == False:
			taken = True
		if cond == 5 and cpu.PVFlag:
			taken = True
		if cond == 6 and cpu.SFlag == False:
			taken = True
		if cond == 7 and cpu.SFlag:
			taken = True

		if taken:
			cpu.PC = addr

		logger.info("JP {} {:04X}".format(flag, addr))

	@staticmethod
	def call_cond(cpu, opcode, logger):
		cond = (opcode >> 3) & 7
		pc = cpu.PC
		addr_lo = cpu.rom.readMemory(pc)
		pc += 1
		addr_hi = cpu.rom.readMemory(pc)
		addr = (addr_hi << 8) + addr_lo
		pc += 1

		taken = False
		flag = ""

		if cond == 0:
			flag == "NZ"
		elif cond == 1:
			flag == "Z"
		elif cond == 2:
			flag = "NC"
		elif cond == 3:
			flag = "C"
		elif cond == 4:
			flag = "NPV"
		elif cond == 5:
			flag = "PV"
		elif cond == 6:
			flag = "NS"
		elif cond == 7:
			flag = "S"

		if cond == 0 and cpu.ZFlag == False:
			taken = True
		elif cond == 1 and cpu.ZFlag:
			taken = True
		elif cond == 2 and cpu.CFlag == False:
			taken = True
		elif cond == 3 and cpu.CFlag:
			taken = True
		elif cond == 4 and cpu.PVFlag == False:
			taken = True
		elif cond == 5 and cpu.PVFlag:
			taken = True
		elif cond == 6 and cpu.SFlag == False:
			taken = True
		elif cond == 7 and cpu.SFlag:
			taken = True

		if taken:
			cpu.ram.storeAddr(cpu.SP - 1, pc >> 8)
			cpu.ram.storeAddr(cpu.SP - 2, (pc & 255))
			cpu.SP = cpu.SP - 2
			cpu.PC = addr


		logger.info("CALL {}, {:04X}".format(flag, addr))

	@staticmethod
	def dec8b(cpu, opcode, logger):
		reg_index = (opcode >> 7) & 7
		cpu.regs[reg_index] = cpu.regs[reg_index] - 1

		cpu.ZFlag = Bits.isZero(cpu.regs[reg_index])
		cpu.SFlag = Bits.isNegative(cpu.regs[reg_index])
		logger.info("DEC {}".format(IndexToReg.translate8bit(reg_index)))