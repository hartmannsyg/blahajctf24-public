import os
import subprocess
import base64
import socket
import threading
import uuid
import time, random

def compile_and_encode():
    # Write C code to file
    c_code = r'''
#include <stdio.h>
asm(".fill %d, 1, 0x90");
void win(){
    printf("HACK SUCCESS\n");
    _exit(0);
}
int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    char buf[%d];
    gets(buf);
}
''' % (random.randint(0, 1000), random.randint(50, 800))
    nm = "/tmp/"+str(uuid.uuid4())
    with open(nm+'.c', 'w') as f:
        f.write(c_code)

    subprocess.run(['gcc', nm+'.c', '-o', nm, '-no-pie'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    with open(nm, 'rb') as f:
        program_data = f.read()

    encoded_program = base64.b64encode(program_data).decode() + "\n"

    return encoded_program, nm

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    conn.sendall(b"30 programs. 60 seconds. Are you ready to hack them all? (y/n)\n")
    if not b"y" in conn.makefile("rb").readline():
        conn.sendall(b"Ok bye\n")
        conn.close()
        return
    t0 = time.time()
    for i in range(30):
        if time.time() - t0 > 60:
            conn.sendall(b"Woah, too slow! Try harder...\n")
            conn.close()
            return
        encoded_program, nm = compile_and_encode()
        conn.sendall(encoded_program.encode())
        conn.sendall(b"Program %d of 30\n" % (i + 1))
        data = conn.makefile("rb").readline()
        if not data:
            break
        process = subprocess.run(
            nm,
            input=data,
            capture_output=True
        )
        if b"HACK SUCCESS" in process.stdout:
            conn.sendall(b"Hacked! Next one...\n")
        else:
            conn.sendall(b"You lose!!! Try harder...\n")
            conn.close()
            return
    else:
        if time.time() - t0 > 60:
            conn.sendall(b"Woah, too slow! Try harder...\n")
            conn.close()
            return
        conn.sendall(b"Congrats, you hacked 30 programs in %f seconds! Have a flag: blahaj{I_4M_s0_Sp33d}\n" % (time.time() - t0))
        conn.close()

def run_server():
    HOST = '0.0.0.0'
    PORT = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    run_server()
