# 22 Dec 21

print("Imporint socket")
import socket
import message
import sys
from time import time

# message.Message().msg.append("pes12020101070")

def begin():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # IP_address = "175.198.42.211"
    port = 8080

    server.bind(("", port))
    server.listen(1) # Limiting the maximum connections to a clients per server

    client, addr = server.accept()
    print(client, addr)

    last_check = time()

    while True:
        if time() - last_check >= 60:
            last_check = time()
            try: 
                client.send("TEST".encode())
            except Exception as e:
                print("Inside Exception block 2")
                server.close()
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
                server.bind(("", port))
                server.listen(1) # Limiting the maximum connections to a clients per server

                client, addr = server.accept()
                print(client, addr)

        if len(message.Message.msg_prc) > 0:
            try:
                print(message.Message.msg_prc)
                if(message.Message.msg_prc[0] != "NOTIFY") & (message.Message.msg_prc[0] != "OVERRIDE"):
                    print("Opening the Door")
                    client.send("OPEN".encode())
                elif message.Message.msg_prc[0] == "OVERRIDE":
                    print("OVERRIDE WARNING")
                    client.send("OVERRIDE".encode())
                else:
                    print("NOTIFYING")
                    client.send("NOTIFY".encode())
                client.settimeout(5)
                print("Response:", client.recv(10).decode())
                message.Message.msg_prc.pop()
            except Exception as e:
                print(e)
        
        if message.Message.shut_down == True:
            client.send("SHUTDOWN".encode())
            print("Shutting down Server")
            server.close()
            print("EXITING: Web Server")
            break



# begin()