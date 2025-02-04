import dlib
import cv2

# Load the face detector and face recognition model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load the image (make sure the path is correct)
frame = cv2.VideoCapture(0)  # 0 refers to the default camera
ret, frame = frame.read()
if not ret:
    print("Failed to capture image from camera.")


if frame is None:
    print("Error: Image could not be loaded. Check the file path.")
else:
    # Detect faces
    faces = detector(frame)

    for face in faces:
        try:
            # Get face landmarks (optional, if you need it)
            shape = predictor(frame, face)
            
            # Compute face descriptor (encoding)
            face_encoding = face_rec_model.compute_face_descriptor(frame, face)
            print("Face encoding:", face_encoding)
        except Exception as e:
            print("Error during face encoding:", e)
