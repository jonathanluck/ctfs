# Old RSA

### Cryptography

We get a file containing a ciphertext (c), public modulus (n), and public exponent (e):
```
c = 29846947519214575162497413725060412546119233216851184246267357770082463030225
n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
e = 3
```

First thing to notice: the public exponent is tiny. Modern forms of RSA use public moduli that are hundreds of digits long. This modulus is under 100 digits long, and thus can be factored easily.

##### Factoring the modulus
Cracking an RSA problem like this requires us to extract the two prime numbers (`p` and `q`) that were used to generate `n`. Doing so allows us to compute the private exponent (private key) `d`.

Because this modulus is very small, we can run it through [msieve](https://github.com/radii/msieve) to factor it.
![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Old%20RSA/5d260f377f.jpg)
Doing so nets us `p = 238324208831434331628131715304428889871` and `q = 296805874594538235115008173244022912163`

We now have all the components needed to decrypt the message.

##### Decryption

```python
import codecs

#egcd/modinv from http://stackoverflow.com/a/9758173
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


c = 29846947519214575162497413725060412546119233216851184246267357770082463030225
n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
e = 3
p = 238324208831434331628131715304428889871
q = 296805874594538235115008173244022912163

#https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
tot = n - (p + q - 1)
d = modinv(e, tot)
m = pow(c,d,n)

#convert to hex and clip off the '0x' at the beginning
string = hex(m)[2:]

#print as ascii
print(codecs.decode(string, 'hex'))
```

We use `p` and `q` to calculate `tot`, which is Euler's totient of `n`. We then use modular inverse to calculate `d` (the private exponent).

Using the build in `pow` function, we can quickly perform modular exponentiation. When using 3 arguments, `pow(x, y, z)` is equivalent to `(x ** y) % z` but performs the calculations much faster.

Our plaintext is `pow(c, d, n)`, which results in: `6872557977505747778161182217242712228364873860070580111494526546045`

Converting that to hex gets us: `0x41424354467b746831735f7761735f683472645f696e5f313938307d`

Which can be decoded into ascii to yield the flag: `ABCTF{th1s_was_h4rd_in_1980}`