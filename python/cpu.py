A = 7B = 0C = 1D = 2E = 3H = 4L = 5SF = 7ZF = 6HF = 4PVF = 2NF = 1CF = 0class CPU(object):	@property	def A(self):		return self.regs[A]	@A.setter	def A(self, value):		self.regs[A] = value	@property	def B(self):		return self.regs[B]	@B.setter	def B(self, value):		self.regs[B] = value	@property	def C(self):		return self.regs[C]	@C.setter	def C(self, value):		self.regs[C] = value	@property	def D(self):		return self.regs[D]	@D.setter	def F(self, value):		return self.regs[D]	@property	def E(self):		return self.regs[E]	@E.setter	def E(self, value):		self.regs[E] = value	@property	def H(self):		return self.regs[H]	@H.setter	def H(self, value):		self.regs[H] = value	@property	def L(self):		return self.regs[L];	@L.setter	def L(self, value):		self.regs[L] = value	@property	def ZFlag(self):		return self.flags[ZF]	@ZFlag.setter	def ZFlag(self, value):		self.flags[ZF] = value	@property	def CFlag(self):		return self.flags[CF]	@CFlag.setter	def CFlag(self, value):		self.flags[CF] = value	@property	def NFlag(self):		return self.flags[NF]	@NFlag.setter	def NFlag(self, value):		self.flags[NF] = value	@property	def HFlag(self):		return self.flags[HF]	@HFlag.setter	def HFlag(self, value):		self.flags[HF] = value	@property	def SFlag(self):		return self.flags[SF]	@SFlag.setter	def SFlag(self, value):		self.flags[SF] = value	def __init__(self, rom, isDebugged = False):		#Index registers		self.ix = 0x00;		self.iy = 0x00;		self.sp = 0x00;				self.pc = 0x00;		#special registers		self.i = 0x00;		self.r = 0x00;		self.isDebugged = isDebugged				self.iff = 0x00;				self.regs = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B,C,D,E,H,L,none,A		self.regsPri = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B',C',D',E',H',L',none,A'		self.flags = [False,False,False,False,False,False,False,False]		self.fls = [0x00];		self.flsPri = [0x00]; #flags'				self.rom = rom;				self.dispatch = {			0xF3 : self.disableInterrupts,			0xAF : self.xorA		}		def readOp(self):		opcode = self.rom.readMemory(self.pc)				disp = self.dispatch[opcode](opcode)		self.pc+=1	def run(self):		while True:			self.readOp()		def disableInterrupts(self, opcode):		"""DI"""		self.iff = 0x00;				self.debug("DI")	def xorA(self, opcode):		"""XOR A"""		regInd = opcode & 7		self.debug(regInd)		self.debug(self.regs[A])		self.debug(self.regs[regInd])		self.regs[A] = self.regs[A] ^ self.regs[regInd]		"""Flags"""		self.flags[ZF] = True if self.regs[A] == 0 else False		self.flags[CF] = False		self.flags[NF] = False		self.flags[HF] = False		self.flags[SF] = True if self.regs[A] & 0x80 else False		self.debug("XOR A")	def setFlags(self, value):		self.debug(value)			def debug(self, str):		"""print debug info"""		if (self.isDebugged):			print(str)