import cv2
from HandTrackingModule import HandDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from mongo_db import get_database
import time
import face_recognition
import pickle
import os
import RPi.GPIO as GPIO
from time import sleep
import sys

# GPIO Pin
DIR1 = 0
DIR2 = 0
DIR3 = 0
DIR4 = 0
DIR5 = 0
STEP1 = 0
STEP2 = 0
STEP3 = 0
STEP4 = 0
STEP5 = 0
LED1 = 0
LED2 = 0
LED3 = 0
CW = 1
CCW = 0
SPR = 48  # Steps per rev (360/7.5)

# Set GPIO Pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(STEP3, GPIO.OUT)
GPIO.setup(STEP4, GPIO.OUT)
GPIO.setup(STEP5, GPIO.OUT)
GPIO.output(DIR1, CW)
GPIO.output(DIR2, CW)
GPIO.output(DIR3, CW)
GPIO.output(DIR4, CW)
GPIO.output(DIR5, CW)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)

delay = 0.0208


def motor_1rev(step):
    step_pin = [STEP1, STEP2, STEP3, STEP4, STEP5]
    for i in range(SPR):
        GPIO.output(step_pin[step], GPIO.HIGH)
        sleep(delay)
        GPIO.output(step_pin[step], GPIO.LOW)
        sleep(delay)


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
    items = ['Item_1', 'Item_2', 'Item_3', 'Item_4', 'Item_5']
    print(items[item])
    temp = db.find_one({"name": items[item]})
    print(temp)
    if temp['qty'] > 0:
        motor_1rev(item)
        db.update_one({"name": items[item]}, {'$inc': {'qty': -1, 'used': +1}})
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


def compare_face(encode, face, threshold=0.5):
    name = list(encode.keys())
    print(name)
    face_encode = list(encode.values())
    result = list(face_recognition.face_distance(face_encode, face))
    print(result)
    min_result = min(result)
    print(min_result)
    if min_result <= threshold:
        return name[result.index(min_result)]
    else:
        return 'unknown'


def main():
    cap = cv2.VideoCapture(0)
    def change_res(width, height):
        cap.set(3, width)
        cap.set(4, height)

    change_res(640, 480)
    # camera = PiCamera()
    # camera.resolution = (640, 480)
    # camera.framerate = 32
    # rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    encode = get_encode()

    # connect to the database
    dbname = get_database()
    db = dbname['items']
    # define Hand detector and set to detect only 1 hand
    detector = HandDetector(detectionCon=0.5, maxHands=1)

    isListen = False
    isFace = False
    faceKnown = False

    # for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        # get image from camera
        # img = frame.array
    while True:
        scuess, img = cap.read()
        hands, img = detector.findHands(img)
        # check if the picture have hand or not
        if hands != []:
            # detect finger in the hand
            finger = detector.fingersUp(hands[0])
            LED1_state = finger == [1, 0, 0, 0, 0] or isListen
            LED2_state = isFace or isListen
            LED3_state = faceKnown or isListen
            GPIO.output(LED1,LED1_state)
            GPIO.output(LED2,LED2_state)
            GPIO.output(LED3,LED3_state)
            if isListen:  # hand action
                if finger == [1, 1, 1, 1, 1]:
                    upadate_item(4, db)
                    isListen = False
                elif finger == [0, 1, 1, 1, 1]:
                    upadate_item(3, db)
                    isListen = False
                elif finger == [0, 1, 1, 1, 0]:
                    upadate_item(2, db)
                    isListen = False
                elif finger == [0, 1, 1, 0, 0]:
                    upadate_item(1, db)
                    isListen = False
                elif finger == [0, 1, 0, 0, 0]:
                    upadate_item(0, db)
                    isListen = False
            else:
                # user show thumb up start listening to the hand action
                if finger == [1, 0, 0, 0, 0]:
                    unknown = face_recognize(img)
                    if unknown != []:
                        isFace = True
                        result = compare_face(encode, unknown)
                        if result != 'unknown':
                            faceKnown = True
                            GPIO.output(LED2,GPIO.HIGH)
                            print(result)
                            print('Is listening')
                            isListen = True
                        else:
                            faceKnown = False
                            print('unknown face')
                    else:
                        isFace = False
                        print('No face')
                else:
                    print('Not match')

        cv2.imshow("image", img)
        # rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
