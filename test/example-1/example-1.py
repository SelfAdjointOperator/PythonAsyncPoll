#!/usr/bin/env python3

import sys
import socket
import select
from pathlib import Path

import PythonAsyncPoll

# Coroutine 1

def get_char_1(coroutine: PythonAsyncPoll.Coroutine):
    coroutine.await_fd(sys.stdin.fileno(), select.POLLIN) # wait for stdin data

def get_char_2(coroutine: PythonAsyncPoll.Coroutine):
    print("stdin ready")

    c = sys.stdin.read(1)
    print(f"c={c}")

# Coroutine 2

def get_socket_char_1(coroutine: PythonAsyncPoll.Coroutine):
    server_path = Path(__file__).parent / "test.socket"
    server_path.unlink(missing_ok = True)

    server = socket.socket(family = socket.AF_UNIX)
    server.bind(f"{server_path}")
    server.listen()

    setattr(coroutine.coroutine_locals, "server", server)
    coroutine.await_fd(server.fileno(), select.POLLIN) # wait for connection

def get_socket_char_2(coroutine: PythonAsyncPoll.Coroutine):
    print("server socket ready")
    server: socket.socket = getattr(coroutine.coroutine_locals, "server")

    client, _ = server.accept()
    server.close()

    setattr(coroutine.coroutine_locals, "client", client)
    coroutine.await_fd(client.fileno(), select.POLLIN) # wait for client data

def get_socket_char_3(coroutine: PythonAsyncPoll.Coroutine):
    print("client socket ready")
    client: socket.socket = getattr(coroutine.coroutine_locals, "client")

    c = client.recv(1)
    print(f"c={c}")
    client.shutdown(socket.SHUT_RDWR)
    client.close()

def main() -> None:
    event_loop = PythonAsyncPoll.EventLoop([
        PythonAsyncPoll.Coroutine([get_char_1, get_char_2]),
        PythonAsyncPoll.Coroutine([get_socket_char_1, get_socket_char_2, get_socket_char_3])
    ])

    event_loop.run()

if __name__ == "__main__":
    main()
