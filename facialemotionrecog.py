# code from: https://github.com/akmadan/Emotion_Detection_CNN

from keras.models import load_model
from time import sleep
from keras_preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

class EmotionRecognition(object):
    def __init__(self):
        self.emotion = None
    
    def scanFace(self):
        face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        classifier =load_model(r'model.h5')

        emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()
            labels = []
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = classifier.predict(roi)[0]
                    label=emotion_labels[prediction.argmax()] # returns dominant emotion
                    label_position = (x,y)
                    cv2.putText(frame, "Press 'q' to capture your emotion!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,6,(255,0,255),5)
                    self.emotion = label
                else:
                    cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.imshow('Emotion Detector',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return self.emotion

        
    
    def getEmotion(self):
        return self.emotion