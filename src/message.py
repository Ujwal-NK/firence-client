class Message:
    # Variable to store Class (ELECTRICAL, PHYSICS, PHYSICS LAB, COMPUTERS, COMPUTERS LAB, CHEMISTRY, BIOLOGY, MATHEMATICS)
    msg_cls = ""
    # Store all from sorce to avoid duplicates - accessed only by recognize_face.py
    msg = [] 
    # Store the student name against their SRN - accessed only by client.py
    student = {}
    # Message from the facial recognition module - processed only by client
    msg_src = [] 
    # Message from the client(remote) - processed only by the lock
    msg_prc = []
    # Teacher login creadentials check variable
    msg_login = {"ID": "", "PASS": ""}
    # Authentication
    auth = False
    # Shutdown call
    shut_down = False
    # Close
    # close = False

    @staticmethod
    def reset():
        # Message.msg_cls = ""
        Message.msg_login = {"ID": "", "PASS": ""}
    
    # @staticmethod
    def pop_msg_src():
        print("Before Popping:", Message.msg_src)
        Message.msg_src.remove(Message.msg_src[0])
        print("After Popping:", Message.msg_src)
