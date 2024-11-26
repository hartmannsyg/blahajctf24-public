def insert(startpos, image1, image2, original, new, width, height):
    #insert a piece from the first image 
    #into another position in the second image
    image2[
        startpos[0] + new[0] * height:startpos[0] + (new[0]+1) * height,
        startpos[1] + new[1] * width:startpos[1] + (new[1]+1) * width
        ] = image1[
        startpos[0] + original[0] * height:startpos[0] + (original[0]+1) * height, 
        startpos[1] + original[1] * width:startpos[1] + (original[1]+1) * width
        ]
import cv2
import numpy as np

flag = "blahaj{????????????????????????}"
assert len(flag) == 32  

image = cv2.imread('menu.jpg')
piece_width = image.shape[1] // 12
piece_height = image.shape[0] // 16
startx = image.shape[1] // 6
image2 = image.copy()

#horizontal shuffling
for v in range(8):
    positions = [0,1,2,3,4,5,6,7]
    char = ord(flag[31-v])
    for h in range(8):
        newPos = positions[char % (8-h)]
        positions.remove(newPos)
        insert((0,startx),image, image2, (v+8,h), (v+8, newPos), piece_width, piece_height)
for v in range(8):
    positions = [0,1,2,3,4,5,6,7]
    char = ord(flag[23-v])
    for h in range(8):
        newPos = positions[char % (8-h)]
        positions.remove(newPos)
        insert((0,startx),image, image2, (v,h), (v, newPos), piece_width, piece_height)
image3 = image2.copy()


#vertical shuffling
for h in range(8):
    positions = [0,1,2,3,4,5,6,7]
    char = ord(flag[15-h])
    for v in range(8):
        newPos = positions[char % (8-v)]
        positions.remove(newPos)
        insert((0,startx),image2, image3, (v,h), (newPos, h), piece_width, piece_height)
for h in range(8):
    positions = [0,1,2,3,4,5,6,7]
    char = ord(flag[7-h])
    for v in range(8):
        newPos = positions[char % (8-v)]
        positions.remove(newPos)
        insert((0,startx),image2, image3, (v+8,h), (newPos+8, h), piece_width, piece_height)



cv2.imwrite("puzzle.png", image3)

    





