import cv2
import face_recognition
import os
from imutils.video import VideoStream

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply histogram equalization
    gray_eq = cv2.equalizeHist(gray)
    return gray_eq

def detect_faces(image):
    image = preprocess_image(image)
    face_locations = face_recognition.face_locations(image)
    return face_locations

def compare_faces(image1, image2):
    face_locations1 = detect_faces(image1)
    face_locations2 = detect_faces(image2)

    if len(face_locations1) == 0 or len(face_locations2) == 0:
        return False

    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)
    face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

    for face_encoding1 in face_encodings1:
        for face_encoding2 in face_encodings2:
            # Compare the face encodings
            matches = face_recognition.compare_faces([face_encoding1], face_encoding2)
            if any(matches):
                return True

    return False

# Initialize the video stream
vs = VideoStream(src=0).start()

# Provide the paths to your images here
image1 = vs.read()  # Capture the image from the webcam
dataset_directory = r'C:\Users\anura\OneDrive\Desktop\DSCE_TechTitans\images'

# Detect faces in image1
face_locations1 = detect_faces(image1)
face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

# Iterate over the images in the dataset directory
for filename in os.listdir(dataset_directory):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        image2_path = os.path.join(dataset_directory, filename)
        image2 = cv2.imread(image2_path)
        same_faces = compare_faces(image1, image2)

        if same_faces:
            print(f'Captured image matches with {image2_path}')
        else:
            print(f'Captured image does not match with {image2_path}')

# Stop the video stream and close all windows
vs.stop()
cv2.destroyAllWindows()
