import face_recognition
import cv2
import time
# This code finds all faces in a list of images using the CNN model.
#
# This demo is for the _special case_ when you need to find faces in LOTS of images very quickly and all the images
# are the exact same size. This is common in video processing applications where you have lots of video frames
# to process.
#
# If you are processing a lot of images and using a GPU with CUDA, batch processing can be ~3x faster then processing
# single images at a time. But if you aren't using a GPU, then batch processing isn't going to be very helpful.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read the video file.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open video file
start_total_time = time.time()

video_capture = cv2.VideoCapture("/home/murilo/Github/Dataset PI/praca4k3sec.mp4")
batch_size = 2
frames = []
frame_count = 0


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

print("[INFO] Banco de dados: {} imagens".format(count))
unknown_face = "Desconhecido"
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0









while video_capture.isOpened():
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Bail out when the video file ends
    if not ret:
        break
    #frame = cv2.resize(frame,(1080,720))
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    frame = frame[:, :, ::-1]

    # Save each frame of the video to a list
    frame_count += 1
    frames.append(frame)

    # Every 128 frames (the default batch size), batch process the list of frames to find faces
    if len(frames) == batch_size:
        batch_time = time.time()
        batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0, batch_size=batch_size)
        final_batch_time = time.time() - batch_time
        print("Tempo para processar {} frames: {}".format(batch_size, final_batch_time))
        # Now let's list all the faces we found in all 128 frames
        for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
            number_of_faces_in_frame = len(face_locations)

            frame_number = frame_count - batch_size + frame_number_in_batch
            print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))

            for face_location in face_locations:
                # Print the location of each face in this frame
                top, right, bottom, left = face_location
                print(" - A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # Clear the frames array to start the next batch
        frames = []

final_total_time = time.time() - start_total_time
print("Tempo total: {}".format(final_total_time))