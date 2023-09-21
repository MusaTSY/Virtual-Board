import socket
import threading

POST_MESSAGE_COMMAND = "POST:"
CHECK_MESSAGES_COMMAND = "CHECK:"
REMOVE_MESSAGE_COMMAND = "REMOVE:"
HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.34"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

POSTS = []


def handle_client(conn, addr):
    client_id = f"ID: {addr[0]}:{addr[1]}"
    print(f"[NEW CONNECTION] {client_id} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(
                FORMAT)  # conn.recv(HEADER) receives the message of size HEADER bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The value received is stored in msg_length
            if msg_length:
                msg_length = int(
                    msg_length)  # converts the msg_length from a string to an integer. The received message
                msg = conn.recv(msg_length).decode(
                    FORMAT)  # the server receives the actual message sent by the client. conn.recv(msg_length) receives the message of size msg_length bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The decoded message is stored in the variable msg.
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                elif msg.startswith(POST_MESSAGE_COMMAND):
                    message_content = msg[len(POST_MESSAGE_COMMAND):]
                    print(f"[POSTED] {client_id}: {message_content}")
                    POSTS.append((addr, message_content))
                    conn.send("Message is on Board".encode(FORMAT))
                elif msg.startswith(CHECK_MESSAGES_COMMAND):
                    messages = "\n".join([f"IP:{client[0]}-{content}" for client, content in POSTS])
                    conn.send(messages.encode(FORMAT))
                elif msg.startswith(REMOVE_MESSAGE_COMMAND):
                    message_content = msg[len(REMOVE_MESSAGE_COMMAND):]
                    removed = False
                    for client, content in POSTS:
                        if client == addr and content == message_content:
                            POSTS.remove((client, content))
                            removed = True
                            break
                    if removed:
                        conn.send("Message removed.".encode(FORMAT))
                    else:
                        conn.send("Message not found.".encode(FORMAT))
        except:
            break


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # get the obj of the current socket and addr get the list of the client
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # handle_client, which is responsible for handling communication with the connected client.
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
