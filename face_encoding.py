import face_recognition
import pickle
import os
import sys
import numpy as np

name = sys.argv[1]
qty = int(sys.argv[2])
encode = []
for i in range(qty):
    try:
        print(i)
        img_path = os.path.join('image', name+str(i)+'.jpg')
        img = face_recognition.load_image_file(img_path)
        try:
            encode_img = face_recognition.face_encodings(img)[0]
            print(encode_img)
            encode.append(encode_img)
        except:
            pass
    except:
        break

mean_encode = np.sum(encode, axis=0)/len(encode)
encode_path = os.path.join('face_encode', name+'.pickle')
f = open(encode_path, 'wb')
f.write(pickle.dumps(mean_encode))
f.close()
