import socket
import sys

# https://docs.python.org/3/library/threading.html
import threading


class ChatClient():
    def __init__(self, conn, addr, clients):
        self.conn = conn
        self.addr = addr
        self.username = f"<{self.addr}>"
        self.clients = clients

    def handler(self):
        client_connected = self.conn is not None

        try:
            while client_connected:
                message = self.conn.recv(2048).decode("utf-8")

                if message:
                    print(f"{self.username} :: {message}")

                    # broadcast message
                    self._broadcast_message(message)
                else:
                    self.client_connected = False

        except Exception as ex:
            print("ERROR: ", ex)

        self.conn.close()

    def send_message(self, message):
        try:
            if message:
                self.conn.send(message.encode("utf-8"))
        except Exception as ex:
            print("#send_message - ERROR: ", ex)
       

    def _broadcast_message(self, message):
        for client in self.clients:
            if (client.addr == self.addr):
                continue

            print(f" > broadcast message = {self.username} :: {message}")
            client.send_message(message)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', port))

server.listen(5)

clients = []
running = True
while running:
    conn, addr = server.accept()

    client = ChatClient(conn, addr, clients)
    threading.Thread(target=client.handler, args=()).start()

    clients.append(client)


server.close()
