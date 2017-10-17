import codecs
from scapy.all import *

pcap = rdpcap("cap.pcap")

sessions = pcap.sessions()

output = ""

for k in sessions:
    session = sessions[k]
    for packet in session:
        try:
            if(b"&x=" in packet.load):
                s = packet.load.decode("utf-8")
                output += s[s.find("&x=")+3:]
        except AttributeError:
            pass

output = codecs.decode(output, "hex")

with open("output.bmp", "wb") as f:
    f.write(output)
