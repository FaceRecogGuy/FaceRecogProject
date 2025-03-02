# FaceRecogProject
### Recognises known faces based on the referenced directory and labels unknown faces as "Unknown"
### Internship project
# Setting up the project
## 1. Work environment
- Using your computer's command prompt [accessible via your desktop/laptop search bar] is sufficient, but I would recommend installing Visual Studio Code for a neat and tidy workspace
- Keep track of where you've downloaded the file "facetest2again.py". In the exact same location, create a new folder called "known_faces" and upload as many images as you want.
## 2. Build dependencies
- run the following command: pip install face_recognition opencv-python numpy
- if you encounter an error message saying "failed to install some libraries for dlib" refer to the next points
- https://github.com/z-mahmud22/Dlib_Windows_Python3.x go to this link and download whichever .msi dlib wheel file matches your python version
- run cd [insert path to your downloaded file here]
- run pip install dlib-<version>-cp<python_version>-win_amd64.whl [or just copy the exact name of the file]
- you should be able to run the first command again
## 3. Actually running the file
- Ensure that your desktop or laptop camera can see you
- run cd [insert path to wherever you downloaded facetest2again.py]
- run "python facetest2again.py"
- The recognition is quite insensitive, so try to slowly move your head around to match the position of your face within the reference image you put into the known_faces folder
# code from https://youtu.be/tl2eEBFEHqM?si=WDNKmpL3BWeqJPOZ
