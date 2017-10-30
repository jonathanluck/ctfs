# ECB

### Cryptography(/Forensics?)

We are given two files, [img1](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img1.png) and [img2](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img2.png). We are told only that the images were encrypted using ECB mode.

#### Making some assumptions and educated guesses
First of all, we are not given any info about how the images themselves were actually encrypted. However looking at the images, the pixels look pretty random, giving the impression that RGBA (color and transparency) values were simply turned into bytes, then encrypted. This is supported by the fact that the images themselves are in tact and readable (i.e. the file headers/metadata/checksums/IDATs were not encrypted). This is also supported with recent experience in performing the same type of encryption on images, and with my results looking very similar to these given images.

Second of all, we can guess that this problem isn't going to involve recovering a key or any actual plain text. This is indicated by the fact that we don't have an arbitrary encryption oracle, and we don't have any plaintext data.

Additionally, we can guess that the two images are related in some way, mostly because it would be pointless to give us two images if only one would yield the flag.

Given these three guesses/assumptions, we can make one last guess. Because ECB's main weakness is that the same plaintext deterministically is encrypted to become the same ciphertext, we are probably looking for chunks of repeat data. Given that we are working with images, the repeated ciphertext blocks probably form some visual pattern (hopefully a flag).

#### Solving the problem
1. We need to break down the images into chunks of `blocksize`
2. We need to see which blocksize yields the most number of identical ciphertext blocks
3. We want to visualize the identical ciphertext blocks

#### Breaking the image down into chunks

For this, we will use Python, specifically, Python Image Libary (Pillow since I write code in Python 3).

We can actually just load up the image and use the `tobytes` function to turn the RGBA values directly into bytes:

```python
>>> from PIL import Image
>>> img = Image.open("img1.png")
>>> b = img.tobytes()
>>> len(b)
1088000
>>> b[:10]
b'\x02w\x95\x92\xcb\n\xb6\xfc<<'
>>>
```

#### Finding the block size

Because we are looking for repeated blocks, we want to find the block size with the maximum number of repeated blocks. We can use the `collections.Counter` to handle the dirty implementation of counting and maxing.

```python
>>> from collections import Counter
>>> c = Counter()
>>> for i in range(0,len(b), blocksize):
...   c.update([b[i:i+blocksize]])
```

We have to wrap the slice of the bytes in a list, otherwise the Counter would iterate over the individual bytes instead of treating the entire slice as a single object.
 `blocksize` is a variable that we can change. Based on the divisibility of the number of bytes in the image, we can guess 3 potential block sizes: 64, 128, and 256 bits.
 
This next part is a bit of guess and check. 
 
Guessing an incorrect block size means that we likely won't have many (or any) ciphertext blocks that repeat. For example, guessing a block size of 128 bits on img2.png:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img_2_128bit.png)

Notice how there isn't a single most common block of ciphertext (the second number in each tuple is the number of times the byte stream appears in the image data)

After a bit of guessing and checking, we find correct block sizes: 128 bits for img1 and 64 bits for img2.

img1:
![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img_1_128bit.png)

img2:
![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img_2_64bit.png)

#### Visualizing identical ciphertext blocks

We can now take the most common ciphertext blocks and replace them with white pixels to visualize them:

```python
>>> out = Image.new("RGBA", img.size)
>>> most_freq = [i[0] for i in c.most_common(5)]
>>> out.frombytes(b"".join(map(lambda x: b"\xff"*blocksize if x in most_freq else x, (b[i:i+blocksize] for i in range(0,len(b),blocksize)))))
>>> out.save("img1_out.png")
```

This line `out.frombytes(b"".join(map(lambda x: b"\xff"*blocksize if x in most_freq else x, (b[i:i+blocksize] for i in range(0,len(b),blocksize)))))` simply replaces blocks with white pixels if they are identical to and of the 5 most frequent ciphertext blocks.

Doing this for both images yields some pretty interesting results:

img1:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img1_out.png)

img2:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/img2_out.png)

The white pixels (repeated ciphertext) are clustered in the center of both images, in patterns that make it look like we need to combine both images to read a flag.

#### Putting it all together

```python
from PIL import Image
from collections import Counter

def do_stuff(fname, outname, blocksize):

    a = Image.open(fname)
    b = a.tobytes()
    c = Counter()

    #get the most frequent encrypted vblocks
    for i in range(0,len(b), blocksize):
        c.update([b[i:i+blocksize]])

    
    out = Image.new("RGBA", a.size)
    most_freq = [i[0] for i in c.most_common(5)]

    #replace the 5 most frequent blocks with white pixels
    out.frombytes(b"".join(map(lambda x: b"\xff"*blocksize if x in most_freq else x, (b[i:i+blocksize] for i in range(0,len(b),blocksize)))))
    out.save(outname)
    return out

one = do_stuff("img1.png", "img1_out.png", 16)
two = do_stuff("img2.png", "img2_out.png", 8)

#combine the images. White pixels get turned into black pixels, and non-white get turned white
combined = Image.new("RGBA", one.size)
for x in range(one.size[0]):
    for y in range(one.size[1]):
        if(one.getpixel((x,y)) == (255,)*4 or two.getpixel((x,y)) == (255,)*4):
            combined.putpixel((x,y), (0,)*4)
        else:
            combined.putpixel((x,y), (255,)*4)
            
combined.save("combined.png")
```

The nested for loops at the end simply take any pixel that is non-white and makes it white (background) and takes the white pixels from either of the images and turns them black.

Doing so yields a flag of sorts:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/BackdoorCTF2017/ecb/combined.png)

We then do a SHA-256 of the flag to get the actual submission

```python
from hashlib import sha256
print(sha256(b'CTF{0n1y_n00b5_u53_3cb}').hexdigest())
```

Our submitted flag is `4c0c0dfc09e51ba49b04b8b48f1ccca3965cc6415ea6185e40c4804c7dab0649`
