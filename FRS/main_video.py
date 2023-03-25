from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import cvlib as cv
import easygui
from simple_facerec import SimpleFacerec
from playsound import playsound
import datetime as dt
import pygame

lastTime = dt.datetime.now()
currentTime = dt.datetime.now()

pygame.mixer.init()
sound12 = pygame.mixer.Sound("iphone_alarm.mp3") 

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(0)

model = load_model('gender_detection.model')
    
classes = ['man','woman']

while True:
    ret, frame = cap.read()

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        Res1= easygui.enterbox(msg="Your name?")
        img_name = "images/" + Res1 + ".jpg"
        cv2.imwrite(img_name, frame)
        #print("{} written!".format(Res1))
    
    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        
        if(name != "Unknown"):
            cv2.rectangle(frame, (x1-10, y1-10), (x2+10, y2+10), (0, 0, 200), 4)
        else:
             cv2.rectangle(frame, (x1-10, y1-10), (x2+10, y2+10), (0, 255, 0), 4)
        
        face_crop = np.copy(frame[y1: y2,x1: x2])
                
        #cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        
        if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
                continue
            
        # preprocessing for gender detection model
        face_crop = cv2.resize(face_crop, (96,96))
        face_crop = face_crop.astype("float") / 255.0
        face_crop = img_to_array(face_crop)
        face_crop = np.expand_dims(face_crop, axis=0)

        # apply gender detection on face
        conf = model.predict(face_crop)[0] # model.predict return a 2D matrix, ex: [[9.9993384e-01 7.4850512e-05]]

        # get label with max accuracy
        idx = np.argmax(conf)
        label = classes[idx]

        label = "{}".format(label)
        if (len(name) > 0 and name != "Unknown"):
            currentTime = dt.datetime.now()           
            if(currentTime - lastTime).seconds > 1:
                sound12.play()
                lastTime = dt.datetime.now()
                
        # write label and confidence above face rectangle
        if(name == "Unknown"):
            cv2.putText(frame, "Person : ",(540, 370), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, name,(540, 400), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Gender : ",(540, 430), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, label, (540, 460),  cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Person : ",(540, 370), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 200), 2)
            cv2.putText(frame, name,(540, 400), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 200), 2)
        #cv2.rectangle(frame, (530, 350), (640, 480), (0, 0, 200), 4)



    cv2.imshow("Frame", frame)
    
        
cap.release()
cv2.destroyAllWindows()