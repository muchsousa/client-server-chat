import socket
import sys
from datetime import datetime

import threading

import support.tlv as tlv
class ChatClient():
    def __init__(self, conn, addr, clients):
        self.conn = conn
        self.addr = addr
        self.clients = clients
        self.username = ""

    def handler(self):
        try:
            while self.conn is not None:
                raw_message = self.conn.recv(2048).decode("utf-8")

                if raw_message:
                    print(f"<{self.addr}> :: raw message :: {raw_message}")

                    decoded_message = tlv.decode_tlv(raw_message)

                    print(f"<{self.addr}> :: decoded message :: {decoded_message}")

                    if (decoded_message["type"] == "command"):
                        command = decoded_message["value"] or ""
        
                        # @ORDENAR: mostra as últimas 15 mensagens, ordenadas pelo horário de envio
                        if command == "@ORDENAR":
                            print(f"<{self.addr}> :: command :: @ORDENAR")

                        # @SAIR: faz "logout" do cliente
                        elif command == "@SAIR":
                            print(f"<{self.addr}> :: command :: @SAIR")
                            self.close_socket()

                        # @LOGIN: faz "login" do cliente
                        elif command == "@LOGIN":
                            print(f"<{self.addr}> :: command :: @LOGIN")

                            self.username = decoded_message["username"]
                            self._broadcast_message(raw_message)
                            
                        # @UPLOAD: faz upload de um arquivo para o servidor
                        elif command == "@UPLOAD":
                            print(f"<{self.addr}> :: command :: @UPLOAD")
                            

                        # @DOWNLOAD: faz download de um arquivo do servidor
                        elif command == "@DOWNLOAD":
                            print(f"<{self.addr}> :: command :: @DOWNLOAD")


                        else:
                            print("Command unknown")

                    # broadcast message
                    if (decoded_message["type"] == "message"):
                        self._broadcast_message(raw_message)

        except Exception as ex:
            print("#ChatClient.handler - Error: ", ex)
            # raise ex
        finally:
            self.close_socket()

    def close_socket(self):
        if self.conn is not None:
            self.conn.close()

        self.conn = None        

        # broadcast the logout
        datetime_message = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logout_message = tlv.encode_tlv({
            "type": "command",
            "datetime": datetime_message, 
            "username": self.username, 
            "value": "@SAIR"
        })
        self._broadcast_message(logout_message)

    def send_message(self, message):
        try:
            if message and self.conn is not None:
                self.conn.send(message.encode("utf-8"))
        except Exception as ex:
            print("#ChatClient.send_message - Error: ", ex)

    def _broadcast_message(self, message):
        for client in self.clients:
            if (client.addr == self.addr): continue

            print(f" > broadcast message from <{self.addr}> to <{client.addr}> :: {message}")
            client.send_message(message)

# --------------------------------------------------------------------------------------------------------------------

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
