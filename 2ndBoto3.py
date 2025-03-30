import boto3
import os
import sys
import cv2
import time

class FaceRecognition:
    def __init__(self, known_faces_dir='known_faces', log_interval=10, region_name='ap-southeast-1', process_interval=5, confidence_threshold=80, refresh_interval=300):
        self.known_faces_dir = known_faces_dir
        self.log_interval = log_interval
        self.process_interval = process_interval
        self.confidence_threshold = confidence_threshold
        self.refresh_interval = refresh_interval
        self.last_logged_time = 0
        self.last_refresh_time = 0
        self.frame_count = 0
        self.known_face_encodings = []
        self.known_face_names = []
        self.rekognition = boto3.client("rekognition", region_name=region_name)
        self.encode_faces()
        self.face_locations = []
        self.face_names = []

    def encode_faces(self):
        if not os.path.exists(self.known_faces_dir):
            raise RuntimeError(f"The '{self.known_faces_dir}' directory does not exist.")
        
        self.known_face_encodings = []
        self.known_face_names = []
        
        for image in os.listdir(self.known_faces_dir):
            if not image.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Skipping non-image file: {image}")
                continue
            try:
                image_path = os.path.join(self.known_faces_dir, image)
                with open(image_path, "rb") as image_file:
                    image_bytes = image_file.read()
                response = self.rekognition.detect_faces(
                    Image={"Bytes": image_bytes}, Attributes=["ALL"]
                )
                if response["FaceDetails"]:
                    face_encoding = response["FaceDetails"][0]
                    self.known_face_encodings.append(image_bytes)
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

        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
        new_face_path = os.path.join(self.known_faces_dir, f'new_face_{len(os.listdir(self.known_faces_dir)) + 1}.jpg')
        cv2.imwrite(new_face_path, face_image)
        print(f"Logged new face: {new_face_path}")
        self.refresh_known_faces()

    def refresh_known_faces(self):
        current_time = time.time()
        if current_time - self.last_refresh_time >= self.refresh_interval:
            self.encode_faces()
            self.last_refresh_time = current_time

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        _, buffer = cv2.imencode('.jpg', small_frame)
        image_bytes = buffer.tobytes()

        response = self.rekognition.detect_faces(
            Image={"Bytes": image_bytes}, Attributes=["ALL"]
        )

        face_locations = []
        face_names = []
        if response["FaceDetails"]:
            for face_detail in response["FaceDetails"]:
                bounding_box = face_detail["BoundingBox"]
                top = int(bounding_box["Top"] * frame.shape[0])
                right = int((bounding_box["Left"] + bounding_box["Width"]) * frame.shape[1])
                bottom = int((bounding_box["Top"] + bounding_box["Height"]) * frame.shape[0])
                left = int(bounding_box["Left"] * frame.shape[1])
                face_locations.append((top, right, bottom, left))

                name = "Unknown"
                confidence = face_detail["Confidence"]
                for known_face, known_name in zip(self.known_face_encodings, self.known_face_names):
                    if self.compare_faces(known_face, image_bytes):
                        name = known_name
                        break

                if name == "Unknown" and confidence >= self.confidence_threshold:
                    self.log_new_face(frame)

                face_names.append(f'{name} ({confidence:.2f}%)')

        self.face_locations = face_locations
        self.face_names = face_names

    def compare_faces(self, known_face, face_image):
        response = self.rekognition.compare_faces(
            SourceImage={"Bytes": known_face},
            TargetImage={"Bytes": face_image},
            SimilarityThreshold=70
        )
        return len(response['FaceMatches']) > 0

    def annotate_frame(self, frame):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
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

            self.frame_count += 1
            if self.frame_count % self.process_interval == 0:
                self.process_frame(frame)

            self.annotate_frame(frame)
            
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition(region_name="ap-southeast-1")  # Change to your actual region name
    fr.run_recognition()