import socket
import string


keyspace = string.printable[:-5]

def send_recv(s, string1, string2, block_num):
    #send our guess
    s.send(bytes(string1[16-(16-len(string2)):] + string2, "utf-8") + b"\n")
    a = s.recv(1024).decode("utf-8")
    b = a.split("\n")[0]
    b = b.replace("Your Cookie is: ", "")[:32]

    #force the block we are guessing to move forward into the previous block
    s.send(bytes(string1[16-(16-len(string2)):], "utf-8") + b"\n")
    c = s.recv(1024).decode("utf-8")
    d = c.split("\n")[0]
    d = d.replace("Your Cookie is: ", "")[32*block_num:32*(block_num +1)]

    #check to see if we are correct
    return d == b
    

#create and set up the socket
s = socket.socket()

s.connect(("crypto.chal.csaw.io", 1578))
s.recv(1024)

block = ""

#do the first block.
#Because we can directly access the first block of the flag, we can just use a's to front fill our test block
while(len(block) < 16):
    for char in keyspace:
        guess = block + char
        if(send_recv(s, "a"*16, guess, 0)):
            block += char
            print(block)
            break

#for testing purposes:
#block = "flag{Crypt0_is_s"
block2 = ""

#now we need to use the first block to offset the second block
while(len(block2) < 16):
    for char in keyspace:
        guess = block2 + char
        if(send_recv(s, block, guess, 1)):
            block2 += char
            print(block + block2)
            break
    
