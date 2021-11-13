import cv2 
from HandTrackingModule import HandDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import face_recognition
import pickle

def get_database():
    from pymongo import MongoClient
    import certifi
    import pymongo

    CONNECTION_STRING = 'mongodb+srv://mechatronic:mechatronic@cluster0.el0zv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING,tlsCAFile=certifi.where())

    return client['mechatronic']

def recognize_face(img,link_enc):
    print('before')
    rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    try:
        unknown_face_encoding = face_recognition.face_encodings(rgb_img)[0]
        results = face_recognition.compare_faces(link_enc,unknown_face_encoding)
        print(results)
    except IndexError:
        print('no Face')

def face_recognize(img):
    rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    try:
        return face_recognition.face_encodings(rgb_img)[0]
    except IndexError:
        return []

def upadate_item(item,db):
    print(item)
    temp = db.find_one({"name":item})
    if temp['qty']>0:
        db.update_one({"name":item},{'$inc': {'qty':-1,'used':+1}})
    else:
        print('Item out of stock')

if __name__ == '__main__':
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate =32
    rawCapture = PiRGBArray(camera, size=(640,480))
    time.sleep(0.1)
    
    link = face_recognition.load_image_file('link0.jpg')
    link_enc = face_recognition.face_encodings(link)[0]
    print(link_enc)

    # connect to the database
    dbname = get_database()
    db = dbname['items']
    #define camera and Hand detector and set to detect only 1 hand
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.5, maxHands =1)

    isListen = False

    for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):
        #get image from camera
        img = frame.array
        hands, img = detector.findHands(img)
        # check if the picture have hand or not
        if hands != []:
            # detect finger in the hand
            finger = detector.fingersUp(hands[0])

            if isListen: # hand action
                if finger == [1, 1, 1, 1, 1]:
                    upadate_item('Item_5',db)
                    isListen = False
                elif finger == [0,1,1,1,1]:
                    upadate_item('Item_4',db)
                    isListen = False
                elif finger == [0,1,1,1,0]:
                    upadate_item('Item_3',db)
                    isListen = False
                elif finger == [0,1,1,0,0]:
                    upadate_item('Item_2',db)
                    isListen = False
                elif finger == [0,1,0,0,0]:
                    upadate_item('Item_1',db)
                    isListen = False
            else:
                if finger == [1,0,0,0,0]: # user show thumb up start listening to the hand action
                    unknown = face_recognize(img)
                    if unknown != []:
                        result = face_recognition.compare_faces([link_enc],unknown)
                        print('Is listening')
                        isListen = True
                else:
                    print('Not match')
            
        
        cv2.imshow("image",img)
        rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

