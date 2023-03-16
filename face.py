import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

if not os.path.exists('faces'):
    os.makedirs('faces')

cap = cv2.VideoCapture(0)
counter = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('r'):
        for (x, y, w, h) in faces:
            counter += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f'faces/face_{counter}.jpg', face_img)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f'Face {counter} registered!', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow('Face Detection', frame)
        cv2.waitKey(3000)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        face_paths = [os.path.join('faces', f) for f in os.listdir('faces') if f.endswith('.jpg')]
        faces = []
        labels = []
        for i, path in enumerate(face_paths):
            img = cv2.imread(path, 0)
            faces.append(img)
            labels.append(i+1)
        recognizer.train(faces, np.array(labels))

        cv2.putText(frame, 'Recognizer trained!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_img)
            name = f'Person {label}'
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
