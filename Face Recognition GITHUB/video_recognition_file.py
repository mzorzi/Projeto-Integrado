import face_recognition
import cv2
import os
import time

# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file
input_movie = cv2.VideoCapture("/home/murilo/Github/Dataset P.I/praca4k5min.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('output.avi', fourcc, 30, (3840, 2160))

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

unknown_face = "Unknown"
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1
    #(h, w) = frame.shape[:2]
    #print("[INFO] w: {} h:{}".format(h, w))
    #frame = cv2.flip( frame, 0 )
    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]
    if process_this_frame:

        start_time = time.time()

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        elapsed_time = time.time() - start_time
        print("[INFO] Tempo para achar rostos: {}".format(elapsed_time))
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
        print("[INFO] Tempo para localizar faces: {}".format(elapsed_time))

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

            # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    process_this_frame = not process_this_frame
    # Write the resulting image to the output video file
    print("Writing frame {} / {}".format(frame_number, length))
    output_movie.write(frame)

# All done!
input_movie.release()
cv2.destroyAllWindows()