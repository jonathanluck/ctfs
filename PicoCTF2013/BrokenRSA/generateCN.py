import socket
import binascii
from time import sleep
import gmpy2

def pad(stri):
        if(len(stri)%2==1):
                return stri.zfill(len(stri)+1)
        else:
                return stri

def digify(s):
        return int((s).encode("hex"),16)

threshold = int(1.24*digify("A"*40)-digify("A"*40))
def find(lo,hi,s):
	#print(str(lo))
	#print(str(hi))
	#print()
	#print()
	#print()
	if(hi-lo<threshold):
		return hi
	if (hi < lo):
	        return -1
	mid = (hi+lo)/2
	if (check(binascii.a2b_hex(pad(hex(mid)[2:-1])),s)):
		return find(mid,hi,s)
	else:
		return find(lo,mid,s)

def check(m,s):
	s.send(m+"\n")
	sleep(1)
	return s.recv(2048).split("\n")[2]==AAA(m+"\n")
	
def AAA(m):
	return hex(pow(int(m.encode("hex"), 16),3))	

def strify(n):
        return binascii.a2b_hex(pad(hex(n)[2:-1]))




s=socket.socket()
s.connect(("vuln.picoctf.com",6666))
sleep(1)
start = s.recv(2048)
start = start.split("\n")
#print(start[9])
print("c="+str(int(start[9][2:-1],16)))
sleep(1)
assert check("A"*40, s)
assert check("A"*42, s) == False
hi = find(int(("A"*40).encode("hex"),16), int(("A"*42).encode("hex"),16), s)
hinl = digify(strify(hi)+"\n")
s.send(strify(hi)+"\n")
sleep(3)
rec = int(s.recv(2048).split("\n")[2][2:-1], 16)
n = pow(digify(strify(hi)+"\n"),3) - rec
print("n="+str(n))
assert pow(hinl,3,n)==rec
