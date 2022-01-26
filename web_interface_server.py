import sys
import http.server
import socketserver
import message
import urllib
import hashlib
from io import BytesIO
import time
from PIL import Image
import threading


session = ""
session_login_id = ""

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler): 

    def do_GET(self):
        global session
        # Setting cookies to none
        self.cookie = None

        # Dictionary of routes
        routes = {
            "/"         : self.home,    # HOME   Page 
            "/logout"   : self.logout,  # LOGOUT URL
            "/login"    : self.login    # LOGIN  URL
        }

        # print("GET_PATH:", self.path)
        # print("HEADER:", self.parse_cookies(self.headers['Cookie']))

        # Checking if the user is logged in
        self.user = False
        response = 404
        try:
            if session == self.parse_cookies(self.headers['Cookie'])['SID']:
                # print("Found the session ID")
                self.user = True
        except KeyError:
            self.user = False

        # Sending Appropriate content to the client
        content = "NOT FOUND".encode()
        path = self.path
        if path in routes:
            ## print("PATH:", path)
            content = routes[path]().encode()
            response = 200
            if content == "Logged IN".encode():
                # print("Changing resp to 303")
                response = 303
            # print("Calling:", routes[path])
        
        elif (".css" in str(path)) | (".js" in str(path)):
            # print("Other files:", path)
            response = 200
            try:
                path = "../web" + path
                f = open(path, 'rb')
                content = f.read()
                f.close()
            except Exception:
                content = "NOT FOUND".encode()
                response = 404
            # print("Sending file:", path, response)
        elif  (".png" in str(path)):
            path = "../web" + path
            image = Image.open(path)
            output = BytesIO()
            image.save(output, format="png")
            content = output.getvalue()

        # Sending important headers
        self.send_response(response)
        if response == 303:
            self.send_header('Location', '/')

        # Checking for cookies to send with header
        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)

        # Ending header content
        self.end_headers()

        # Sending the body content to client
        if response != 303:
            self.wfile.write(content)

    def do_POST(self):
        global session, session_login_id
        self.user = False
        response = 404
        try:
            if session == self.parse_cookies(self.headers['Cookie'])['SID']:
                self.user = True
        except KeyError:
            self.user = False
        resp = self.rfile.read(int(self.headers['Content-Length'])).decode()
        if self.user:
            user_req = urllib.parse.parse_qs(resp)
            ## print("User Request:", user_req, ":from:", resp)
            if resp.find("peopleList") != -1:
                self.send_response(200)
                # Setting the header
                self.send_header("Content-type", "text/html")
                # Whenever using 'send_header', you also have to call 'end_headers'
                self.end_headers()

                return_str = list(message.Message().student.values())
                # print(return_str)
                self.wfile.write(str(return_str).encode())
            elif "OVERRIDE" in resp:
                message.Message.msg_prc.append("OVERRIDE")

                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()

            elif(resp.find("srn") != -1):

                if user_req['options'][0] == 'a':
                    message.Message().msg_src.append(['R' + str(user_req['srn'][0]), '-'])
                    print("Appended Message:", message.Message.msg_src)
                    message.Message().msg.append(user_req['srn'][0])
                elif user_req['options'][0] == 'p':
                    message.Message().msg_src.append(['R' + str(user_req['srn'][0]), '+'])
                    print("Appended Message:", message.Message.msg_src)
                    message.Message().msg.append(user_req['srn'][0])
                elif user_req['options'][0] == 'r':
                    message.Message().msg_src.append(['R' + str(user_req['srn'][0]), 'r', user_req['report'][0], session_login_id])
                    print("Appended Message:", message.Message.msg_src)
                    message.Message().msg.append(user_req['srn'][0])
                
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()  
            elif (resp.find("name") != -1):
                srn = list(message.Message.student.keys())[list(message.Message.student.values()).index(user_req['name'][0])]
                ## print("SRN", srn)

                if user_req['options'][0] == 'a':
                    message.Message().msg_src.append(['R' + srn, '-'])
                    print("Appended Message:", message.Message.msg_src)
                elif user_req['options'][0] == 'p':
                    message.Message().msg_src.append(['R' + srn, '+'])
                    print("Appended Message:", message.Message.msg_src)
                elif user_req['options'][0] == 'r':
                    message.Message().msg_src.append(['R' + srn, 'r', user_req['report'][0], session_login_id])
                    print("Appended Message:", message.Message.msg_src)
                
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers() 
        else:
            user_response = urllib.parse.parse_qs(str(resp))
            if len(message.Message().msg_login['ID']) == 0:
                message.Message().msg_login['ID'] = user_response['id'][0]
                session_login_id = user_response['id'][0]
                ## print("Teacher ID:", session_login_id)
                message.Message().msg_login['PASS'] = user_response['pass'][0]
                time.sleep(5)
                self.send_response(303)
                self.send_header('Location', '/login')
                self.end_headers()
            


    def home(self):
        ## print("Sending home page")

        # Sending Login page by default
        f = open("../web/login.html", 'r')
        # If the user is logged in: Send the Index page
        # print("self.user: ", self.user)
        if self.user:
            f = open("../web/index.html", 'r')
        
        # Reading and writing the file to client
        content = f.read()
        f.close()
        return content

    def login(self):
        # Check Password here
        global session
        if session == "":
            ## print("CLASS:", message.Message.msg_cls)
            # print("AUTH:", message.Message.auth)
            if (message.Message.msg_cls != "") & (message.Message.auth == True):
                self.user = True
                s_id = hashlib.md5(str(time.time()).encode()).hexdigest()
                self.cookie = "SID={}".format(s_id)
                session = s_id
                return "Logged IN"
            else:
                self.send_response(303)
                # print("Redirecting to home-login page")
                self.send_header('Location', '/')
                self.end_headers()
        else:
            return "Another User has logged in"


    def logout(self):
        global session
        if (session != "")& (message.Message.auth == True):
            session = ""
            # self.send_response(303)
            ## print("LOGGED OUT: Redirecting to home-login page")
            # self.send_header('Location', '/')
            # self.end_headers()
            f = open("../web/shutdown.html", 'r')
            content = f.read()
            f.close()
            message.Message.auth = False
            message.Message.shut_down = True

            return content
        else:
            return "No user logged in to logout"

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) \
        if cookie_list else {}

def begin():
    interface_server = socketserver
    port = 8090
    is_started = False
    while not is_started:
        try:
            handler_obj = MyHTTPRequestHandler
            interface_server = socketserver.TCPServer(("", port), handler_obj)
            t_serve = threading.Thread(target=interface_server.serve_forever)
            print("Starting server @", port)
            t_serve.start()
            is_started = True
        except Exception:
            port += 1
            
    while True:
        if message.Message.shut_down == True:
            interface_server.server_close()
            print("Shut down: Web Interface Server")
            break

# begin()
