import binascii

def to_num(s):
	x = 0
	for i in range(len(s)): x += ord(s[-1-i]) * pow(256, i)
	return x

def get_nums(s, n):
	sections = [s[i:i+n] for i in range(0, len(s), n)]
	sections[-1] = sections[-1] + ("\x00" * (n - len(sections[-1])))
	return [to_num(x) for x in sections]

def get_vals(x, n):
	vals = []
	mask = (1 << n) - 1
	for i in range(8):
		vals.append(x & mask)
		x = x >> n
	vals.reverse()
	return vals

def get_chrs(val_list, n):
	# print("GETCHR: ", val_list)
	x = val_list[0]
	chrs = []
	for i in range(1, len(val_list)):
		x <<= n
		x += val_list[i]
	#print("XXX: ", x)
	for i in range(n):
		chrs.append(chr(x % 256))
		x //= 256
	chrs.reverse()
	return "".join(chrs)

def encr_vals(m_chr, k_chr, n):
	return (m_chr + k_chr) & ((1 << n) - 1)

def encrypt(k, m, n):
	if (n >= 8): raise ValueError("n is too high!")
	rep_k = k * (len(m) // len(k)) + k[:len(m) % len(k)] # repeated key
	m_val_list = [get_vals(x, n) for x in get_nums(m, n)]
	k_val_list = [get_vals(x, n) for x in get_nums(rep_k, n)]
	m_vals, k_vals, c_vals = [], [], []
	for lst in m_val_list: m_vals += lst
	for lst in k_val_list: k_vals += lst
	c_vals = [encr_vals(m_vals[i], k_vals[i % len(k_vals)], n)
		for i in range(0, len(m_vals))]
	c_val_list = [c_vals[i:i+8] for i in range(0, len(c_vals), 8)]
	return "".join([get_chrs(lst, n) for lst in c_val_list])

# c='\xd2\x91\xd4[\x8casdfasdf'
c=binascii.unhexlify('809fdd88dafa96e3ee60c8f179f2d88990ef4fe3e252ccf462deae51872673dcd34cc9f55380cb86951b8be3d8429839')
def convert1(str, n):
	return [get_vals(x, n) for x in get_nums(str, n)]

def reverse(c, p, n):
	return c-p if c >= p else c + (1<<n) - p

for n in range(2, 8):
	c_vals = []
	p_vals = []
	c_val_list = [get_vals(x, n) for x in get_nums(c, n)]
	for lst in c_val_list: c_vals += lst

	# print(c_vals)

	prefix = 'flag{_________'
	p_val_list = [get_vals(x, n) for x in get_nums(prefix, n)]
	for lst in p_val_list: p_vals += lst

	# print(p_vals)

	key = [reverse(c_vals[i], p_vals[i],n) for i in range(8) ]
	# print(key)
	# for j in range(0,len(c_vals) - 8):
	# 	pt = [reverse(c_vals[i+j], key[i],n) for i in range(8)]
	# 	print(get_chrs(pt,n))
	# 	k_val_list2 = [key2[i:i+8] for i in range(0, len(key2), 8)]
		# print( "".join([get_chrs(lst ,n) for lst in k_val_list2]))
	# print("p: " , p_vals)
	# print("k: " , key)
	# print("c: " , c_vals)
	# print(get_chrs(c_vals,n))
	# print("p: ", get_chrs(p_vals,n))
	print(n, "".join([get_chrs(lst, n) for lst in [key[0:8]]]))


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
