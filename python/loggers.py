# Logger class

class Logger(object):
	def __init__(self, cpu):
		self.cpu = cpu
	
	def info(self, msg):
		print "{0:4X}: {1}".format(self.cpu.prev_pc, msg)

class EmptyLogger(object):
	def info(self, msg):
		pass