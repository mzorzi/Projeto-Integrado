import face_recognition

image = face_recognition.load_image_file("imagens/fallen1.jpg")
unknow_image = face_recognition.load_image_file("imagens/full_mibr.jpg")

fallen_encoding = face_recognition.face_encodings(image)[0]
unknow_encoding = face_recognition.face_encodings(unknow_image)[0]

results = face_recognition.compare_faces([fallen_encoding], unknow_encoding)
print(results)
