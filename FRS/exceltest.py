import time
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import numpy as np
from PyQt5.QtWebEngineWidgets import QWebEngineView
import datetime
import folium
import openpyxl
from random import randint
from collections import deque
import io
from PyQt5 import QtWidgets, QtCore
import os
import csv
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import datetime as dt
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import cvlib as cv
import easygui
from simple_facerec import SimpleFacerec
from playsound import playsound
import datetime as dt
import pygame
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt, QDate

class Ui_OutputDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Ui_OutputDialog, self).__init__(*args, **kwargs)
        self.ui = loadUi(r"C:\Users\Chirag C\vit\docs\face\outputwindow.ui", self)
        self.traces = dict()
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.image = None
        self.timestamp = 0
        self.timeaxis = []
        self.graphwidget1 = PlotWidget(title="Men Count")
        x1_axis = self.graphwidget1.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (seconds)')
        y1_axis = self.graphwidget1.getAxis('left')
        y1_axis.setLabel(text='Number of Men')
        self.ui.gridLayout.addWidget(self.graphwidget1, 0, 0, 1, 3)
        self.val = randint(76,95)
        self.graphwidget2 = PlotWidget(title="Women Count")
        x1_axis = self.graphwidget2.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (seconds)')
        y1_axis = self.graphwidget2.getAxis('left')
        y1_axis.setLabel(text='Number of Women')
        wb = openpyxl.load_workbook("Detection.xlsx")
        ws = wb["Sheet1"]
        self.ui.gridLayout_2.addWidget(self.graphwidget2, 0, 0, 1, 3)
        
        self.current_timer_graph = None
        self.graph_lim = 15
        self.deque_timestamp = deque([], maxlen=self.graph_lim+20)
        
        
        my_map2 = folium.Map(location = [12.840829280387942, 80.15340683965688],zoom_start = 12)
        #folium.CircleMarker(location = [12.840829280387942, 80.15340683965688],radius = 50, popup = ' FRI ').add_to(my_map2)       
        # save map data to data object
        data = io.BytesIO()
        my_map2.save(data, close_file=False)
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        self.ui.gridLayout_4.addWidget(self.webView)      
        
        self.x = list(range(10))
        self.y = [randint(0,10) for _ in range(10)]
        self.z1 = [randint(0,10) for _ in range(10)]
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.data_line =  self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.data_line =  self.graphwidget2.plot(self.x, self.z1, pen=pen1)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        #self.current_timer_graph.timeout.connect(self.update_cpu)
        
    def update_plot_data(self):
        self.timestamp += 1
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append( randint(0,10)) 
        
        self.z1 = self.z1[1:]  
        self.z1.append( randint(0,10)) 
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.graphwidget1.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.y[-self.graph_lim:]), max(self.y[-self.graph_lim:])])
        self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.graphwidget2.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.z1[-self.graph_lim:]), max(self.z1[-self.graph_lim:])])
        self.graphwidget2.plot(self.x, self.z1, pen=pen1)
        
    def update_plot_data(self):
        self.timestamp += 1
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append( randint(0,10))
        
        self.z1 = self.z1[1:]
        self.z1.append( randint(0,10)) 
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.graphwidget1.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.y[-self.graph_lim:]), max(self.y[-self.graph_lim:])])
        self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.graphwidget2.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.z1[-self.graph_lim:]), max(self.z1[-self.graph_lim:])])
        self.graphwidget2.plot(self.x, self.z1, pen=pen1)
            
    @pyqtSlot()
    def startVideo(self, camera_name):
        lastTime = dt.datetime.now()
        currentTime = dt.datetime.now()

        pygame.mixer.init()
        sound12 = pygame.mixer.Sound("iphone_alarm.mp3") 

        sfr = SimpleFacerec()
        sfr.load_encoding_images("images/")

        self.capture = cv2.VideoCapture(0)

        model = load_model('gender_detection.model')
    
        classes = ['man','woman']

        while True:
            ret, frame = self.capture.read()
            
            current_time = QTime.currentTime()
            label_time = current_time.toString('hh:mm:ss')
            self.label_16.setText(label_time)
            current_date = QDate.currentDate()
            label_date = current_date.toString('ddd dd MMMM yyyy')
            self.label_17.setText(label_date)
            
            
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                exit
            elif k%256 == 32:
                # SPACE pressed
                Res1= easygui.enterbox(msg="Your name?")
                img_name = "images/" + Res1 + ".jpg"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(Res1))
    
            # Detect Faces
            face_locations, face_names = sfr.detect_known_faces(frame)
            print(face_names)
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
                #conf = model.predict(face_crop)[0] # model.predict return a 2D matrix, ex: [[9.9993384e-01 7.4850512e-05]]

                # get label with max accuracy
                #idx = np.argmax(conf)
                #label = classes[idx]

                #label = "{}".format(label)
                if (len(name) > 0 and name != "Unknown"):
                    currentTime = dt.datetime.now()
                    cv2.rectangle(frame, (x1-10, y1-40), (x2+10, y1-10), (0, 0, 200), 4)
                    v1 = name + "  " + str(self.val)
                    cv2.putText(frame, v1, (x1, y1-15),  cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 200), 2)                                    
                    if(currentTime - lastTime).seconds > 1:
                        sound12.play()
                        lastTime = dt.datetime.now()
                """
                # write label and confidence above face rectangle
                if(name == "Unknown"):
                    cv2.putText(frame, "Person : ",(540, 370), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, name,(540, 400), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
                    #cv2.putText(frame, "Gender : ",(540, 430), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
                    #cv2.putText(frame, label, (540, 460),  cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Person : ",(540, 370), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 200), 2)
                    cv2.putText(frame, name,(540, 400), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 200), 2)
                #cv2.rectangle(frame, (530, 350), (640, 480), (0, 0, 200), 4)
                """ 
            image = cv2.resize(frame, (640, 480))
            qformat = QImage.Format_Indexed8
            if len(image.shape) == 3:
                if image.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
            outImage = outImage.rgbSwapped()

            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
            for name in face_names:
                if(name != "Unknown"):
                    self.label_2.setText(name)
                    self.label_6.setText(str(self.val))
                    self.val = randint(76,95)
                    self.label_7.setText(current_time.toString('hh:mm:ss'))
                    if(name == "Messi"):
                        img_name = "images/" + name + ".webp"
                    else:
                        img_name = "images/" + name + ".jpg"
                    pixmap = QPixmap(img_name)
                    self.ui.label_8.setPixmap(pixmap)
                    self.ui.label_8.setScaledContents(True)
                    self.ui.gridLayout_4.removeWidget(self.webView) 
                    self.my_map2 = folium.Map(location = [12.840829280387942, 80.15340683965688],zoom_start = 13)
                    folium.CircleMarker(location = [12.840829280387942, 80.15340683965688],radius = 50, popup = ' FRI ').add_to(self.my_map2)       
                    data = io.BytesIO()
                    self.my_map2.save(data, close_file=False)
                    self.webView = QWebEngineView()
                    self.webView.setHtml(data.getvalue().decode())
                    self.ui.gridLayout_4.addWidget(self.webView) 
                    jump = 1
                    naqw1 = 'A'+str(jump)
                    self.ws[naqw1] = name
                    
                    jump = jump + 1
                    self.wb.save("Detection.xlsx")
                
            
    
        self.capture.release()
        cv2.destroyAllWindows()