import base64, string
from pwn import *
p = remote("localhost", 8000)
r = []
for x in range(2000):
    p.sendlineafter(b"Command:", b"getflag")
    p.recvuntil(b"is: ")
    a = p.recvline().strip().decode()
    r.append(a)
    print(a, x)
p.close()

keys = []
for x in r:
    keys.append(base64.b64decode(x.encode()).decode("charmap"))

for x in range(len(keys[0])):
    used = list(set([(ord(a[x])) for a in keys]))
    a = [i for i in range(256) if i not in used and (i > 31 and i < 127)]
    if len(a) == 1:
        print(chr(a[0]), end = "")
    else:
        print([chr(b) for b in a])