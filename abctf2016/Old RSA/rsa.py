import codecs

#egcd and modinv from http://stackoverflow.com/a/9758173
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
