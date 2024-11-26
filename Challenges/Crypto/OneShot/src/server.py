#!/usr/bin/env python3

import asyncio
import random

HOST, PORT = "0.0.0.0", 8000
FLAG = b"blahaj{N1K0_02_N1C0_807H_423_CU73_N4M35}"
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ23456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

welcome_screen = b"""Submit the next 100 random bits in newline separated format
Good luck, player!
"""

wait_prompt = b"Enter to continue."
guess_prompt = b"Submit your random bits: "
incorrect_text = b"Your guess was incorrect, it was %s.\n"
correct_text = b"Your guess was correct!\n"
success_text = b"All bits recovered! The world is saved: %s\n"


async def mutate(bits):
    bits = list(bin(bits)[2:])

    for _ in range(25):
        bits[random.randrange(0, len(bits))] = random.choice(CHARSET)

    return ("".join(bits) + "\n").encode()


async def read_until_newline(reader):
    return await read_until(reader, b"\n")


async def read_until(reader, stop_char):
    buffer = b""

    while True:
        single_byte = await reader.read(1)

        if not single_byte or single_byte == stop_char:
            return buffer

        buffer += single_byte


async def request_handler(
    reader: asyncio.transports.ReadTransport, writer: asyncio.transports.WriteTransport
):
    rand_gen = random.Random()
    conn_info = reader._transport.get_extra_info("peername")

    try:
        conn_ip, conn_port = conn_info

    except ValueError:
        print(f"Tried to unpack connecting address and failed, got {conn_info}")
        writer.close()
        return

    print(f"Connection from {conn_ip}:{conn_port}")

    try:
        writer.write(welcome_screen)
        writer.write(wait_prompt)
        await writer.drain()

        await read_until_newline(reader)

        for _ in range(2370):
            rand_num = await mutate(rand_gen.getrandbits(32))
            writer.write(rand_num)
            await writer.drain()

        print(f"Sent random numbers to {conn_ip}:{conn_port}")

        for _ in range(100):
            writer.write(guess_prompt)
            await writer.drain()

            actual_guess = str(rand_gen.getrandbits(32)).encode()

            guess = await read_until_newline(reader)

            if not guess:
                raise ConnectionResetError

            try:
                assert guess == actual_guess

            except (UnicodeError, AssertionError):
                writer.write(incorrect_text % (actual_guess))
                await writer.drain()
                writer.close()
                return

            else:
                writer.write(correct_text)

        else:
            print(f"Served flag {FLAG.decode()} to {conn_ip}:{conn_port}")
            writer.write(success_text % FLAG)
            await writer.drain()

    except (BrokenPipeError, ConnectionResetError):
        print(f"Client {conn_ip}:{conn_port} disconnected.")

    else:
        print(f"Disconnected client {conn_ip}:{conn_port}")
        await writer.drain()

    finally:
        writer.close()


async def main(host, port):
    server = await asyncio.start_server(request_handler, host, port)
    await server.serve_forever()


if __name__ == "__main__":
    print(f"Serving on {HOST}:{PORT}")
    asyncio.run(main(HOST, PORT))
