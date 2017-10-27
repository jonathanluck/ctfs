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
