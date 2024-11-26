# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 22:00:55 2024

@author: User
"""
def get_piece_position(piece, pieces):
    for v in range(len(pieces)):
        for h in range(len(pieces[0])):
            if np.array_equal(pieces[v][h], piece):
                return (v,h)
    print("No piece found!")
    return (-1,-1)
        
import cv2
import numpy as np

image = cv2.imread('menu.jpg')
image2 = cv2.imread('puzzle.png')
piece_width = image.shape[1] // 12
piece_height = image.shape[0] // 16
startx = image.shape[1] // 6
originalpieces = [[None for j in range(8)] for i in range(16)]
scrambledpieces = [[None for j in range(8)] for i in range(16)]
halfscrambled = [[None for j in range(8)] for i in range(16)]
flagmodulus = [[None for j in range(8)] for i in range(32)]
flag = ""
for i in range(16):
    for j in range(8):
        originalpieces[i][j] = image[i * piece_height:(i+1) * piece_height, startx + j * piece_width:startx + (j+1) * piece_width]
        scrambledpieces[i][j] = image2[i * piece_height:(i+1) * piece_height, startx + j * piece_width:startx + (j+1) * piece_width]
#horizontal correcting
for v in range(8):
    positions = [0,1,2,3,4,5,6,7]
    for h in range(8):
        newh = get_piece_position(originalpieces[v][h], scrambledpieces)[1]
        halfscrambled[v][newh] = originalpieces[v][h]
        flagmodulus[23-v][h] = positions.index(newh)
        positions.remove(newh)
for v in range(8):
    positions = [0,1,2,3,4,5,6,7]
    for h in range(8):
        newh = get_piece_position(originalpieces[v+8][h], scrambledpieces)[1]
        halfscrambled[v+8][newh] = originalpieces[v+8][h]
        flagmodulus[31-v][h] = positions.index(newh)
        positions.remove(newh)
        
        
#vertical correcting
for h in range(8):
    positions = [0,1,2,3,4,5,6,7]
    for v in range(8):
        newv = get_piece_position(halfscrambled[v][h], scrambledpieces)[0]
        flagmodulus[15-h][v] = positions.index(newv)
        positions.remove(newv)
for h in range(8):
    positions = [0,1,2,3,4,5,6,7]
    for v in range(8):
        newv = get_piece_position(halfscrambled[v+8][h], scrambledpieces)[0]
        flagmodulus[7-h][v] = positions.index(newv-8)
        positions.remove(newv-8)

#flag extraction
for i in range(32):
    for j in range(128):
        correct = True
        for k in range(8):
            if j % (8-k) != flagmodulus[i][k]:
                correct = False
                break
        if (correct):
            flag += chr(j)
            break
print(flag)
        
        
        