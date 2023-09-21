import socket
import select
import sys
from datetime import datetime
import re
import threading

import support.tlv as tlv

def message_listener(socket):
    running = True
    while running:
        raw_message = socket.recv(2048).decode("utf-8")
        if raw_message == "":
            continue
    
        message = tlv.decode_tlv(raw_message)
        
        if (message["type"] == "message"):
            print(f"[{message['datetime']}] \N{ESC}[33m{message['username']}\u001b[0m :: {message['value']}")
        elif (message["type"] == "command"):
            command = message["value"]

            # @LOGIN: faz "login" do cliente
            if command == "@LOGIN":
                print(f"[{message['datetime']}] \N{ESC}[33m{message['username']}\u001b[0m :: \N{ESC}[3mjoined the chat\u001b[0m")

            # @SAIR: faz "logout" do cliente
            elif command == "@SAIR":
                print(f"[{message['datetime']}] \N{ESC}[33m{message['username']}\u001b[0m :: \N{ESC}[3mleft the chat\u001b[0m")

# ----------------------------------------------------------------

if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

print("What you username? ")
username = sys.stdin.readline().replace("\n", "")

# notify user login
datetime_message = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
tlv_message = tlv.encode_tlv({
    "type": "command",
    "datetime": datetime_message, 
    "username": username, 
    "value": "@LOGIN"
})
server.send(tlv_message.encode("utf-8"))

print("\n[Chat]\n")

# thread to listen messages
threading.Thread(target=message_listener, args=(server,)).start()

running = True
while running:
    message = sys.stdin.readline().replace("\n", "")

    is_command = re.search("(@[a-zA-Z]+)((.*).([a-z]{2,4}))?", message)

    datetime_message = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_type = "message" if is_command is None else "command"
    tlv_message = tlv.encode_tlv({
        "type": message_type,
        "datetime": datetime_message, 
        "username": username, 
        "value": message
    })

    server.send(tlv_message.encode("utf-8"))

    print(f"[{datetime_message}] \N{ESC}[32m{username} (you)\u001b[0m :: {message}")

server.close()
