# AES Mess
###Cryptography

So we start with a huge file of plaintext/ciphertext combinations and a ciphertext flag. We are told that it was encryped with AES in [ECB mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29). 

The encryption algorithm itself isn't too interesting (all we care about is the block size). However the mode is how we are going to break this.

##### A short description of ECB mode and its weakness:
With some other modes of bock ciphers, the input key for the encryption algorithm is changed every block, or the output from the encryption algorithm is xored with something else. With ECB, the exact same key is being fed into the encryption algorithm every single block, and the output of the encryption algorithm is directly used as the ciphertext. This leads to the unfortunate result of the same plaintext blocks resulting in the exact same ciphertext blocks.

Example: Let's take a hypothetical block cipher `E` with block size of 4 bytes (32 bits). Let's say you know the first 4 bytes of input are `"abcd" ` and the corresponding 4 bytes of ciphertext are `"1234"`. Then you know that any time you see `"1234"` on a 4 byte alignment, the plaintext `"abcd"` was in that position in the plaintext.

##### Breaking this problem
So we know the block size (128 bits or 16 bytes), and we know the key was reused for every single ciphertext/plaintext combination. What we can do is search through the combinations for blocks of 16 bytes that correspond to 16 byte blocks of our ciphertext. Because they used the same key, that means the corresponding plaintext is the same plaintext of that block of our flag. 

To start: The first block of 16 bytes of the flag is `e220eb994c8fc16388dbd60a969d4953` (two hex chars correspond to one byte). We can search for the corresponding plaintext/ciphertext combination. We find it in the first half of the ciphertext of this line: `abctf{looks_like_gospel_feebly}:e220eb994c8fc16388dbd60a969d49536d896bd7d6da9c4ce3eac5e4832c2f64`. We extract the first 16 bytes (first 16 characters) of the plaintext and our flag starts out with: `abctf{looks_like`

We repeat the same procedure withe the next block of 16 bytes, yielding: `_you_can_break_a`

The last 16 bytes is a bit trickier. When we search through the plaintext/ciphertext combinations for the last 16 bytes of the flag, we get multiple results. Why? The answer is padding. Block ciphers only work on specific sizes of inputs. If the last block is not long enough, then it will be padded to reach the block size before being passed to the encryption function. 

Let's take this line `abctf{eocene_fazes}:b58b970036b3a521a314d06f1436863efafa1a7c21ff824a5824c5dc4a376e75` that matches the last block of the flag's ciphertext. We can't just take the last 16 bytes of this plaintext. Instead we can get rid of the first 16 bytes of the this plaintext, and the remaining is the plaintext before padding was applied. Doing so yields: `es}`

Putting it all together, we get the flag: `abctf{looks_like_you_can_break_aes}`
