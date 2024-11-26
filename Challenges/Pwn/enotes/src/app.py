import socket
import os
import select
import subprocess
import signal
import sys
import psutil


def handle_client(client_socket):
    # Create a new process
    conns = [x.laddr.port for x in psutil.net_connections()]
    port = 8001
    while port in conns:
        port += 1
        if port > 8400:
            client_socket.sendall(b"Too many connections! Please contact an admin, or come back later")
            client_socket.close()
            return
    process = subprocess.Popen(
        ['./enotes', str(port)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )

    while True:
        # Wait for data from either the client or the process
        readable, _, _ = select.select([client_socket, process.stdout, process.stderr], [], [])

        for source in readable:
            if source == client_socket:
                # Data from client
                data = client_socket.recv(1024)
                if not data:
                    # Client disconnected
                    process.terminate()
                    return
                # Send data to process
                process.stdin.write(data)
                process.stdin.flush()
            elif source in [process.stdout, process.stderr]:
                # Data from process
                output = source.read(1024)
                if not output:
                    # Process ended
                    client_socket.close()
                    return
                # Send output to client
                client_socket.sendall(output)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 8000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        
        # Fork a new process to handle the client
        pid = os.fork()
        if pid == 0:  # Child process
            server_socket.close()
            handle_client(client_socket)
            sys.exit(0)
        else:  # Parent process
            client_socket.close()

if __name__ == "__main__":
    main()