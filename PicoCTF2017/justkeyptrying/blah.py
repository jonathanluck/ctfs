import string

lines = [l.strip().split(",")[6] for l in open("blah.csv", "r").readlines()]


s = string.ascii_lowercase +string.digits[1:] + "0" + "\n\x00\x00\t _+{}|"

d = {i : s[i-4] for i in range(4,4+len(s))}

output = ""

for f in lines:
	if(int(f[5:7],16) != 0):
		output += d[int(f[5:7],16)]

print(output)
