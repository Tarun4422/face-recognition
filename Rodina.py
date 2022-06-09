from asyncore import loop
import face_recognition
import cv2
import numpy as np
import def_load as load
import random as rn

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
print("GO!")
# for a in range(10):
#     print("trying", a)
#     video_capture = cv2.VideoCapture(a, cv2.CAP_DSHOW)
#     ret, frame = video_capture.read()
#     print(ret)
#     if ret == True:
#         break
#     else:
#         video_capture.release()
video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

print(video_capture)

# Load a sample picture and learn how to recognize it.
maja = load.img("faces_rodina/maja.png")
mama = load.img("faces_rodina/mama.jpg")
mata = load.img("faces_rodina/mata.png")
michael = load.img("faces_rodina/michael.jpg")
tata = load.img("faces_rodina/tata.png")



# Create arrays of known face encodings and their names
known_face_encodings = [maja, mama, mata, michael, tata]
known_face_names = ['maja', 'mama', 'mata', 'michael', 'tata']

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
loop_noob = 0

while True:
    loop_noob = loop_noob + 1
    # Grab a single frame of video
    ret, frame = video_capture.read()
    print(ret, loop_noob)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
    # small_frame = frame

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 5
        right *= 5
        bottom *= 5
        left *= 5

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
