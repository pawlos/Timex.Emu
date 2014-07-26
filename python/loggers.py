# Logger class

class Logger(object):

	def info(self, msg):
		print msg

class EmptyLogger(object):
	def info(self, msg):
		pass