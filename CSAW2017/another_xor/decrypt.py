import codecs

ct = codecs.decode(open("encrypted", "r").read().strip(), "hex")

keylen = 67
message_len = 38

known = [0] * (keylen -5)
start = [i^j for i,j in zip(ct, b'flag{')]
known = start + known

low = 0 
for j in range(67):
    
    for i in range(5):
        known[(message_len + low + i) % keylen] = ct[message_len + ((low + i) % keylen)] ^ known[(low + i) % keylen]

    low = (low + message_len) % keylen
    print(bytes(known), low, j)

key = bytes(known)

message = ct[:message_len]

print("".join(chr(i ^ j) for i,j in zip(key,message)))
