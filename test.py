import dlib
import cv2

# Load the face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load an image
frame = cv2.imread('image.jpg')

# Detect faces in the image
faces = detector(frame)

# Iterate through the detected faces
for face in faces:
    # Get face landmarks (predictor returns full_object_detection)
    shape = predictor(frame, face)
    
    # Compute the face descriptor (encoding)
    face_encoding = face_rec_model.compute_face_descriptor(frame, shape)
    print("Face encoding:", face_encoding)
