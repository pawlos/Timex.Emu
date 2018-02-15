# IO prots


class IO(object):

	def __init__(self):
		self.ports = [0x00]*0xff

	def readFrom(self, port):
		return self.ports[port]

	def writeTo(self, port):
		pass
