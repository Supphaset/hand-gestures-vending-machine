import face_recognition
import pickle
import os
import sys
import numpy as np

name = sys.argv[0]
qty = sys.argv[1]
encode = []
for i in range(qty):
    img_path = os.path.join('image', name+str(i)+'.jpg')
    img = face_recognition.load_image_file(img_path)
    encode.append(face_recognition.face_encodings(img))
mean_encode = np.mean(encode, axis=0)
encode_path = os.path.join('face_encode', name+'.pickle')
f = open(name+'.pickle', 'wb')
f.write(pickle.dumps(encode))
f.close()
