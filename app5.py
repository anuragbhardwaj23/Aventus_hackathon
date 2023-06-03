from flask import Flask, render_template
import cv2
import face_recognition
import os
from imutils.video import VideoStream
import csv
from datetime import datetime

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/compare_faces', methods=['POST'])
def compare_faces_route():
    # Initialize the video stream
    vs = VideoStream(src=0).start()

    # Capture the image from the webcam
    image1 = vs.read()

    # Provide the path to your dataset directory here
    dataset_directory = r'C:\Users\anura\OneDrive\Desktop\DSCE_TechTitans\images'

    # Detect faces in image1
    face_locations1 = detect_faces(image1)
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

    # Create an empty list to store the results
    results = []
    flag = False
    result = ''

    # Iterate over the images in the dataset directory
    for filename in os.listdir(dataset_directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image2_path = os.path.join(dataset_directory, filename)
            image2 = cv2.imread(image2_path)
            same_faces = compare_faces(image1, image2)

            if same_faces:
                flag = True
                name, number = filename.rsplit("_", 1)

                result = f'FaceMatch Successful!! Access Granted Name: {name}, TicketID: {number}'
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

                # Append the matched filename and timestamp to the CSV file
                with open('matches.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([filename, timestamp])
                
                # Delete the matched image2
                os.remove(image2_path)
                
                break

    if not flag:
        result = 'Details not found!! Please proceed with manual verification'

    results.append(result)

    # Stop the video stream and close all windows
    vs.stop()
    cv2.destroyAllWindows()

    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
