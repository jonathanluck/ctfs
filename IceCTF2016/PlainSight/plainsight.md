#Plain Sight

### Reversing

We get a binary file that doesn't seem to do anything. However when we put it into a disassembler and take a look at `main`,  we see values being repeatedly moved into the `al` register:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/IceCTF2016/PlainSight/plainsight.png)

Those hex values correspond to printable hex characters. We can translate them into a string with the following:
```Python
print("".join([chr(c) for c in [0x49, 0x63, 0x65, 0x43, 0x54, 0x46, 0x7b, 0x6c, 0x6f, 0x6f, 0x6b, 0x5f, 0x6d, 0x6f, 0x6d, 0x5f, 0x49, 0x5f, 0x66, 0x6f, 0x75, 0x6e, 0x64, 0x5f, 0x69, 0x74, 0x7d]]))
```

Running that yields the flag: `IceCTF{look_mom_I_found_it}`
