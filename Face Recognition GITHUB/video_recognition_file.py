import face_recognition
import cv2
import os
import time
import multiprocessing


def func(frame_recived, known_face_encodings_recived, frame_number_recived, output_movie_recived, queue_recived, queue_images_recived):
    face_locations = []
    face_encodings = []
    face_names = []
    unknown_face = "Unknown"
    rgb_frame = frame_recived[:, :, ::-1]

    start_time = time.time()
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    elapsed_time = time.time() - start_time
    print("[INFO][{}] Tempo para achar rostos: {}".format(frame_number_recived,elapsed_time))
    face_names = []
    start_time = time.time()
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings_recived, face_encoding)
        name = unknown_face

            # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    elapsed_time = time.time() - start_time
    print("[INFO][{}] Tempo para localizar faces: {}".format(frame_number_recived,elapsed_time))

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue
        color = (0,0,255)
        if "Unknown" in name:
            color = (0,255,0)
            # Draw a box around the face
        cv2.rectangle(frame_recived, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
        cv2.rectangle(frame_recived, (left, bottom - 25), (right, bottom), color, 2)
        cv2.putText(frame_recived, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
    # Write the resulting image to the output video file

    while True: 
        rec = queue_recived.get()
        if frame_number_recived != rec:
            queue_recived.put(rec)

        if frame_number_recived == rec:
            queue_images_recived.put(frame_recived)
            #output_movie_recived.write(frame_recived)   
            queue_recived.put(rec+2)
            #if (frame_number_recived % 100) == 0:
            print("[INFO][{}] Writing frame {} / {}".format(frame_number_recived, frame_number_recived, length))
            
            break

    return






if __name__ == '__main__':
    # This is a demo of running face recognition on a video file and saving the results to a new video file.
    #
    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Open the input movie file
    input_movie = cv2.VideoCapture("/home/victor/Downloads/praca4k20sec.mp4")
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter('output.avi', fourcc, 30, (1080, 720))

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
    print("Frames: {}".format(length))
    unknown_face = "Unknown"
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0


    process_this_frame = True

    queue = multiprocessing.Queue()
    queue_images = multiprocessing.Queue()
    queue.put(1)
    while process_this_frame:
        jobs = []
        counter = 0
        for i in range(0, 16):
        # Grab a single frame of video
            ret, frame = input_movie.read()
            frame_number += 1
            #(h, w) = frame.shape[:2]
            #print("[INFO] w: {} h:{}".format(h, w))
            #frame = cv2.flip( frame, 0 )
            # Quit when the input video file ends
            if not ret:
                process_this_frame = False
                break
            if i % 2 == 0:
                process = multiprocessing.Process(target=func, args=(frame, known_face_encodings, frame_number, output_movie, queue, queue_images))
                jobs.append(process)
                process.start()
                print("Processo da frame {} iniciado".format(frame_number))
            else:
                queue_images.put(frame)
                print("Nao Processando a frame {}".format(frame_number))
            counter += 1
                
        for i in range(0,counter):
            frame_write = queue_images.get()
            frame_write = cv2.resize(frame_write,(1080,720))
            output_movie.write(frame_write) 
        
        #print("Aguardando fim dos processos")
        for j in jobs:
            j.join()
        #print("Processos encerrados") 

    # All done!
    print("acabou")
    input_movie.release()
    cv2.destroyAllWindows()