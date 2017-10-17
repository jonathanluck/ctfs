# baby_crypt

### Crypto 350

We are given a server `nc crypto.chal.csaw.io 1578`, the information that the cookie we get is `input + flag`, and that this is AES in ECB (electronic code book) mode.

If we send the server a string, it replies with the string encrytped, appended to the flag. For example:
```
Enter your username (no whitespace): abcdef
Your Cookie is: f998e7c349343d2205c0db166b09b5f562d2ef447cbb3bdb206b8dd9c2f4b2a3348893c7445e928e940f9e034f5cea72
```

#### Explanation of the attack

For this example, I will explain the attack with a 4 byte (32 bit) example block cipher (note that the problem uses 128 bit AES).

When using ECB, if two blocks of data are the same, they both will encrpyt to the same value. For example if we encrypt `aaaabbbbaaaa` with our 4 byte cipher, we might get `fdsl89ewfdsl`. Notice how the first and last blocks of the ciphertext are the same. We will use this to solve this problem

Let's pretend the flag is `flag1234`. If we provide the server the input `aaaa`, the plaintext to be encrypted is `aaaaflag1234`. Where `aaaa`, `flag`, and `1234` will be encrypted as separate blocks.

We can use the fact that this is ECB to guess the flag one byte at a time. For example we can send the server `aaaf`, making the blocks `aaaf`, `flag`, and `1234`. We then record the output of the `aaaf` block (let's sat the output is `qwer`). We then send the server `aaa` (one byte shorter), and the blocks become `aaaf`, `lag1`, and `234` (with the last block being padded with some unkown value. Notice how the first block is also `aaaf`, which we said will encrypt to `qwer`. 

We now notice that we have `qwer` in both ciphertexts, meaning that our guess of `f` for the first character is right. We can perform this again until we get a full block of the flag. Then use the first block of the flag instead of a's

#### Code for the attack:

```python
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
```

Resulting flag: `flag{Crypt0_is_s0_h@rd_t0_d0...}`
