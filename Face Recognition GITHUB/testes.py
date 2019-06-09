import face_recognition
import cv2
import os
import time
import threading
import _thread
import multiprocessing 

finished = 0
frame_number = 1


# Open the input movie file
input_movie = cv2.VideoCapture("/home/murilo/Github/Dataset P.I/praca4k5min.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('output.avi', fourcc, 30, (3840, 2160))

unknown_face = "Unknown"
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []     

def par():
    print("[INFO][PAR] INICIADO")
    global unknown_face
    global finished
    global frame_number
    global input_movie
    global length
    global fourcc
    global output_movie
    global face_locations
    global face_encodings
    global face_names
    process_this_frame = True

    while True:
        if frame_number % 2 == 0:
            # Grab a single frame of video
            print("[INFO][PAR] Frame retirada: {}".format(frame_number))
            this_frame_number = frame_number
            ret, frame = input_movie.read()
            frame_number += 1
            #(h, w) = frame.shape[:2]
            #print("[INFO] w: {} h:{}".format(h, w))
            #frame = cv2.flip( frame, 0 )
            # Quit when the input video file ends
            if not ret:
                finished = 1
                break

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]
            if process_this_frame:

                start_time = time.time()

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                elapsed_time = time.time() - start_time
                print("[INFO][PAR] Tempo para achar rostos: {}".format(elapsed_time))
                face_names = []
                start_time = time.time()
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding)
                    name = unknown_face

                        # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

                elapsed_time = time.time() - start_time
                print("[INFO][PAR] Tempo para localizar faces: {}".format(elapsed_time))
            if not process_this_frame:
                print("[INFO][PAR] Frame n processada")
            process_this_frame = not process_this_frame
            # Label the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not name:
                    continue
                color = (0,0,255)
                if "Unknown" in name:
                    color = (0,255,0)
                    # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                    # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                

            
            # Write the resulting image to the output video file
            
            print("[INFO][PAR] Writing frame {} / {}".format(this_frame_number, length))
            output_movie.write(frame)            
    return

def impar():
    print("[INFO][IMPAR] INICIADO")
    global unknown_face
    global finished
    global frame_number
    global input_movie
    global length
    global fourcc
    global output_movie
    global face_locations
    global face_encodings
    global face_names
    process_this_frame = True

    while True:
        if frame_number % 2 == 1:
            # Grab a single frame of video
            ret, frame = input_movie.read()
            print("[INFO][IMPAR] Frame retirada: {}".format(frame_number))
            this_frame_number = frame_number
            frame_number += 1
            #(h, w) = frame.shape[:2]
            #print("[INFO] w: {} h:{}".format(h, w))
            #frame = cv2.flip( frame, 0 )
            # Quit when the input video file ends
            if not ret:
                finished = 1
                break

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]
            if process_this_frame:

                start_time = time.time()

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                elapsed_time = time.time() - start_time
                print("[INFO][IMPAR] Tempo para achar rostos: {}".format(elapsed_time))
                face_names = []
                start_time = time.time()
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding)
                    name = unknown_face

                        # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

                elapsed_time = time.time() - start_time
                print("[INFO][IMPAR] Tempo para localizar faces: {}".format(elapsed_time))
            if not process_this_frame:
                print("[INFO][IMPAR] Frame n processada")   
            process_this_frame = not process_this_frame
            # Label the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not name:
                    continue
                color = (0,0,255)
                if "Unknown" in name:
                    color = (0,255,0)
                    # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                    # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                

            
            # Write the resulting image to the output video file
            
            print("[INFO][IMPAR] Writing frame {} / {}".format(this_frame_number, length))
            output_movie.write(frame)            
    return




# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.


path = "imagens/"

# Load some sample pictures and learn how to recognize them.
directory = os.fsencode(path)
count = 0
known_face_encodings = []
known_face_names = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".png"):
        known_face_encodings.append(face_recognition.face_encodings(
            face_recognition.load_image_file(path+filename))[0])
        known_face_names.append(filename[:-4])
        count = count + 1
        continue

print("Banco de dados: {} imagens".format(count))

jobs = []

p = multiprocessing.Process(target=par)
jobs.append(p)
p.start()
p = multiprocessing.Process(target=impar)
jobs.append(p)
p.start()


threads = []

t = threading.Thread(target=par)
threads.append(t)
t.start()
t = threading.Thread(target=impar)
threads.append(t)
t.start()

while True:
    if finished == 1:
        # All done!
        input_movie.release()
        cv2.destroyAllWindows()
