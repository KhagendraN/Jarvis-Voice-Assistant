import face_recognition
import cv2
import numpy as np    
import logging

logger = logging.getLogger("FaceAuth")

def check_authorization(authorized_image_path):
    try:
        authorized_image = face_recognition.load_image_file(authorized_image_path)
        encodings = face_recognition.face_encodings(authorized_image)
        if not encodings:
            logger.error(f"No face found in authorized image: {authorized_image_path}")
            return False
        authorized_face_encoding = encodings[0]
    except Exception as e:
        logger.error(f"Failed to load or encode authorized image: {e}")
        return False

    try:
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            logger.error("Could not open webcam.")
            return False
        logger.info("Starting video feed. Press 'q' to quit.")
        attempts = 0
        while attempts < 3:
            ret, frame = video_capture.read()
            if not ret:
                logger.error("Failed to grab frame from webcam.")
                break
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) == 0:
                logger.warning("No faces detected.")
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
                    logger.info("Face authentication successful.")
                    return True
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Access Denied ❌", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    cv2.imshow("Face Authorization", frame)
                    logger.warning(f"Access Denied. Attempt {attempts + 1}")
                    attempts += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()
        logger.warning("Access Denied. Please try again later.")
        return False
    except Exception as e:
        logger.error(f"Exception during face authorization: {e}")
        return False  