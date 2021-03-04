import socket
import threading
import select
import os

IP = "127.0.0.1"
PORT = 8001
messages = list()


def server(name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((IP,PORT))
        sock.listen(1)
        print("Server wait for connection...")
        conn, addr = sock.accept()
        client_name = conn.recv(1024).decode("UTF-8")
        print(f"{client_name} connected")
        conn.send(name.encode("UTF-8"))
        sock.close()
        return True, addr
    except:
        return False, None


def client(name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP,PORT))
    sock.send(name.encode("UTF-8"))
    server_name = sock.recv(1024).decode("UTF-8")
    print(f"Connected to {server_name}")
    addr = sock.getsockname()
    sock.close()
    return addr


def recv(s: socket.socket):
    while 1:
        msg = s.recv(1024).decode("UTF-8")
        messages.append(msg)
        display_message_history(messages)


def send(s: socket.socket, send_addr, name):
    while 1:
        message = input()
        mess = f"{name}: {message}"
        s.sendto(mess.encode("UTF-8"),send_addr)
        messages.append(mess)
        display_message_history(messages)


def display_message_history(messages):
    os.system("clear")
    for message in messages:
        print(f"{message}")


name = input("Input your name: ")
receive_addr = (IP, PORT)
result, send_addr = server(name)
if result is False:
    send_addr = receive_addr
    receive_addr = client(name)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(receive_addr)

receive = threading.Thread(target=recv, args=[s])
send = threading.Thread(target=send, args=[s,send_addr,name])

receive.start()
send.start()
receive.join()
send.join()