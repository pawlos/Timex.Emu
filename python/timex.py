import io

f = open('../rom/tc2048.rom','rb')
rom = f.read()
if len(rom) != 16384:
	raise Exception('Wrong rom size. Should be 16384 bytes long.') ;
print("ROM loaded...");
print("Sterting execution...");
eip = 0
while eip < len(rom):
	#for now we will only print rom bytes
	print("0x%0.2x" % rom[eip])
	eip+=1
print("Ending...")