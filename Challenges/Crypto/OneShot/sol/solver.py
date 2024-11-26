#!/usr/bin/env python3

# OwOverflow!

import string
import time

from pwn import *
from symbolic_mersenne_cracker import Untwister

CHARSET = string.ascii_letters + "23456789" + string.punctuation
CHARSET_MAP = {ord(x): "?" for x in CHARSET}

HOST, PORT = "127.0.0.1", 7000

p = remote(HOST, PORT)

p.recvuntil(b"Enter to continue.")
p.sendline()

corrupted_random_numbers = p.clean().decode().split("\n")[:-1]
random_numbers = []

for i in corrupted_random_numbers:
    random_numbers.append(i.translate(CHARSET_MAP))

t1 = int(time.time())
log.info("Got %i random numbers, solving them now.", len(random_numbers))

ut = Untwister()
for i in random_numbers:
    ut.submit(i)

r2 = ut.get_random()
t2 = int(time.time())

log.info("Found state in %i seconds", t2 - t1)

for _ in range(100):
    p.sendline(str(r2.getrandbits(32)).encode())
    resp = p.recvline()

    if b"Your guess was correct!" == resp:
        continue

p.readuntil(b"All bits recovered! The world is saved: ")
flag = p.clean().decode().strip()

log.success("We got the flag! %s", flag)
