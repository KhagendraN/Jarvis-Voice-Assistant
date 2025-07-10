import face_recognition
import cv2
import numpy as np    

def check_authorization(authorized_image_path):
    authorized_image = face_recognition.load_image_file(authorized_image_path)
    authorized_face_encoding = face_recognition.face_encodings(authorized_image)[0]

    video_capture = cv2.VideoCapture(0)

    print("Starting video feed. Press 'q' to quit.")

    attempts = 0
    while attempts < 3:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame.")
            break

        face_locations = face_recognition.face_locations(frame)

        if len(face_locations) == 0:
            print("No faces detected.")
            continue

        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            match = face_recognition.compare_faces([authorized_face_encoding], face_encoding)[0]
            
            if match:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Access Granted ✅", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.imshow("Face Authorization", frame)
                video_capture.release()
                cv2.destroyAllWindows()
                return True  

            else:
                # Draw a box around the face and display access denied
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Access Denied ❌", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.imshow("Face Authorization", frame)
                print("Access Denied. Attempt", attempts + 1)
                attempts += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # If access was denied for 3 attempts, return False
    video_capture.release()
    cv2.destroyAllWindows()
    print("Access Denied. Please try again later.")
    return False  