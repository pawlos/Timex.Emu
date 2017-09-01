
#Z80 CPU
from opcodes import *
from regs import *
from ram import *
from rom import *
from loggers import EmptyLogger
from debugger import EmptyDebugger
import sys


class CPU(object):

	@property
	def A(self):
		return self.regs[A]
	@A.setter
	def A(self, value):
		self.regs[A] = value

	@property
	def B(self):
		return self.regs[B]
	@B.setter
	def B(self, value):
		self.regs[B] = value

	@property
	def C(self):
		return self.regs[C]
	@C.setter
	def C(self, value):
		self.regs[C] = value

	@property
	def D(self):
		return self.regs[D]

	@D.setter
	def D(self, value):
		self.regs[D] = value

	@property
	def E(self):
		return self.regs[E]

	@E.setter
	def E(self, value):
		self.regs[E] = value

	@property
	def H(self):
		return self.regs[H]
	@H.setter
	def H(self, value):
		self.regs[H] = value

	@property
	def L(self):
		return self.regs[L];
	@L.setter
	def L(self, value):
		self.regs[L] = value

	@property
	def ZFlag(self):
		return self.flags[ZF]
	@ZFlag.setter
	def ZFlag(self, value):
		self.flags[ZF] = value

	@property
	def CFlag(self):
		return self.flags[CF]

	@CFlag.setter
	def CFlag(self, value):
		self.flags[CF] = value

	@property
	def NFlag(self):
		return self.flags[NF]

	@NFlag.setter
	def NFlag(self, value):
		self.flags[NF] = value

	@property
	def HFlag(self):
		return self.flags[HF]

	@HFlag.setter
	def HFlag(self, value):
		self.flags[HF] = value

	@property
	def SFlag(self):
		return self.flags[SF]

	@SFlag.setter
	def SFlag(self, value):
		self.flags[SF] = value

	@property
	def PVFlag(self):
		return self.flags[PVF]

	@PVFlag.setter
	def PVFlag(self, value):
		self.flags[PVF] = value

	@property
	def HL(self):
		return (self.regs[H] << 8) + self.regs[L]

	@HL.setter
	def HL(self, value):
		value = Bits.limitTo16bits(value)
		self.regs[H] = value >> 8
		self.regs[L] = value & 0xFF

	@property
	def HLPrim(self):
		return (self.regsPri[H] << 8) + self.regsPri[L]

	@HLPrim.setter
	def HLPrim(self, value):
		value = Bits.limitTo16bits(value)
		self.regsPri[H] = value >> 8
		self.regsPri[L] = value & 0xFF

	@property
	def DE(self):
		return (self.regs[D] << 8) + self.regs[E]

	@DE.setter
	def DE(self, value):
		value = Bits.limitTo16bits(value)
		self.regs[D] = value >> 8
		self.regs[E] = value & 0xFF

	@property
	def DEPrim(self):
		return (self.regsPri[D] << 8) + self.regsPri[E]

	@DEPrim.setter
	def DEPrim(self, value):
		value = Bits.limitTo16bits(value)
		self.regsPri[D] = value >> 8
		self.regsPri[E] = value & 0xFF

	@property
	def BC(self):
		return (self.regs[B] << 8) + self.regs[C]

	@BC.setter
	def BC(self, value):
		value = Bits.limitTo16bits(value)
		self.regs[B] = value >> 8
		self.regs[C] = value & 0xFF

	@property
	def BCPrim(self):
		return (self.regsPri[B] << 8) + self.regsPri[C]

	@BCPrim.setter
	def BCPrim(self, value):
		value = Bits.limitTo16bits(value)
		self.regsPri[B] = value >> 8
		self.regsPri[C] = value & 0xFF

	@property
	def I(self):
		return self.i

	@I.setter
	def I(self, value):
		self.i = value

	@property
	def IX(self):
		return self.ix

	@IX.setter
	def IX(self, value):
		self.ix = value

	@property
	def IY(self):
		return self.iy

	@IY.setter
	def IY(self, value):
		self.iy = value

	@property
	def PC(self):
		value = self.pc
		self.pc += 1
		return value

	@PC.setter
	def PC(self, value):
		self.pc = value

	def __init__(self,
				rom = ROM(), 
				ram = RAM(), 
				logger = EmptyLogger(),
				debugger = EmptyDebugger()):
		#Index registers
		self.ix = 0x00
		self.iy = 0x00
		self.sp = 0x00		
		self.pc = 0x00
		#special registers
		self.i = 0x00
		self.r = 0x00
		self.logger = logger
		self.debugger = debugger
		
		self.iff = 0x00

		self.interruptMode = 0

		self.regs = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00] #B,C,D,E,H,L,none,A
		self.regsPri = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00] #B',C',D',E',H',L',none,A'
		self.flags = [False,False,False,False,False,False,False,False]
		self.fls = [0x00]
		self.flsPri = [0x00] #flags'
		self.ports = [x for x in range(0,255)]
		
		self.ram = ram
		self.rom = rom
		
		self.dispatchTable = {
			0x00 : Opcodes.nop,
			0x01 : Opcodes.ld16,
			0x03 : Opcodes.inc16,
			0x04 : Opcodes.inc8,
			0x09 : Opcodes.add16,
			0xF3 : Opcodes.disableInterrupts,
			0xAF : Opcodes.xorA,
			0xB0 : Opcodes.xorA,
			0xB1 : Opcodes.xorA,
			0x0c: Opcodes.inc8,
			0x11 : Opcodes.ld16,
			0x13 : Opcodes.inc16,
			0x19 : Opcodes.add16,
			0x21 : Opcodes.ld16,
			0x22 : Opcodes.ldNnHl,
			0x23 : Opcodes.inc16,
			0x20 : Opcodes.jpnz,
			0x28 : Opcodes.jrz,
			0x29 : Opcodes.add16,
			0x2a : Opcodes.ldHl_addr,
			0x30 : Opcodes.jpnc,
			0x31 : Opcodes.ld16,
			0x32 : Opcodes.ldnn_a,
			0x33 : Opcodes.inc16,
			0x39 : Opcodes.add16,
			0x47 : Opcodes.ld8,
			0x62 : Opcodes.ld8,
			0x6b : Opcodes.ld8,
			0x3e : Opcodes.ld8n,
			0x2b : Opcodes.dec16b,
			0x36 : Opcodes.ld_addr,
			0xa7 : Opcodes._and,
			0xa4 : Opcodes._and,
			0xbc : Opcodes.cp,
			0xc3 : Opcodes.jp,
			0xd3 : Opcodes.out,
			0xd9 : Opcodes.exx,
			0xeb : Opcodes.ex_de_hl,
			0xed : self.twoBytesOpcodes,
			0xf9 : Opcodes.ld_sp_hl,
			0xfb : Opcodes.enableInterrupts,
			0xfd : self.twoBytesOpcodes,
			0xed43 : Opcodes.ldNnRr,
			0xed53 : Opcodes.ldNnRr,
			0xed47 : Opcodes.ldExt,
			0xed52 : Opcodes.sbc,
			0xed56 : Opcodes.im1,
			0xedb0 : Opcodes.ldir,
			0xedb8 : Opcodes.lddr,
			0xfd21 : Opcodes.ldiy,
			0xfd35 : Opcodes.dec_mem_at_iy
		}

	def readOp(self):
		pc = self.PC
		opcode = self.rom.readMemory(pc)
		self.dispatch(opcode, pc)

	def twoBytesOpcodes(self, cpu, opcode, logger):
		pc = self.PC
		secondOpByte = self.rom.readMemory(pc)
		fullOpcode = (opcode << 8) + secondOpByte
		self.dispatch(fullOpcode, pc)

	def dispatch(self, opcode, pc):
		try:
			self.debugger.next_opcode(pc, self)
			self.dispatchTable[opcode](self, opcode, self.logger)
		except KeyError as e:
			print "Missing opcode key: {1:x}, PC = 0x{0:x}".format(self.PC, opcode)
			self.debugger.stop(self)

	def run(self):
		while True:
			self.readOp()
