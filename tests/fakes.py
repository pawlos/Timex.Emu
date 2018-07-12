class FakeRom(object):
	
	def __init__(self, romdata):
		self.data = bytearray(romdata)

	def __getitem__(self, index):
		return self.data[index]

	def __len__(self):
		return len(self.data)

class FakeCpu(object):

	def __init__(self):
		self.logger = None
