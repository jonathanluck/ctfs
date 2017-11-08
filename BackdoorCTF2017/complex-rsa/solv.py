from Crypto.PublicKey import RSA
from base64 import b64decode
import RSAExploits
import binascii

pk1 = b64decode("".join([i.strip() for i in open("pubkey1").readlines()[1:-1]]))
pk2 = b64decode("".join([i.strip() for i in open("pubkey2").readlines()[1:-1]]))

key1 = RSA.importKey(pk1)
key2 = RSA.importKey(pk2)

n = key1.n
e1 = key1.e
e2 = key2.e

e12 = e1 * e2

r = RSAExploits.RSAData(RSAExploits.rsa_obj(n, e12))

w = RSAExploits.Wiener()

w.run([r])

c = int(open("flag(1).enc").read().encode("hex"),16)

m = pow(c, r.get_d(), n)

print(hex(m)[2:-1].decode("hex"))
