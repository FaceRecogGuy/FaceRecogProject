import face_recognition
import os
import sys
import cv2
import numpy as np
import math
import time

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_value = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_value * 100, 2)) + '%'
    else:
        value = (linear_value + ((1.0 - linear_value) * math.pow((linear_value - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    def __init__(self, known_faces_dir='known_faces', new_faces_dir='new_faces', log_interval=10):
        self.known_faces_dir = known_faces_dir
        self.new_faces_dir = new_faces_dir
        self.log_interval = log_interval
        self.last_logged_time = 0
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True
        self.encode_faces()

    def encode_faces(self):
        if not os.path.exists(self.known_faces_dir):
            raise RuntimeError(f"The '{self.known_faces_dir}' directory does not exist.")
        
        for image in os.listdir(self.known_faces_dir):
            if not image.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Skipping non-image file: {image}")
                continue
            try:
                face_image = face_recognition.load_image_file(os.path.join(self.known_faces_dir, image))
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    face_encoding = face_encodings[0]
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(image)
                else:
                    print(f"No face encodings found in image: {image}")
            except Exception as e:
                print(f"Error processing image {image}: {e}")

        if not self.known_face_encodings:
            print("No known faces loaded.")
        else:
            print("Known faces loaded:", self.known_face_names)

    def log_new_face(self, face_image):
        current_time = time.time()
        if current_time - self.last_logged_time < self.log_interval:
            return  # Avoid logging the same face multiple times within the log interval
        self.last_logged_time = current_time

        if not os.path.exists(self.new_faces_dir):
            os.makedirs(self.new_faces_dir)
        new_face_path = os.path.join(self.new_faces_dir, f'new_face_{len(os.listdir(self.new_faces_dir)) + 1}.jpg')
        cv2.imwrite(new_face_path, face_image)
        print(f"Logged new face: {new_face_path}")

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            if self.known_face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = 'Unknown'

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index] or face_distances[best_match_index] < 0.5:  # Increased threshold
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])
                else:
                    # Log the new face if it is not recognized
                    self.log_new_face(frame)
            else:
                name = "Unknown"
                confidence = 'Unknown'
                # Log the new face if no known faces are loaded
                self.log_new_face(frame)

            self.face_names.append(f'{name} ({confidence})')

    def annotate_frame(self, frame):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit("Error: Could not open video source.")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture frame")
                continue

            if self.process_current_frame:
                self.process_frame(frame)
            
            self.process_current_frame = not self.process_current_frame

            self.annotate_frame(frame)
            
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()