import cv2
from HandTrackingModule import HandDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from mongo_db import get_database
import time
import face_recognition
import pickle
import os


def recognize_face(img, link_enc):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        unknown_face_encoding = face_recognition.face_encodings(rgb_img)[0]
        results = face_recognition.compare_faces(
            link_enc, unknown_face_encoding)
        print(results)
    except IndexError:
        print('no Face')


def face_recognize(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    try:
        return face_recognition.face_encodings(rgb_img)[0]
    except IndexError:
        return []


def upadate_item(item, db):
    print(item)
    temp = db.find_one({"name": item})
    if temp['qty'] > 0:
        """
        RPI GPIO CODE
        """
        db.update_one({"name": item}, {'$inc': {'qty': -1, 'used': +1}})
    else:
        print('Item out of stock')


def get_encode():
    encode = {}
    for filename in os.listdir('face_encode'):
        if filename.endswith(".pickle"):
            name = filename.split('.')[0]
            with open(os.path.join('face_encode', filename), 'rb') as f:
                encode[name] = pickle.load(f)
        else:
            continue
    return encode


def compare_face(encode, face, threshold=0.6):
    name = list(encode.keys())
    print(name)
    face_encode = list(encode.values())
    result = face_recognition.face_distance(face_encode, face)
    print(result)
    min_result = min(result)
    print(min_result)
    if min_result <= threshold:
        return name[result.index(min_result)]
    else:
        return 'unknown'


def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    encode = get_encode()

    # connect to the database
    dbname = get_database()
    db = dbname['items']
    # define Hand detector and set to detect only 1 hand
    detector = HandDetector(detectionCon=0.5, maxHands=1)

    isListen = False

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        # get image from camera
        img = frame.array
        hands, img = detector.findHands(img)
        # check if the picture have hand or not
        if hands != []:
            # detect finger in the hand
            finger = detector.fingersUp(hands[0])

            if isListen:  # hand action
                if finger == [1, 1, 1, 1, 1]:
                    upadate_item('Item_5', db)
                    isListen = False
                elif finger == [0, 1, 1, 1, 1]:
                    upadate_item('Item_4', db)
                    isListen = False
                elif finger == [0, 1, 1, 1, 0]:
                    upadate_item('Item_3', db)
                    isListen = False
                elif finger == [0, 1, 1, 0, 0]:
                    upadate_item('Item_2', db)
                    isListen = False
                elif finger == [0, 1, 0, 0, 0]:
                    upadate_item('Item_1', db)
                    isListen = False
            else:
                # user show thumb up start listening to the hand action
                if finger == [1, 0, 0, 0, 0]:
                    unknown = face_recognize(img)
                    if unknown != []:
                        result = compare_face(encode, unknown)
                        if result != 'unknown':
                            print(result)
                            print('Is listening')
                            isListen = True
                        else:
                            print('unknown face')
                    else:
                        print('No face')
                else:
                    print('Not match')

        cv2.imshow("image", img)
        rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
