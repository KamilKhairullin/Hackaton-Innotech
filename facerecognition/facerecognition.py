import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import face_recognition
import os
import cv2

KNOWN_FACES_DIR = '/content/known_faces'
UNKNOWN_FACES_DIR = '/content/unknown_faces'
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'

known_faces = []
known_names = []
def add_face(image_path, id):
    image = face_recognition.load_image_file(image_path)

    encoding = face_recognition.face_encodings(image)[0]

    known_faces.append(encoding)
    known_names.append(id)

def find_face(image_path):
    image = face_recognition.load_image_file(image_path)

    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    print(f'found {len(encodings)} face(s)')
    for face_encoding, face_location in zip(encodings, locations):

        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

        match = None
        if True in results:

            match = known_names[results.index(True)]

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = name_to_color(match)

            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)

            cv2.rectangle(image, top_left, bottom_right, 255, cv2.FILLED)

            print(match)
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    return image

for name in os.listdir(KNOWN_FACES_DIR):
    i += 1
    add_face(f'{KNOWN_FACES_DIR}/{name}', name)

img = find_face('/content/unknown_faces/17.jpg')

imgplot = plt.imshow(img)
plt.show()
