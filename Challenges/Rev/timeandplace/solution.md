program logic:

- the UUID temp folders decode to an XOR'd shellcode
- each set of folders links to another set of folders through timestamp bytes at the start and end of each UUID (sort of like a linked list)
- program requires you to input a time (which would be the timestamp corresponding to the start of a shellcode chain) and a place (which would be the byte which the shellcode is XOR'd against)
- player should be able to determine how the program decodes the shellcode from the folders through static reversing
- player should be able to determine what the starting timestamp should be by working backwards (the end of each linked list is a folder without any subfolders, then chain backwards based on the indexes until you find a "front")
- byte that is XOR'd against the shellcode is equal to the last byte of the md5 hash of the whole shellcode
- when the correct time and place is inputted, a message box displaying a part of the flag pops up
- assuming the player figured out the logic, they should be able to replicate this process for the remaining parts (3 part flag totes)

if reversing is too hard, give them the PDB so they get symbols.

The following are the values required to print the flag:

Time: 1650135656
Place: 15

Time: 1689276985
Place: 251

Time: 1659450715
Place: 27

Flag: `blahaj{totally_legit_temp_folders_:333}`