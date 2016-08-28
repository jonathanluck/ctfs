import binascii

f = open("thor.txt", 'r')
lines = f.readlines()
out = ""
for l in lines:
	out += l[10:49].replace(' ', '')
outputfile = open("thor.lz",'w')
outputfile.write(binascii.unhexlify(out))
outputfile.close()
