from rom import ROM

B = 0
C = 1
D = 2
E = 3
H = 4
L = 5
A = 7

class CPU(object):
	def __init__(self, isDebugged = False):
		#Index registers
		self.ix = 0x00;
		self.iy = 0x00;
		self.sp = 0x00;		
		self.pc = 0x00;
		#special registers
		self.i = 0x00;
		self.r = 0x00;
		self.isDebugged = isDebugged
		
		self.iff = 0x00;
		
		self.regs = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B,C,D,E,H,L,none,A
		self.regsPri = [0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00]; #B',C',D',E',H',L',none,A'
		self.fls = [0x00];
		self.flsPri = [0x00]; #flags'
		
		self.rom = ROM();
		
		self.dispatch = {
			0xF3 : self.disableInterrupts,
			0xAF : self.xorA
		}
	
	def readOp(self):
		opcode = self.rom.readMemory(self.pc)		
		disp = self.dispatch[opcode](opcode)
		self.pc+=1

	def run(self):
		while True:
			self.readOp()
	
	def disableInterrupts(self, opcode):
		"""DI"""
		self.iff = 0x00;		
		self.debug("DI")

	def xorA(self, opcode):
		"""XOR A"""
		regInd = opcode & 7
		self.regs[A] = self.regs[A] ^ self.regs[regInd]
		self.debug("XOR A")

	def debug(self, str):
		"""print debug info"""
		if (self.isDebugged):
			print(str)
