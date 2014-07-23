

class Bits(object):
	@staticmethod
	def count(value):
		return bin(value).count('1')