from rom import ROM

class CPU(object):
	def __init__(self):
		#Index registers
		self.ix = 0x00;
		self.iy = 0x00;
		self.sp = 0x00;		
		self.pc = 0x00;
		#special registers
		self.i = 0x00;
		self.r = 0x00;
		
		self.regs = []; #A,B,C,D,E,H,L
		self.regsPri = []; #A',B',C',D',E',H',L;
		self.fls = 0x00;
		self.flsPri = 0x00; #flags'
		
		self.rom = ROM();
		
		self.dispatch = {			
		};
	
	def readOp(self):
		opcode = self.rom.readMemory(self.pc);
		print("0x%0.2x" % opcode)
		self.pc+=1;

	def run(self):
		while True:
			self.readOp();