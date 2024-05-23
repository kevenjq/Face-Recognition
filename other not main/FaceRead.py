import cv2
import face_recognition
from simple_facerec import SimpleFacerec
import sys
import time
import numpy as np
import time


def take_pass_pic():
    camera = cv2.VideoCapture(0)

    if camera.isOpened():
        ret, frame = camera.read()
        cv2.waitKey(1000)
        cv2.imwrite("../images/facepass.png", frame)

    camera.release()
    cv2.destroyAllWindows()


def take_picture():
    camera = cv2.VideoCapture(0)
    time.sleep(5)
    if camera.isOpened():
        ret, frame = camera.read()
        cv2.waitKey(1000)
        cv2.imwrite("../images/Pic_taken.png", frame)

    camera.release()
    cv2.destroyAllWindows()


def analyze_user():
    baseing = face_recognition.load_image_file("../images/facepass.png")
    baseing = cv2.cvtColor(baseing, cv2.COLOR_BGR2RGB)

    # myface = face_recognition.face_locations(baseing)[0]
    encodingmyface = face_recognition.face_encodings(baseing)[0]
    # cv2.rectangle(baseing, (myface[3], myface[0]), (myface[1], myface[2]), (255, 0, 255), 2)

    # cv2.imshow("test", baseing)
    # cv2.waitKey(0)

    cameraimg = face_recognition.load_image_file("../images/Pic_taken.png")
    cameraimg = cv2.cvtColor(cameraimg, cv2.COLOR_BGR2RGB)

    picTaken = face_recognition.face_locations(cameraimg)[0]
    encodepictaken = face_recognition.face_encodings(cameraimg)[0]

    result = face_recognition.compare_faces([encodingmyface], encodepictaken)

    result_to_string = str(result)

    """
    print(bool(result))
    if not(bool(result)) == True:
        print("good")
    elif not(bool(result)) == False:
        print("okay i get it")


        if result_to_string == "[True]":
        cv2.rectangle(cameraimg, (picTaken[3],picTaken[0]), (picTaken[1], picTaken[2]), (255, 0, 255), 2)
        cv2.imshow("new test me", cameraimg)
        cv2.waitKey(0)
    else:
        cv2.imshow("NOT RIGHT ONE", cameraimg)
        cv2.waitKey(0)
    """
    print("face recognition complete")
    return result
    # cv2.addText(cameraimg,"Successful!!", (15, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),2)


"""
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cam = cv2.VideoCapture(0)

time.sleep(3)
running = True
if running:
    ret, frame = cam.read()

    cv2.imshow("frame",frame)

    face_location, face_names = sfr.detect_known_faces(frame)
    for face_loco, name in zip(face_location, face_names):
        print(face_loco)

    key = cv2.waitKey(0)


    cam.release()
    cv2.destroyAllWindows()
"""
sfr = SimpleFacerec()
sfr.load_encoding_images("Test.png")
# live_recognition()
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    baseing = face_recognition.load_image_file("images/facepass.png")
    baseing = cv2.cvtColor(baseing, cv2.COLOR_BGR2RGB)
    encodingmyface = face_recognition.face_encodings(baseing)[0]

    cameraimg = face_recognition.load_image_file("images/known_face.png")
    cameraimg = cv2.cvtColor(cameraimg, cv2.COLOR_BGR2RGB)
    knownpictaken = face_recognition.face_locations(cameraimg)[0]
    encodepictaken = face_recognition.face_encodings(cameraimg)[0]

    result = face_recognition.compare_faces([encodingmyface], encodepictaken)
    result_to_string = str(result)
    print(result_to_string)

    if result_to_string == "[True]":
        #put name
        name = "keven"
        cv2.rectangle(cameraimg, (knownpictaken[3], knownpictaken[0]), (knownpictaken[1], knownpictaken[2]),
                      (255, 0, 255), 2)
        cv2.putText(cameraimg, name, (knownpictaken[3], knownpictaken[0]+300), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("new test me", cameraimg)
    cv2.waitKey(0)
    # cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

    cap.release()
    cv2.destroyAllWindows()
