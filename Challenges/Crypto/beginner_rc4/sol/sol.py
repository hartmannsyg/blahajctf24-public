ct = [83, 103, 109, 44, 99, 106, 98, 96, 32, 104, 122, 43, 96, 97, 107, 102, 101, 105, 124, 110, 56, 106, 127, 80, 99, 56, 102, 53, 94, 121, 57, 119, 119, 82, 127, 125, 62, 113, 102, 88, 58, 105, 51, 118, 93, 117, 52, 95, 121, 48, 109, 54, 113, 105, 115, 35, 116]

# The plaintext is xored with stream
# s0, S1, S2, S3, ..., S14, S15, S0, SS1, SS2, ...
# where s is the initial 8-state,
# S is the result of genstream(s, s)
# SS is the result of genstream(S, S)
# We can recover S, then use it to generate the remaining xorstream to recover the flag!

def RC4_KeySchedule(key, S):
    j = 0
    for i in range(len(key)):
        j = (j + S[i] + key[i]) % 16
        S[i], S[j] = S[j], S[i]
    return S

known_ptxt = b"he flag is blaha"
S = [i^j for i,j in zip(known_ptxt, ct[1:17])]
S = [S[-1]] + S[:-1]

flag = "T" + known_ptxt.decode()
for i in range(17, len(ct)):
    if i % 16 == 1:
        S = RC4_KeySchedule(S, S)
    flag += chr(S[i % 16] ^ ct[i])
print(flag)
# The flag is blahaj{d0nt_m4k3_y0ur_st4te_4a5y_t0_r3c0ver!}