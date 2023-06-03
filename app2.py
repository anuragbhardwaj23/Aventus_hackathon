from flask import Flask, render_template, Response
import cv2
import face_recognition
import os
from imutils.video import VideoStream

app = Flask(__name__)

# Define vs as a global variable
vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)


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

def generate_frames():
    while True:
        frame = vs.read()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template(r'verification.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_faces')
def detect_faces():
    # Provide the paths to your images here
    image1 = vs.read()  # Capture the image from the webcam
    dataset_directory = r'C:\Users\anura\OneDrive\Desktop\DSCE_TechTitans\images'

    # Detect faces in image1
    face_locations1 = detect_faces(image1)
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

    results = []

    # Iterate over the images in the dataset directory
    for filename in os.listdir(dataset_directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image2_path = os.path.join(dataset_directory, filename)
            image2 = cv2.imread(image2_path)
            same_faces = compare_faces(image1, image2)

            if same_faces:
                results.append(f'Captured image matches with {image2_path}')
            else:
                results.append(f'Captured image does not match with {image2_path}')

    return '\n'.join(results)

if __name__ == '__main__':
    app.run(debug=True)
