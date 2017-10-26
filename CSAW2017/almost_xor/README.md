# almost_xor

### Crypto 200

We are given a ciphertext
```
809fdd88dafa96e3ee60c8f179f2d88990ef4fe3e252ccf462deae51872673dcd34cc9f55380cb86951b8be3d8429839
```
and a python source file.

The python file contains several functions, but most notably, there is an encrypt function which takes in two strings
`k`, `m`, and an integer `n`.

The encryption function essentially breaks the input message and the key into blocks of `n` bits and encrypts each block in the message with the corresponding block in the key.

For example, let's say we have the message `m = "hello"` and the key `k = "world"`, and `n = 5` The binary represention of these strings is:

```
01101000 01100101 01101100 01101100 01101111  
01110111 01101111 01110010 01101100 01100100
```

Breaking these strings into blocks of size `n`, we have

```
01101 00001 10010 10110 11000 11011 00011 01111  
01110 11101 10111 10111 00100 11011 00011 00100
```
For each pair of blocks, the program computes the sum, and then takes the last `n` bits (cutting off any overflow).
```
11011 11110 01001 01101 11100 10110 00110 10011  
```
This sequence of bits is then converted back into a string.

You might notice there are potential issues if a block ends in the middle of a byte.
For example, if `m = "hell"`, `k = "worl"`, `n=5` then when we try to break the input into blocks of 5 bits, we get this,
```
01101 00001 10010 10110 11000 11011 00  
01110 11101 10111 10111 00100 11011 00
```
and the last block only has 2 bits.

The program deals with this by first cutting the input string into bigger blocks of `n` _bytes_ (adding null characters on the end if needed).
Each block will have `n*8` bits, which means it can be divided evenly into smaller blocks of size `n` bits.

This is why the program has `m_val_list` and `m_vals`. `m_val_list` is a list of lists, where each inner list represents a block of `n` _bytes_. The elements of the inner list are integers at most `2^n`, representing each smaller block of `n` bits. Because there are `n` bytes for each bigger block, there will always be 8 smaller blocks for each bigger block.
`m_vals` is just a flattened `m_val_list`, one giant list of small blocks.

On a broader scope, they use a repeated key for encryption, which we can exploit to find the flag.

### Solution

It might seem as if we lose information because we potentially cut off a bit of information during the addition, but the cryptography is actually uniquely reversible. Here is how we reverse a block of ciphertext given the corresponding block of either plaintext or key:
Let c be the ciphertext block, and let m be the known block.
If c > m,  
	then return c - m
else
	return c + 2^(n) - m

The idea is that if the original addition of the key and message overflowed, then we should be able to tell by checking if the output ciphertext is less than any of the inputs and thus we can compensate.
here is python code for reversing a block

``` python
def reverse(c, p, n):
	return c-p if c >= p else c + (1<<n) - p
```

We know the first 5 characters of the message must be `flag{`. Using this, we can figure out the first few characters of the key. To do this, however, we also need to know n. Fortunately, there are less than 8 possible values for n, so we can just try them all.
Here is code to find the first n characters of the key for each n

``` python
for n in range(2, 8):
	c_vals = []
	p_vals = []
	c_val_list = [get_vals(x, n) for x in get_nums(c, n)]
	for lst in c_val_list: c_vals += lst

	prefix = 'flag{_________'
	p_val_list = [get_vals(x, n) for x in get_nums(prefix, n)]
	for lst in p_val_list: p_vals += lst

	key = [reverse(c_vals[i], p_vals[i],n) for i in range(8) ]
	print(n, "".join([get_chrs(lst, n) for lst in [key[0:8]]]))
```

Unfortunately, the output shows that the key does not have any plaintext english

```
	(2, 'ns')
	(3, '>\xb3\xbc')
	(4, '*3|!')
	(5, '"s|\xa5\x7f')
	(6, '\x1e3\xbc%o\x9b')
	(7, '\x1a3|!\x7f\x9b\xb7')
```

But we can still use the fact that the key is repeated to figure out some more of the message.
Since we don't know the length of the key, we just try xoring the start of the key that we figured out with every position and then look for plaintext.
```python
for n in range(2, 8):
	c_vals = []
	p_vals = []
	c_val_list = [get_vals(x, n) for x in get_nums(c, n)]
	for lst in c_val_list: c_vals += lst

	prefix = 'flag{_________'
	p_val_list = [get_vals(x, n) for x in get_nums(prefix, n)]
	for lst in p_val_list: p_vals += lst

	key = [reverse(c_vals[i], p_vals[i],n) for i in range(8) ]
	for j in range(0,len(c_vals) - 8):
		pt = [reverse(c_vals[i+j], key[i],n) for i in range(8)]
		print(get_chrs(pt,n))
	print(n, "".join([get_chrs(lst, n) for lst in [key[0:8]]]))
```

The output looks something like this (its very long so I cut off sections of it):
```
fl
Σ
∩Ä
╔ä
q«

...

...
$i
∞1
╧P
H▀
(2, 'ns')
fla
ΩMp
        Eε
...

...
╤ ╨
F╪∞
φíï
(3, '>\xb3\xbc')
flag
∩╩ll
...

```

What we find is that its almost all garbage, except for `n=3`, where every 16 positions, we see some reasonable characters:

```
fla
...

...
x0r
...

...
_Ad
...

...
10n
...

...
D-2
...

...
U+_
...

...
5_W
...

...
m0d
```

This looks very much like a flag, so we know we're on the right track.

Since `n=3`, the python code I wrote above only gave the first 3 bytes of the key, ``>\xb3\xbc``, but we know the first 5 bytes of plaintext must be `flag{`. So next I added these last two characters to the key

```python
def convert1(str, n):
	return [get_vals(x, n) for x in get_nums(str, n)]
def de_block(c,m,n):
	return get_chrs([reverse(a,b,n) for a,b in zip(c,m)],n)

def decrypt(c,k,n):
	c_val_list = [get_vals(x, n) for x in get_nums(c, n)]
	c_vals = []
	for lst in c_val_list: c_vals += lst

	k_val_list = [get_vals(x, n) for x in get_nums(k, n)]
	k_vals = []
	for lst in k_val_list: k_vals += lst

	o_vals=[]
	for i in range(len(c_vals)):
		o_vals += [reverse(c_vals[i], k_vals[i%len(k_vals)], n)]

	o_val_list= [o_vals[i:i+8] for i in range(0, len(o_vals), 8)]
	return "".join([get_chrs(lst, n) for lst in o_val_list])

def guess(c, i, str, n):
	return de_block(convert1(c,n)[i//3], convert1(str,n)[0], n)

guess(c,3,"g{_",3)
```

The last call to guess gives some more characters of the key

```python
decrypt(c,'>\xb3\xbc%\xe1\xa3',3)
```

gives us

```python
"flag{_x0r_iV_Add1L10n-mQD-2,'\x83U+_+hR5_Wa5\xb8m0d=8\x9e"
```

The flag looks almost complete, except every 6th character is wrong. We can figure out the last character of the key by guessing any missing part of the flag:

```python
guess(c,7*3,"-m0",3)
```

returns

```python
'%\xe1\xc4'
```

for the second half of the key.

Putting it all together,

```python
decrypt(c,'>\xb3\xbc%\xe1\xc4',3)
```

gives us

```python
"flag{>x0r_i5_Add1+10n-m0D-2,'bU+_+h15_Wa5_m0d=8}"
```
