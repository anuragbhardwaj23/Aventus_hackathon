import cv2
import os
import numpy as np
import face_recognition


def compare_faces(image1, image2):
    face_encodings1 = face_recognition.face_encodings(image1)
    face_encodings2 = face_recognition.face_encodings(image2)
    return face_recognition.compare_faces(face_encodings1, face_encodings2)


def capture_face():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the video capture
    cap = cv2.VideoCapture(0)

    # Create a directory to save the captured photo
    save_directory = 'captured_faces'
    os.makedirs(save_directory, exist_ok=True)

    # Initialize variables
    photo_taken = False
    face_detected = False

    while True:
        # Read the frame from the video capture
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(150, 150))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Capture Face', frame)

        # Capture a photo of the first detected face
        if len(faces) > 0 and not photo_taken:
            face_detected = True
            x, y, w, h = faces[0]
            face_image = frame[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(save_directory, 'captured_face.jpg'), face_image)
            photo_taken = True

            # Compare the captured face with images in the dataset directory
            dataset_directory = r'C:\Users\anura\OneDrive\Desktop\DSCE_TechTitans\images'
            for filename in os.listdir(dataset_directory):
                if filename.endswith('.png') or filename.endswith('.jpg'):
                    image2_path = os.path.join(dataset_directory, filename)
                    image2 = cv2.imread(image2_path)
                    same_faces = compare_faces(face_image, image2)

                    if same_faces:
                        print(f'Captured face matches with {image2_path}')
                    else:
                        print(f'Captured face does not match with {image2_path}')

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


# Call the capture_face function
capture_face()
