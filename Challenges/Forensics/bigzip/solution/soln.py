import zipfile
import io

with open("r.zip", "rb") as f:
    file_bytes = f.read()
while True:
    if file_bytes.startswith(b"PK\x03\x04\x14\x00\x00\x00\x08\x00"): #hunt for deflates
        zfile = zipfile.ZipFile(io.BytesIO(file_bytes), "r")
        print(zfile.infolist(), len(file_bytes))
        file_bytes = zfile.read(zfile.infolist()[0])
    else:
        file_bytes2 = file_bytes[35000:][:-73000] #blast away stores 1000 at a time
        if len(file_bytes2) == 0: #we found the flag, hit the end of the chain
            zfile = zipfile.ZipFile(io.BytesIO(file_bytes), "r")
            print(zfile.infolist(), len(file_bytes))
            file_bytes = zfile.read(zfile.infolist()[0])
            print("FLAG:", file_bytes)
            break
        file_bytes = file_bytes2