import face_recognition
import pickle
import os
import sys
import numpy as np

'''
This file is to Encode the face image and save it in a pickle file.
To use this file download your image into image directory and change it name to "<name>0.jpg"
then run the file. The program take name and qty of the image that you want to encode.
'''

name = sys.argv[1]
qty = int(sys.argv[2])
encode = []
for i in range(qty):
    try:
        print(i)
        img_path = os.path.join('image', name+str(i)+'.jpg')
        # load the image
        img = face_recognition.load_image_file(img_path)
        try:
            # encode the face feature and append it to the list
            encode_img = face_recognition.face_encodings(img)[0]
            print(encode_img)
            encode.append(encode_img)
        except:
            pass
    except:
        break
# get average of the face feature and save it as a pickle file
mean_encode = np.sum(encode, axis=0)/len(encode)
encode_path = os.path.join('face_encode', name+'.pickle')
f = open(encode_path, 'wb')
f.write(pickle.dumps(mean_encode))
f.close()
