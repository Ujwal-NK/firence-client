from email import message_from_binary_file
import socket
import message
import json
import sys
import hashlib
import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.connect(("", 8060))

def start_comms():
    auth = True
    while auth:
        server.send(hashlib.md5((str(datetime.datetime.today())[:14]).encode()).hexdigest().encode())
        if server.recv(1024).decode() == "AUTH: OK":
            auth = False
        print("Authenticating")
    while True:
        try:
            if message.Message.msg_login['ID'] != "":
                print("Sending login ID", message.Message.msg_login)
                server.send(json.dumps(message.Message.msg_login).encode())
                data = server.recv(1024).decode()
                print("Recived message:", data)
                if ("AUTH_FAIL" != data) & (str(data).find("ERROR") == -1):
                    print("AUTH SUCCESS")
                    message.Message.auth = True
                    message.Message.msg_cls = data
                else:
                    message.Message.auth = False
                message.Message.reset()
                print("CLASS: ", message.Message.msg_cls)
                print("LOGIN: ", message.Message.msg_login)
        except Exception as e:
            if str(e).find("string") == -1:
                print(e)
            # message.Message().msg_class = ""

        # print("CLIENT.PY >> SRC", message.Message.msg_src)

        if len(message.Message.msg_src) > 0:
            print("Content present in source")
            try:
                # print("KEYS:", type(message.Message().msg_src[0].keys()), message.Message().msg_src[0].keys())
                # print("Sending value:", json.dumps({'ID': str(message.Messaprint(message.Message.student, "after appending", message.Message.msg_src[0][0].upper()), 'STATUS': message.Message().msg_src[0][1], 'CLASS': message.Message().msg_cls}).encode())
                # server.send(("+" + str(message.Message().msg_src[0])).encode())
                if len(message.Message().msg_src[0]) == 2:
                    server.send(json.dumps({'ID': str(message.Message().msg_src[0][0].upper()), 'STATUS': message.Message().msg_src[0][1], 'CLASS': message.Message().msg_cls}).encode())
                elif len(message.Message().msg_src[0]) == 4:
                    server.send(json.dumps({'ID': str(message.Message().msg_src[0][0].upper()), 'STATUS': message.Message().msg_src[0][1], 'CLASS': message.Message().msg_cls, "QUERY":message.Message().msg_src[0][2], "TEACHER": message.Message().msg_src[0][3]}).encode())
                student_name = server.recv(1024).decode()
                if(student_name != "INVALID"):
                    print(student_name)
                    if((student_name != "NOTIFY") & (student_name != "") & (student_name != "OK")):
                        message.Message.msg_prc.append(message.Message.msg_src[0])
                        print(message.Message.student, "appending", message.Message.msg_src[0])
                        message.Message.student[message.Message.msg_src[0][0]] = student_name
                        print(message.Message.student)
                        print("About to pop:", message.Message.msg_src)
                        message.Message.pop_msg_src()
                        print("After POPPED:", message.Message.msg_src)
                    elif (student_name == "NOTIFY"):
                        message.Message.msg_prc.append("NOTIFY")
                        message.Message.pop_msg_src()
                    elif (student_name == "OK"):
                        message.Message.pop_msg_src()
                else:
                    print("Invalid Key Error")
                    raise InvalidKeyError
            except InvalidKeyError:
                print("Invalid ID")
                message.Messag.pop_msg_src()
            except Exception as e:
                print(e)
                print("Unable to communicate to server, will try sending again")
            print("POPPED:", message.Message.msg_src)
            
    # except KeyboardInterrupt:
        if message.Message.shut_down == True:
            print("Shutting down Client")
            server.send("SHUTDOWN".encode())
            server.close()
            print("EXITING: Client")
            break

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidKeyError(Error):
    """Raised when the Key is Invalid"""
    pass

# start_comms()