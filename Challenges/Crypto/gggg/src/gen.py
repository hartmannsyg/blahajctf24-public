from random import shuffle
from math import lcm

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


def mul(x, k):
    order, cycles, lu = get_order(x)
    k %= order
    out = []
    for i in tqdm(x): # bottleneck
        cycle = cycles[lu[i-1]]
        val = cycle[(k - 1 + cycle.index(i-1)) % len(cycle)] + 1 # k - 1 as k = 1 means nothing should happen
        out.append(val) 
    return out


def compose(x, y):
    out = [y[i-1] for i in x]
    # 0 -> i (via x)
    # i -> yi (via y)
    return out


from sage.all import random_prime, save
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm
from functools import reduce

gk = random_prime(2**64, 2**65)
g = 50000
ge = 0x10001

gp = list(range(1,g+1))
shuffle(gp)
gq = list(range(1,g+1))
shuffle(gq)

gn = compose(gp, gq)
gm = compose(compose(gp, gp), reduce(compose, [gq] * 17)) 
# 2,17 chosen as random element values. compose() is a lot faster than mul() if the scalar multiplier is small

gc = mul(gm, gk * ge)

ggm = compose(gn, gm) # for i in GN
ggc = compose(gn, gc) # for i in GN


flag = b'blahaj{gr0ups?_iT5_alL_aBout_tH3_cYCL35!}'
enc = AES.new(sha256(str(gk).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag,16)).hex()

out = {"GN":gn, "GM":ggm, "GC":ggc, "enc":enc}
save(out, "out.sobj")
print(gk)
print(get_order(gm)[0])
print(gm[:10])