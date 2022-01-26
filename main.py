# Code Starting point, starts both the recognize_face.py as well as the server.
import time
import logging
logging.basicConfig(filename='app.log', filemode='a', format='[%(created)i]- %(levelname)s - %(message)s', level=logging.DEBUG,  datefmt='%d-%b-%y %H:%M:%S')
logging.info("Infinite Bit...")
print("Starting")
import threading
logging.debug("Module Import: Threading : OK")
print("Imported Threading")
import web_interface_server
logging.debug("Module Import: Interface Web Server : OK")
print("Inported interface server")
import recognize_face
logging.debug("Module Import: Face Recognition : OK")
print("Imported Face Recognition")
import web_server
logging.debug("Module Import: Communication Web Server : OK")
print("Imported Web server")
import client
logging.debug("Module Import: Client : OK")


def check_login():
    global face_recog_thread
    while message.Message.auth == False:
        time.sleep(1)
    if message.Message.auth == True:
        face_recog_thread.start()
        logging.debug("Thread Start: Face Recognition: OK")

def get_input():
    i = input()

    if 'q' in i:
        message.Message.shut_down = True
        print("Shutting down the system")


# Creating threads for individual tasks
face_recog_thread = threading.Thread(target=recognize_face.begin, daemon=True)
print("Created thread for FR")
web_interface_server_thread = threading.Thread(target=web_interface_server.begin, daemon=True)
print("Created thread for WIS")
server_thread = threading.Thread(target=web_server.begin, daemon=True)
print("Created threads")
client_thread = threading.Thread(target=client.start_comms, daemon=True)

recog_start_thread = threading.Thread(target=check_login, daemon = True)
input_thread = threading.Thread(target=get_input, daemon=True)

import message
# Starting the threads
a = True

web_interface_server_thread.start()
logging.debug("Thread Start: Web Interface Server : OK")
server_thread.start()
logging.debug("Thread Start: Communication Web Server : OK")
client_thread.start()
recog_start_thread.start()
input_thread.start()


thread_running = True
while thread_running:
    thread_running = False
    if client_thread.is_alive():
        thread_running = True
    if server_thread.is_alive():
        thread_running = True
    if web_interface_server_thread.is_alive():
        thread_running = True
    if face_recog_thread.is_alive():
        thread_running = True

print("Shut Down : OK")
# web_interface_server_thread.stop()
# face_recog_thread.stop()
# server_thread.stop()
# client_thread.stop()
    

# print("done importing")
# import message

# print("Done importing message")

# while True:
    # x= 1
    
# print(message.Message.msg)
