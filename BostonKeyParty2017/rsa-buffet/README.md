#RSA Buffet

###Crypto

We are given a problem with 5 ciphertexts, 10 public keys and a couple of .py files for the [encryption](https://github.com/jonathanluck/ctfs/blob/master/BostonKeyParty2017/rsa-buffet/encrypt.py) and [message sharing](https://github.com/jonathanluck/ctfs/blob/master/BostonKeyParty2017/rsa-buffet/generate-plaintexts.py) format. The problem text says essentially: with what you are given, crack at least 3 of the ciphertexts, then put them back together to get a flag.

I solved this problem by exploiting 3 different weak implementations:
* Shared primes (Keys 0 and 6)
* Fermat factorization (Key 1)
* Wiener's attack (Key 3)

Python libraries I had to install for [my solution code](https://github.com/jonathanluck/ctfs/blob/master/BostonKeyParty2017/rsa-buffet/rsa.py):
* [RSAExploits](https://github.com/vik001ind/RSAExploits) (by far the most useful to have for future CTFs)
* [PyCrypto](https://pypi.python.org/pypi/pycrypto)
* [SecretSharing](https://github.com/blockstack/secret-sharing)

#### Shared primes:
The assumption behind this attack was that we didn't get to see how the keys were generated, and with 10 keys, there is probably a chance the problem writers would give us a gimme and share a prime between two public moduli.

This attack works because finding the GCD of two numbers is extremely fast even if the numbers are large. If two of the moduli share a prime, then their GCD will be something other than 1. Once we find a common factor, then we can compute the other prime for each moduli and therefore compute each private key.

We start by loading in all the public keys and getting the public moduli out of them:

```Python
from Crypto.PublicKey import RSA

a = [open("key-{}.pem".format(i)).read() for i in range(10)]
#turn them into usuable public keys
b = [RSA.importKey(k) for k in a]
#get all their moduli
n = [pk.key.n for pk in b]
#read all the ciphertexts
cts = [open("ciphertext-{}.bin".format(i), 'rb').read() for i in range(1,6)
```
Next, we need to loop through each pair of moduli and try to find if there is a pair that share a common factor:

```Python
from fractions import gcd

#first decryption: common factor
n1 = 1
p1 = 1
q1 = 1
e1 = 1

#loop through every pair of moduli checking for common factors.
#If we find one, use it to decrypt a message
for i in range(10):
    for j in range(i+1, 10):
        if(gcd(n[i], n[j]) != 1):
            n1 = n[i]
            e1 = b[i].key.e
            p1 = gcd(n[i], n[j])
            q1 = n1 / p1
            break
```

Then we do our standard calculations to obtain the private key (`decrypt` is the function that they gave us in `encrypt.py`. It returns `None` if the key is wrong or the ciphertext if the key is right):

```Python
assert p1 * q1 == n1
tot1 = n1 - (p1 + q1 - 1)
d1 = modinv(e1, tot1)
privkey1 = RSA.construct((n1, e1, d1))
#decrypt a ciphertext
for c in cts:
    temp = decrypt(privkey1, c)
    if(temp):
        plaintexts.append(temp)
        break
```

Looking at the decrypted plaintext, we get something like this:
```
Congratulations, you decrypted a ciphertext!  One down, two to go :)\n3-17e568ddc3ed3e6fe330ca47a2b27a2707edd0e0839df59fe9114fe6c08c6fc1ac1c3c8d9ab3cf7860dac103dff464d4c215e197b54f0cb46993912c3d0220a3eb1b80adf33ee2cc59b0372c\n3-b69efb4f9c5205175a4c9afb9d3c7bef728d9fb6c9cc1241411b31d4bd18744660391a330cefa8a86af8d2b80c881cfa\n3-572e70c5acfbe8b4c2cbd47217477d217da88c256ff2586af6a18391972c258bbea6143e7cd2ff6d39393efeb64d51d9318a2c337e50e2d764a42173bc3a1d5c7c8f24b64043daf5d2a8e9f4\n3-e9e6850880eb0a44d36fe9f2e5a458c6da3977b7fcd285afa27e9bfc116b1408570991504116b81864b03a7060bfd5d3fb6e007bb346f276d749befd545d1489c4\n
```
For now it is unreadable, but later we will combine all 3 of the plaintexts at the end to get the flag.

#### Fermat factorization:
This was also based on a guess. The theory behind a Fermat factorization attack is that the two primes are relatively close to each other, making N very close to p<sup>2</sup> or q<sup>2</sup>. Based on this, searching around sqrt(N) should yeild one of the primes, and therefore allowing us to compute the private key.

For this attack, we will use the [RSAExploits](https://github.com/vik001ind/RSAExploits) library (mainly because we will use it again later):

```Python
import RSAExploits

#next up is fermat factorization
f = []
for k in b:
	f.append(RSAExploits.rsa_obj(k.key.n, k.key.e))
y = [RSAExploits.RSAData(i) for i in f]
ferm = RSAExploits.Fermat()
ferm.run(y)
```

We start by taking all the keys and turning them into RSA objects and then into RSAData objects (what RSAExploits works with). We then initialize a Fermat exploit, and run it on the list of RSAData objects. The result is then saved into whichever RSAData object was cracked. We then perform a search through the RSAData objects to see which one was cracked. Finding the private key and decrypting another ciphertext is done the same as the first example:
```Python
n2 = 1
p2 = 1
q2 = 1
e2 = 1
for data in y:
    if(data.get_p()):
        n2 = data.get_n()
        p2 = data.get_p()
        q2 = data.get_q()
        e2 = data.get_e()
```

#### Wiener's attack:
This one was based on the observation that e on key-3 was exceptionally large. This looked very similar to [examples](https://en.wikipedia.org/wiki/Wiener's_attack#Example) found online.

For this attack, we will continue to use `y` from the last exploit, and we will also continue to use RSAExploits.

```Python
w = RSAExploits.Wiener()
#we know to run it only on key-3.pem because the public exponent in that key is very large
w.run([y[3]])

n3 = n[3]
p3 = y[3].get_p()
q3 = y[3].get_q()
e3 = b[3].key.e
assert p3 * q3 == n3
```

Finding the private key and decrypting a ciphertext is the same as the fist example

#### Combining the plaintexts:
In order to ensure that we needed to decrypt at least 3 ciphertexts, the problem writers split up the flag using a secret sharing scheme.

We need to take the plaintexts that we decrypted and pass it through the same library that they used to recombine the messages.

```Python
#cut off the congratulations messages and break up each line
pt1 = plaintexts[0].strip().split("\n")[1:]
pt2 = plaintexts[1].strip().split("\n")[1:]
pt3 = plaintexts[2].strip().split("\n")[1:]

#zip them together and recover the secret.
#zipped so we can combine pt1[n] pt2[n] and pt3[n] easily 
for i in zip(pt1, pt2, pt3):
    print(PlaintextToHexSecretSharer.recover_secret(i))
```
We take off the congratulations message from each one. Then we break them apart line by line. After that, we zip the lists together, and iterate through the zippedl lists.

In the end, we get the flag: `FLAG{ndQzjRpnSP60NgWET6jx}`

Solution code combining all 3 attacks and secret recovery (written for python 2, but can be easily changed to python 3 w/ minor modifications to handle integer division): [rsa.py](https://github.com/jonathanluck/ctfs/blob/master/BostonKeyParty2017/rsa-buffet/rsa.py)
