# pip freeze > requirements.txt 
# Stores the current installed packages & versions into the file 

# pip install -r requirements.txt 
# Installs exactly the same packages, versions into a new environment 

########################################################################################
################################################# Imports ##############################
# Importing pacakges nescessary for face recognition
import face_recognition
import cv2
import numpy as np

# Importing required system packages
import os
import glob
import sys
import logging

# Importing custom debug print, path2name modules
sys.path.insert(1, os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "lib/usr"))
import debug_print as dprint
import path2name as pn
import message
########################################################################################
def begin():
    ################################# Checking for parameter ###############################
    logging.basicConfig(filename='app.log', filemode='a', format='[%(created)i]- %(levelname)s - %(message)s', level=logging.DEBUG)
    # if sys.argv[1] == "--debug" or sys.argv[1] == "-d":
    # 	dprint.set_print_level(1) # 1 for complete Debug data
    # elif sys.argv[1] == "--info" or sys.argv[1] == "-i":
    # 	dprint.set_print_level(2) # 2 for top level data

    ########################################################################################
    #################################### Getting Face Paths ################################
    faces_encodings = []
    faces_names = []
    cur_direc = os.getcwd()
    cur_direc = os.path.abspath(os.path.join(cur_direc, os.pardir))
    path = os.path.join(cur_direc, 'data/faces/')
    logging.debug("Using faces stored in " + str(path))
    # dprint.dprint(3, "Using faces stored in: " + path)

    list_of_files = [f for f in glob.glob(path+'*.jpg')]
    number_files = len(list_of_files)
    names = list_of_files.copy()
    logging.debug("List " + str(names))
    # dprint.dprint(1, "List" + str(names))
    ########################################################################################


    # dprint.dprint(4, "Training the faces")
    logging.debug("Training faces")
    ########################################################################################
    ############################# Training the Faces #######################################
    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])# Create array of known names
        names[i] = names[i].replace(cur_direc, "")
        faces_names.append(names[i])
        # dprint.dprint(1, "Training Face[" + str(i+1) + "] " + str(names[i]))
        logging.debug("Training Face[" + str(i+1) + "] " + str(names[i]))
    ########################################################################################
    # dprint.dprint(4, "Finished training faces")
    logging.info("Finished training faces")


    face_locations = []
    face_encodings = []
    face_names = [] 
    process_this_frame = True

    # Starting Capture from Camera
    # video_capture = cv2.VideoCapture(-1)
    video_capture = cv2.VideoCapture(0)


    name = ""

    # dprint.dprint(4, "Starting the Face Recognition Algorithm")
    logging.info("Face recognition algorithm started")
    prevName = ""

    while True:
    ########################################################################################
    ###################################### Face Recognition ################################
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        name = "Unknown"

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(faces_encodings, face_encoding)

                face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = faces_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        # Print only if the person is known
        if name != "Unknown":
            # Don't repeatedly print the same values
            if prevName != name:
                # dprint.dprint(1, name + "," + prevName)
                if(pn.path2name(name) not in message.Message().msg):
                    logging.info("Recognized person " + str(pn.path2name(name)))
                    # message.Message().msg_src.append({pn.path2name(name):'+'})
                    message.Message().msg_src.append([pn.path2name(name), '+'])
                    if pn.path2name(name).find("ug") == -1:
                        message.Message().msg.append(pn.path2name(name))
                else:
                    logging.info("Recognized duplicate person " + str(pn.path2name(name)))
                    print(">>>  Source", message.Message().msg_src)
                    print(">>> Process", message.Message().msg_prc)
                    print(">>> Message", message.Message().msg)
                    print(">>> Student", message.Message().student)
                prevName = name

        if message.Message.shut_down == True:
            print("Shutting down Face Recognition Module")
            logging.info("Face Recognition: Shutting down triggered")
            video_capture.release()
            # cv2.destroyAllWindows()
            logging.info("Face Recognition: Shut Down: OK")
            break

        ########################################################################################
# start()
