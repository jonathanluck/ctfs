from PIL import Image
import binascii

def c(n):
    return ((hex(n)[2:]).zfill(2))

def hexpix(p):
    out = ""
    out += c(p[0])
    out += c(p[1])
    out += c(p[2])
    return out


byte = ""


with Image.open("pretty_pixels.png") as img:
    width, height = img.size
    for y in range(0,height):
        for x in range(0,width):
            d = img.getpixel((x,y))
            byte+= hexpix(d)

open("pretty_pixels_out.png",'wb').write(binascii.unhexlify(byte))

