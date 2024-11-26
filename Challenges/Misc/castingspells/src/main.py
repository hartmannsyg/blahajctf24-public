#!/usr/local/bin/python

import os
from numpy import zeros, array, array_equal
import time

FLAG = "blahaj{impr3ss1ve_m4na_f3rn}"
PALETTE = " .o+=*BOX@%&#/^SE"

def main():
    hashbytes = os.urandom(16)    
    matrix = drunken_bishop(hashbytes)
    while matrix is None:
        hashbytes = os.urandom(16)
        matrix = drunken_bishop(hashbytes)
        
    print("Casting the Goddess's magic", end="", flush=True)
    
    for _ in range(3):
        time.sleep(1)
        print(".", end = "", flush=True)
    
    print()
    print()
    print(":".join([format(i,'02x') for i in hashbytes]))
    print()
    print_matrix(matrix)

    print()
    s = input("Your colliding counter spell: ")
    s = bytes([int(x, 16) for x in s.split(":")])
    
    if s == hashbytes:
        print("\n//(´⌯ ̫⌯`)\\\\ You've gotta try harder than that!")
        return

    print()
    matrix2 = drunken_bishop(s)
    print_matrix(matrix2)
    print()

    if array_equal(matrix, matrix2):
        print("\nImpressive work!")
        print(FLAG)
    else:
        print("\n//(´⌯ ̫⌯`)\\\\ You've gotta try harder than that!")


def drunken_bishop(hashbytes):
    matrix = zeros((9,17)).astype(int)
    a = []
    p = (4, 8)
    b = False
    mov = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for c in hashbytes:
        for _ in range(4):
            d = c & 0x3
            m = mov[d]
            p = (min(8, max(0, m[0]+p[0])), min(16, max(0, m[1]+p[1])))
            matrix[p] += 1 
            a.append(p)
            if matrix[p] > 1 and not b:
                for i in range(len(a)):
                    if a[i] == p and a[i+1:-1][::-1] != a[i+1:-1]:
                        b = True
            c >>= 2
    if not b:
        return None
    matrix[(4,8)] = 15
    matrix[p] = 16
    return matrix

def print_matrix(matrix):
    print("+---[blahajctf]---+")
    for line in matrix:
        print(f"|{''.join([PALETTE[i] for i in line])}|")
    print("+---[blahajctf]---+")

if __name__ == "__main__":
    main()
