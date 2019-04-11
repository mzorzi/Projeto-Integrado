import face_recognition
from PIL import Image

image = face_recognition.load_image_file("imagens/stock_people.jpg")
face_locations = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

i=0

for face_location in face_locations:
    top, right, bottom, left = face_location
    print("A face located at pixel location top: {}, left: {}, bottom: {}, right: {}".format(top, left, bottom, right))

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save("imagens/face-{}.jpg".format(i))
    i = i+ 1