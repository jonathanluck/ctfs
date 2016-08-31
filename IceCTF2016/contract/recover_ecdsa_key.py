import hashlib
import binascii

#https://pypi.python.org/pypi/ecdsa/
from ecdsa import SigningKey, NIST384p
from ecdsa import VerifyingKey
from ecdsa.numbertheory import inverse_mod

#sources:
#http://antonio-bc.blogspot.com/2013/12/mathconsole-ictf-2013-writeup.html
#https://neg9.org/news/2015/8/12/openctf-2015-veritable-buzz-1-crypto-300-writeup

#public key we pulled from the server
public_key_ec_pem = """
-----BEGIN PUBLIC KEY-----
MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEgTxPtDMGS8oOT3h6fLvYyUGq/BWeKiCB
sQPyD0+2vybIT/Xdl6hOqQd74zr4U2dkj+2q6+vwQ4DCB1X7HsFZ5JczfkO7HCdY
I7sGDvd9eUias/xPdSIL3gMbs26b0Ww0
-----END PUBLIC KEY-----
"""
public_key_ec = VerifyingKey.from_pem(public_key_ec_pem.strip())
curve_order = public_key_ec.curve.order

#"help" and "time" sigs we obtained from the packet capture
h = "c0e1fc4e3858ac6334cc8798fdec40790d7ad361ffc691c26f2902c41f2b7c2fd1ca916de687858953a6405423fe156cfd7287caf75247c9a32e52ab8260e7ff1e46e55594aea88731bee163035f9ee31f2c2965ac7b2cdfca6100d10ba23826"
t = "c0e1fc4e3858ac6334cc8798fdec40790d7ad361ffc691c26f2902c41f2b7c2fd1ca916de687858953a6405423fe156c0cbebcec222f83dc9dd5b0d4d8e698a08ddecb79e6c3b35fc2caaa4543d58a45603639647364983301565728b504015d"


def string_to_number(tstr):
    return int(binascii.hexlify(tstr), 16)
    
def sha256(content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(content)
    return sha256_hash.digest()

def recover_key(c1,sig1,c2,sig2,pubkey):
    #using the same variable names as in:
    #http://en.wikipedia.org/wiki/Elliptic_Curve_DSA

    curve_order = pubkey.curve.order

    n = curve_order
    s1 = int(sig1[96:],16)
    print("s1: " + str(s1))
    s2 = int(sig2[96:],16)
    print("s2: " + str(s2))
    r = int(sig1[:-96], 16)
    print("r: " + str(r))
    print("R values match: " + str(int(sig2[:-96],16) == r))

    z1 = string_to_number(sha256(c1))
    z2 = string_to_number(sha256(c2))

    #magical math stuff
    sdiff_inv = inverse_mod(((s1-s2)%n),n)
    k = ( ((z1-z2)%n) * sdiff_inv) % n
    r_inv = inverse_mod(r,n)
    da = (((((s1*k) %n) -z1) %n) * r_inv) % n
    print("Recovered Da: " + hex(da))

    #turn the private key into a signing key
    recovered_private_key_ec = SigningKey.from_secret_exponent(da, curve=NIST384p)
    return recovered_private_key_ec
        
vk = VerifyingKey.from_pem(public_key_ec_pem.strip())

#verify the sig we intercepted is valid (i.e. we didn't screw up importing the public key)
print("Help sig verified: " + str(vk.verify(binascii.unhexlify(h), "help", hashfunc=hashlib.sha256)))

#get the signing key from the sigs that we have
key = recover_key("help", h, "time", t, public_key_ec)
print("Recovered private key: \n" + key.to_pem())

#create a forged signature for "read flag.txt"
print("Command with forged sig:\n\nread flag.txt:"+key.sign_digest(sha256("read flag.txt")).encode("hex"))



