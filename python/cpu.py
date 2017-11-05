#Z80 CPU
from opcodes import *
from regs import *
from ram import *
from rom import *
from loggers import EmptyLogger
from debugger import EmptyDebugger


class CPU(object):

	@property
	def A(self):
		return self.regs[A]
	@A.setter
	def A(self, value):
		self.regs[A] = Bits.limitTo8Bits(value)

	@property
	def F(self):
		return self.regs[F]
	@F.setter
	def F(self, value):
		self.regs[F] = Bits.limitTo8Bits(value)

	@property
	def B(self):
		return self.regs[B]
	@B.setter
	def B(self, value):
		self.regs[B] = Bits.limitTo8Bits(value)

	@property
	def C(self):
		return self.regs[C]
	@C.setter
	def C(self, value):
		self.regs[C] = Bits.limitTo8Bits(value)

	@property
	def D(self):
		return self.regs[D]

	@D.setter
	def D(self, value):
		self.regs[D] = Bits.limitTo8Bits(value)

	@property
	def E(self):
		return self.regs[E]

	@E.setter
	def E(self, value):
		self.regs[E] = Bits.limitTo8Bits(value)

	@property
	def H(self):
		return self.regs[H]
	@H.setter
	def H(self, value):
		self.regs[H] = Bits.limitTo8Bits(value)

	@property
	def L(self):
		return self.regs[L];
	@L.setter
	def L(self, value):
		self.regs[L] = Bits.limitTo8Bits(value)

	@property
	def R(self):
		return self.R;

	@R.setter
	def R(self, value):
		self.R = value

	@property
	def ZFlag(self):
		return Bits.getNthBit(self.F,ZF) == 1

	@ZFlag.setter
	def ZFlag(self, value):
		self.F = Bits.setNthBit(self.F, ZF, 1 if value else 0)

	@property
	def CFlag(self):
		return Bits.getNthBit(self.F, CF) == 1

	@CFlag.setter
	def CFlag(self, value):
		self.F = Bits.setNthBit(self.F, CF, 1 if value else 0)

	@property
	def NFlag(self):
		return Bits.getNthBit(self.F, NF) == 1

	@NFlag.setter
	def NFlag(self, value):
		self.F = Bits.setNthBit(self.F, NF, 1 if value else 0)

	@property
	def HFlag(self):
		return Bits.getNthBit(self.F, HF) == 1

	@HFlag.setter
	def HFlag(self, value):
		self.F = Bits.setNthBit(self.F, HF, 1 if value else 0)

	@property
	def SFlag(self):
		return Bits.getNthBit(self.F, SF) == 1

	@SFlag.setter
	def SFlag(self, value):
		self.F = Bits.setNthBit(self.F, SF, 1 if value else 0)

	@property
	def PVFlag(self):
		return Bits.getNthBit(self.F, PVF) == 1

	@PVFlag.setter
	def PVFlag(self, value):
		self.F = Bits.setNthBit(self.F, PVF, 1 if value else 0)

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
		
		self.iff1 = 0x00
		self.iff2 = 0x00

		self.interruptMode = 0

		self.regs = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00,0x00] #B,C,D,E,H,L,none,A, F
		self.regsPri = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00] #B',C',D',E',H',L',none,A'
		self.fls = [0x00]
		self.flsPri = [0x00] #flags'
		self.ports = [x for x in range(0,255)]
		
		self.ram = ram
		self.rom = rom
		
		self.dispatchTable = {
			0x00 : Opcodes.nop,
			0x01 : Opcodes.ld16,
			0x02 : Opcodes.ld_bc_a,
			0x03 : Opcodes.inc16,
			0x04 : Opcodes.inc8,
			0x05 : Opcodes.dec8b,
			0x06 : Opcodes.ld8n,
			0x09 : Opcodes.add16,
			0x0a : Opcodes.ld_a_bc,
			0x0b : Opcodes.dec16b,
			0x0c : Opcodes.inc8,
			0x0e : Opcodes.ld8n,
			0x0f : Opcodes.rrca,
			0x10 : Opcodes.djnz,
			0x11 : Opcodes.ld16,
			0x12 : Opcodes.ld_de_a,
			0x13 : Opcodes.inc16,
			0x16 : Opcodes.ld8n,
			0x17 : Opcodes.lra,
			0x18 : Opcodes.jr_e,
			0x19 : Opcodes.add16,
			0x1a : Opcodes.ld_a_de,
			0x1b : Opcodes.dec16b,
			0x1e : Opcodes.ld8n,
			0x1f : Opcodes.rra,
			0x20 : Opcodes.jpnz,
			0x21 : Opcodes.ld16,
			0x22 : Opcodes.ldNnHl,
			0x23 : Opcodes.inc16,
			0x26 : Opcodes.ld8n,
			0x28 : Opcodes.jrz,
			0x29 : Opcodes.add16,
			0x2a : Opcodes.ldHl_addr,
			0x2b : Opcodes.dec16b,
			0x2e : Opcodes.ld8n,
			0x30 : Opcodes.jpnc,
			0x31 : Opcodes.ld16,
			0x32 : Opcodes.ldnn_a,
			0x33 : Opcodes.inc16,
			0x36 : Opcodes.ld_addr,
			0x39 : Opcodes.add16,
			0x3a : Opcodes.ld_a_nn,
			0x3b : Opcodes.dec16b,
			0x3e : Opcodes.ld8n,
			0x46 : Opcodes.ld_r_hl,
			0x47 : Opcodes.ld8,
			0x4e : Opcodes.ld_r_hl,
			0x57 : Opcodes.ld8,
			0x56 : Opcodes.ld_r_hl,
			0x5e : Opcodes.ld_r_hl,
			0x5f : Opcodes.ld8,
			0x62 : Opcodes.ld8,
			0x66 : Opcodes.ld_r_hl,
			0x67 : Opcodes.ld8,
			0x6b : Opcodes.ld8,
			0x6e : Opcodes.ld_r_hl,
			0x6f : Opcodes.ld8,
			0x70 : Opcodes.ldhlr,
			0x71 : Opcodes.ldhlr,
			0x72 : Opcodes.ldhlr,
			0x73 : Opcodes.ldhlr,
			0x74 : Opcodes.ldhlr,
			0x75 : Opcodes.ldhlr,
			0x77 : Opcodes.ldhlr,
			0x78 : Opcodes.ld8,
			0x7a : Opcodes.ld8,
			0x7e : Opcodes.ld_r_hl,
			0x87 : Opcodes.add_r,
			0x90 : Opcodes.sub_r,
			0x91 : Opcodes.sub_r,
			0xa7 : Opcodes._and,
			0xa4 : Opcodes._and,
			0xAF : Opcodes.xorA,
			0xB0 : Opcodes.xorA,
			0xB1 : Opcodes.xorA,
			0xb3 : Opcodes._or,
			0xbc : Opcodes.cp,
			0xc1 : Opcodes.pop,
			0xc2 : Opcodes.jp_cond,
			0xc3 : Opcodes.jp,
			0xc5 : Opcodes.push,
			0xc6 : Opcodes.add_r_n,
			0xc7 : Opcodes.rst,
			0xc9 : Opcodes.ret,
			0xca : Opcodes.jp_cond,
			0xcd : Opcodes.call,
			0xcf : Opcodes.rst,
			0xd1 : Opcodes.pop,
			0xd2 : Opcodes.jp_cond,
			0xd3 : Opcodes.out,
			0xd4 : Opcodes.call_cond,
			0xd5 : Opcodes.push,
			0xd6 : Opcodes.sub_n,
			0xd7 : Opcodes.rst,
			0xd9 : Opcodes.exx,
			0xda : Opcodes.jp_cond,
			0xdd : [self.twoBytesOpcodes],
			0xdf : Opcodes.rst,
			0xe0 : Opcodes.jp_cond,
			0xe1 : Opcodes.pop,
			0xe5 : Opcodes.push,
			0xe4 : Opcodes.call_cond,
			0xe6 : Opcodes.and_n,
			0xe7 : Opcodes.rst,
			0xe8 : Opcodes.jp_cond,
			0xeb : Opcodes.ex_de_hl,
			0xec : Opcodes.call_cond,
			0xed : [self.twoBytesOpcodes],
			0xef : Opcodes.rst,
			0xf1 : Opcodes.pop,
			0xf2 : Opcodes.jp_cond,
			0xf3 : Opcodes.disableInterrupts,
			0xf4 : Opcodes.call_cond,
			0xf5 : Opcodes.push,
			0xf6 : Opcodes.or_n,
			0xf7 : Opcodes.rst,
			0xf9 : Opcodes.ld_sp_hl,
			0xfa : Opcodes.jp_cond,
			0xfb : Opcodes.enableInterrupts,
			0xfc : Opcodes.call_cond,
			0xfd : [self.twoBytesOpcodes],
			0xff : Opcodes.rst,
			0xdd2a : Opcodes.ld_ix_nn,
			0xdde1 : Opcodes.pop_ix,
			0xed42 : Opcodes.sbc,
			0xed43 : Opcodes.ldNnRr,
			0xed44 : Opcodes.neg,
			0xed46 : Opcodes.im0,
			0xed47 : Opcodes.ldExt,
			0xed4f : Opcodes.ldra,
			0xed52 : Opcodes.sbc,
			0xed56 : Opcodes.im1,
			0xed53 : Opcodes.ldNnRr,
			0xed5e : Opcodes.im2,
			0xed5f : Opcodes.ldar,
			0xed63 : Opcodes.ldNnRr,
			0xed67 : Opcodes.rrd,
			0xed6f : Opcodes.rld,
			0xed73 : Opcodes.ldNnRr,
			0xed7b : Opcodes.ld16_nn,
			0xedb0 : Opcodes.ldir,
			0xedb8 : Opcodes.lddr,
			0xfd21 : Opcodes.ldiy,
			0xfd35 : Opcodes.dec_mem_at_iy,
			0xfd36 : Opcodes.ldiy_d_n,
			0xfd46 : Opcodes.ld_r_iy_d,
			0xfd4e : Opcodes.ld_r_iy_d,
			0xfd56 : Opcodes.ld_r_iy_d,
			0xfd5e : Opcodes.ld_r_iy_d,
			0xfd66 : Opcodes.ld_r_iy_d,
			0xfd6e : Opcodes.ld_r_iy_d,
			0xfd75 : Opcodes.ldiy_d_r,
			0xfd7e : Opcodes.ld_r_iy_d,
			0xfd86 : Opcodes.add_iy,
			0xfdcb : [self.fourBytesOpcodes],
			0xfdcb01ce : Opcodes.bit_set,
			0xfdcb014e : Opcodes.bit_bit,
			0xfdcb0246 : Opcodes.bit_bit,
			0xfdcb0476 : Opcodes.bit_bit,
			0xfdcb308e : Opcodes.bit_res,
			0xfdcb3086 : Opcodes.bit_res,
		}

	def generateInterrupt(self):
		if self.interruptMode == 1:
			self.PC = 0x38

	def readOp(self):
		pc = self.PC
		opcode = self.rom.readMemory(pc)
		self.dispatch(opcode, pc)

	def twoBytesOpcodes(self, cpu, opcode, logger):
		pc = self.PC
		secondOpByte = self.rom.readMemory(pc)
		fullOpcode = (opcode << 8) + secondOpByte
		self.dispatch(fullOpcode, pc)

	def fourBytesOpcodes(self, cpu, opcode, logger):
		pc = self.PC
		thirdbyte = cpu.rom.readMemory(pc)
		fourthbyte = cpu.rom.readMemory(cpu.PC)
		fullOpcode = (opcode << 16) + (thirdbyte << 8) + fourthbyte
		self.dispatch(fullOpcode, pc)

	def dispatch(self, opcode, pc):
		try:
			_dispatch = self.dispatchTable[opcode]
			if type(_dispatch) is not list:
				self.debugger.next_opcode(pc, self)
			else:
				_dispatch = _dispatch[0]
			_dispatch(self, opcode, self.logger)
		except KeyError as e:
			print "Missing opcode key: {1:x}, PC = 0x{0:x}".format(self.PC, opcode)
			self.debugger.stop(self)

	def run(self):
		while True:
			self.readOp()
