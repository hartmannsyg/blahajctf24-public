from math import lcm
from hashlib import sha256
from Crypto.Cipher import AES
from sympy.ntheory.modular import crt

def get_order(x):
    visited = [False for _ in range(len(x))]
    cycles = []
    lu = {}
    cptr = 0
    for i in range(len(x)):
        if visited[i]:
            continue
        ptr = i
        cnt = 0
        cycle = []
        while not visited[ptr]:
            cycle.append(ptr)
            lu[ptr] = cptr 
            visited[ptr] = True
            ptr = x[ptr]-1
            cnt += 1
        cycles.append(cycle)
        cptr += 1
    return lcm(*(len(i) for i in cycles)), cycles, lu


def dlog(m, c):
    order, cycles, _ = get_order(m)
    mods, rems = [], []
    for cycle in cycles:
        st = m.index(cycle[0] + 1) # 1 index
        en = c[st] - 1 # convert back to 0 index
        mods.append(len(cycle))
        rems.append(cycle.index(en) + 1)
    return crt(mods, rems)[0], order

def mul(x, k):
    order, cycles, lu = get_order(x)
    k %= order
    out = []
    for i in x: # bottleneck
        cycle = cycles[lu[i-1]]
        val = cycle[(k - 1 + cycle.index(i-1)) % len(cycle)] + 1 # k - 1 as k = 1 means nothing should happen
        out.append(val) 
    return out

def compose(x, y):
    out = [y[i-1] for i in x]
    # 0 -> i (via x)
    # i -> yi (via y)
    return out

from sage.all import load

ge = 0x10001
out = load('out.sobj')
GM, GC, enc = out["GM"], out["GC"], out["enc"]
GN = out["GN"]
GNinv = mul(GN, -1)
GM = compose(GNinv, GM)
GC = compose(GNinv, GC)

ke, mod = dlog(GM, GC)
k = ke * pow(ge, -1, mod) % mod

while k.bit_length() < 65:
    flag = AES.new(sha256(str(k).encode()).digest()[:16], AES.MODE_ECB).decrypt(bytes.fromhex(enc))
    print(k, flag)
    k += mod
"""
2291931459088364897 b'\xcbv\x945b\xc9\xb8s\x0f\xb9\xfa\xbe3I\x88\xca\xb7D\xee\n\x02\x01?\x88\x8c\x85\xe1\xc6\xc8Ged"\x02ri[\'\xda\x16U\x08M\xe9\xee\x0b{,'
8848144183718607857 b'blahaj{gr0ups?_iT5_alL_aBout_tH3_cYCL35!}\x07\x07\x07\x07\x07\x07\x07'
15404356908348850817 b'3u\x7f{\xda`B2z\xddm\xe7I\xb8\x85\x0feg-6E\x0c\xeb\x037\xfd\xdb|\xb9t"#}\x15)\x85?\xc2r\x99\xb1]\xfe\n\xacK\xe9*'
"""