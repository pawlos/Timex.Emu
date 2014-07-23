from opcodes import Opcodesfrom regs import *class CPU(object):	@property	def A(self):		return self.regs[A]	@A.setter	def A(self, value):		self.regs[A] = value	@property	def B(self):		return self.regs[B]	@B.setter	def B(self, value):		self.regs[B] = value	@property	def C(self):		return self.regs[C]	@C.setter	def C(self, value):		self.regs[C] = value	@property	def D(self):		return self.regs[D]	@D.setter	def F(self, value):		return self.regs[D]	@property	def E(self):		return self.regs[E]	@E.setter	def E(self, value):		self.regs[E] = value	@property	def H(self):		return self.regs[H]	@H.setter	def H(self, value):		self.regs[H] = value	@property	def L(self):		return self.regs[L];	@L.setter	def L(self, value):		self.regs[L] = value	@property	def ZFlag(self):		return self.flags[ZF]	@ZFlag.setter	def ZFlag(self, value):		self.flags[ZF] = value	@property	def CFlag(self):		return self.flags[CF]	@CFlag.setter	def CFlag(self, value):		self.flags[CF] = value	@property	def NFlag(self):		return self.flags[NF]	@NFlag.setter	def NFlag(self, value):		self.flags[NF] = value	@property	def HFlag(self):		return self.flags[HF]	@HFlag.setter	def HFlag(self, value):		self.flags[HF] = value	@property	def SFlag(self):		return self.flags[SF]	@SFlag.setter	def SFlag(self, value):		self.flags[SF] = value	@property	def PVFlag(self):		return self.flags[PVF]	@PVFlag.setter	def PVFlag(self, value):		self.flags[PVF] = value	@property	def HL(self):		return (self.regs[H] << 8) + self.regs[L]	@HL.setter	def HL(self, value):		self.regs[H] = value >> 8		self.regs[L] = value & 0xFF	@property	def DE(self):		return (self.regs[D] << 8) + self.regs[E]	@DE.setter	def DE(self, value):		self.regs[D] = value >> 8		self.regs[E] = value & 0xFF	def __init__(self, rom, isDebugged = False):		#Index registers		self.ix = 0x00;		self.iy = 0x00;		self.sp = 0x00;				self.pc = 0x00;		#special registers		self.i = 0x00;		self.r = 0x00;		self.isDebugged = isDebugged				self.iff = 0x00;				self.regs = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B,C,D,E,H,L,none,A		self.regsPri = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B',C',D',E',H',L',none,A'		self._16bitRegs = {HL: self.HL, DE: self.DE}		self.flags = [False,False,False,False,False,False,False,False]		self.fls = [0x00];		self.flsPri = [0x00]; #flags'				self.rom = rom;				self.dispatch = {			0xF3 : Opcodes.disableInterrupts,			0xAF : Opcodes.xorA,			0xB0 : Opcodes.xorA,			0xB1 : Opcodes.xorA,			0x11 : Opcodes.ld16,			0x47 : Opcodes.ld8,			0xc3 : Opcodes.jp,		}		def readOp(self):		self.debug(self.pc)		opcode = self.rom.readMemory(self.pc)		if self.dispatch[opcode](self, opcode) == None:			self.pc+=1	def run(self):		while True:			self.readOp()			def debug(self, str):		"""print debug info"""		if (self.isDebugged):			print(str)