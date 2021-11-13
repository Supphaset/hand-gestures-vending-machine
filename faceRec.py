import face_recognition
import pickle

link = []
golf = []
for i in range(3):
    link_img = face_recognition.load_image_file('link'+str(i)+'.jpg')
    golf_img = face_recognition.load_image_file('golf'+str(i)+'.jpg')
    print(link_img.shape)
    print(golf_img.shape)

    link.append(face_recognition.face_encodings(link_img))
    golf.append(face_recognition.face_encodings(golf_img))

f= open('link.pickle','wb')
f.write(pickle.dumps(link))
f.close()
f= open('golf.pickle','wb')
f.write(pickle.dumps(golf))
f.close()



    