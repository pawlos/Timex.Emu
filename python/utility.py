

class Bits(object):
	@staticmethod
	def count(value):
		#print value
		return bin(value).count('1')