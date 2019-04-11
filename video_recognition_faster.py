import face_recognition
import cv2
import os

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

escale = 0.25
# 0 é a webcam nativa, ver o print do loop abaixo para ver as webcans disponiveis
camera_default = 0
"""
#loop para testar 10 cameras e ver quais estao disponiveis
cams_test = 10
for i in range(0, cams_test):
    cap = cv2.VideoCapture(i)
    test, frame = cap.read()
    print("i : "+str(i)+" /// result: "+str(test))
"""
video_capture = cv2.VideoCapture(camera_default)

directory = os.fsencode("imagens/faces")
count = 0
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".png"):
        count = count + 1
        continue
    else:
        continue
print("Banco de dados: {} imagens".format(count))

# Load a sample picture and learn how to recognize it.
fer_image = face_recognition.load_image_file("imagens/faces/fer.jpg")
fer_face_encoding = face_recognition.face_encodings(fer_image)[0]

# Load a second sample picture and learn how to recognize it.
fallen_image = face_recognition.load_image_file("imagens/faces/fallen.jpg")
fallen_face_encoding = face_recognition.face_encodings(fallen_image)[0]

# Load a second sample picture and learn how to recognize it.
murilo_image = face_recognition.load_image_file("imagens/faces/murilo.jpg")
murilo_face_encoding = face_recognition.face_encodings(murilo_image)[0]

# Load a second sample picture and learn how to recognize it.
pupo_image = face_recognition.load_image_file("imagens/faces/pupo.jpg")
pupo_face_encoding = face_recognition.face_encodings(pupo_image)[0]

# Load a second sample picture and learn how to recognize it.
ettore_image = face_recognition.load_image_file("imagens/faces/ettore.jpg")
ettore_face_encoding = face_recognition.face_encodings(ettore_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    fer_face_encoding,
    fallen_face_encoding,
    murilo_face_encoding,
    pupo_face_encoding,
    ettore_face_encoding
]
known_face_names = [
    "Fer",
    "Fallen",
    "Murilo",
    "Matheus",
    "Etotore"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=escale, fy=escale)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= int(escale*16)
        right *= int(escale*16)
        bottom *= int(escale*16)
        left *= int(escale*16)

        color = (0, 0, 255)
        if "Unknown" in name:
            color = (0, 255, 0)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()