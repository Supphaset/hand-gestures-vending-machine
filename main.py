import cv2
from HandTrackingModule import HandDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from mongo_db import get_database
import time
import face_recognition
import pickle
import os
import sys
from rpi_gpio import motor_1rev, set_led

# define LED Pin
LED1 = 24
LED2 = 25
LED3 = 26


def face_recognize(img):
    # convert the image from bgr to rgb
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    try:
        # return the face feature
        return face_recognition.face_encodings(rgb_img)[0]
    except IndexError:
        return []


def upadate_item(item, db):
    '''This funciton update the item in the database'''
    items = ['Item_1', 'Item_2', 'Item_3', 'Item_4', 'Item_5']
    print(items[item])
    # find the data from the data base
    temp = db.find_one({"name": items[item]})
    print(temp)
    if temp['qty'] > 0:
        # make the stepper motor spin 1 rev
        motor_1rev(item)
        # update the item in the database
        db.update_one({"name": items[item]}, {'$inc': {'qty': -1, 'used': +1}})
    else:
        print('Item out of stock')


def get_encode():
    '''This function get the encoded face feature that have been saved in pickle file and put it in the dict with the name be the key'''
    encode = {}
    # go through the face_encode directory
    for filename in os.listdir('face_encode'):
        if filename.endswith(".pickle"):
            # read the pickle file and put it into the dict with the name of the file be key
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
    # compare the face feature of unknown with the face feature download from the pickle file
    result = list(face_recognition.face_distance(face_encode, face))
    print(result)
    min_result = min(result)
    print(min_result)
    # if the result more than the threshold return name with smallest value if not return unknown
    if min_result <= threshold:
        return name[result.index(min_result)]
    else:
        return 'unknown'


def change_res(width, height, cap):
    # set the resolution of the video
    cap.set(3, width)
    cap.set(4, height)


def main():
    '''using usb camera'''
    cap = cv2.VideoCapture(0)

    change_res(640, 480, cap)
    '''If using pi camera uncomment the code below'''
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
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    isListen = False
    isFace = False
    faceKnown = False
    '''If using pi camera uncomment the code below'''
    # for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    # get image from camera
    # img = frame.array
    '''using usb camera'''
    while True:
        scuess, img = cap.read()
        hands, img = detector.findHands(img)
        # check if the picture have hand or not
        if hands != []:
            # detect finger in the hand
            finger = detector.fingersUp(hands[0])
            # check is the hand action is a thumb up
            isThumb = finger == [1, 0, 0, 0, 0] or finger == [0, 0, 0, 0, 1]
            LED1_state = isThumb or isListen
            LED2_state = isFace or isListen
            LED3_state = faceKnown or isListen
            # set state of the LED
            set_led(LED1, LED1_state)
            set_led(LED2, LED2_state)
            set_led(LED3, LED3_state)
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
                if isListen == False:
                    isFace = False
                    faceKnown = False
            else:
                # user show thumb up start listening to the hand action
                if isThumb:
                    unknown = face_recognize(img)
                    if unknown != []:
                        # face is detected
                        isFace = True
                        result = compare_face(encode, unknown)
                        if result != 'unknown':
                            # the face is known
                            faceKnown = True
                            print(result)
                            print('Is listening')
                            isListen = True
                        else:
                            # the face is unknown
                            faceKnown = False
                            print('unknown face')
                    else:
                        # can not detect the face
                        isFace = False
                        print('No face')
                else:
                    # not thumb
                    print('Not match')

        cv2.imshow("image", img)
        # rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
