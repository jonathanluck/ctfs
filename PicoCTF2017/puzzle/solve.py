import scapy.all as scapy


pcap = scapy.rdpcap("data-1.pcap")

sessions = pcap.sessions()

possible_keys = [k for k in list(sessions.keys()) if k.split(":")[0] == "TCP 10.0.0.1"]

def find_image(packets, fnumber):
    maxlen = 0
    for p in packets:
        maxlen = max(maxlen, p.len)
    if(maxlen > 3000):
        for i in range(len(packets)):
            try:
                l = packets[i].load
                if(l[:2] == b'\xff\xd8'):
                    image = b''
                    if(len(packets[i].load) > 8000):
                        image = packets[i].load + packets[i+1].load + packets[i+2].load
                    else:
                        image += packets[i].load
                        while(packets[i].load[-2:] != b'\xff\xd9'):
                            i += 1
                            image += packets[i].load
                    f = open("{}.jpg".format(fnumber), "wb")
                    f.write(image)
                    f.close()
                    return fnumber + 1
                elif(l[:2] == b'\x89\x50'):
                    image = b''
                    for j in range(10):
                        print(i,j)
                        try:
                            if(i + j < len(packets)):
                                image += packets[i+j].load
                        except:
                            pass
                    f = open("{}.png".format(fnumber), "wb")
                    f.write(image)
                    f.close()
                    return fnumber + 1
            except AttributeError:
                pass
                

i = 0
for k in possible_keys:
    if(find_image(sessions[k],i)):
       i += 1
       print(i, k)
