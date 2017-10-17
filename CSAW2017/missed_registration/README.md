# Missed Registration

### Forensics 150

We get a .pcap file with a bunch of HTTP POSTs. Doing a quick file dump in [NetworkMiner](http://www.netresec.com/?page=NetworkMiner) yeilds nothing interesting, so we move onto Wireshark.

Opening the first POST, we see form data. However the content length looks a little off. The packet size is approximately 900 bytes, but the form data doesn't seem to hold that much data.

Looking into the "raw" packet data, we find that there is an additional parameter in the packet that Wireshark is not parsing:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/CSAW2017/missed_registration/wireshark.png)

The parameter is named `x` and the data appears to be hex-encoded data. Doing a quick hex to ASCII conversion of the first 3 bytes yields `BM\x92`, which is the file header for a .bmp file.

We will use [scapy](http://www.secdev.org/projects/scapy/) to pull the data we want out of the packet, ignoring the packets that do not contain the extra parameter (not all POSTs contained the `x` parameter).

```python
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
```

We first open the pcap file, we then pull out all the sessions, then we go through all the packets in a session. If the packet contains the extra parameter, we pull out the parameter, and store it. After we are finished, we decode the hex into actual bytes, then write it to a file.

Flag:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/CSAW2017/missed_registration/output.bmp)

