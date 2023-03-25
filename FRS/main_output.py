from PyQt5.QtWebEngineWidgets import QWebEngineView
import datetime
import folium
from random import randint
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from collections import deque
import io
from PyQt5 import QtWidgets, QtCore
from simple_facerec import SimpleFacerec
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import datetime as dt
from tensorflow.keras.preprocessing.image import img_to_array

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi(r"C:\Users\Chirag C\vit\docs\face\outputwindow.ui", self)
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
        self.gridLayout.addWidget(self.graphwidget1, 0, 0, 1, 3)
        
        self.graphwidget2 = PlotWidget(title="Women Count")
        x1_axis = self.graphwidget2.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (seconds)')
        y1_axis = self.graphwidget2.getAxis('left')
        y1_axis.setLabel(text='Number of Women')
        self.gridLayout_2.addWidget(self.graphwidget2, 0, 0, 1, 3)
        
        self.current_timer_graph = None
        self.graph_lim = 15
        self.deque_timestamp = deque([], maxlen=self.graph_lim+20)
    
        my_map2 = folium.Map(location = [12.840829280387942, 80.15340683965688],zoom_start = 12)
        folium.CircleMarker(location = [12.840829280387942, 80.15340683965688],radius = 50, popup = ' FRI ').add_to(my_map2)       
        # save map data to data object
        data = io.BytesIO()
        my_map2.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.gridLayout_4.addWidget(webView)     
        
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points
        self.z1 = [randint(0,100) for _ in range(100)]  # 100 data points
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.data_line =  self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.data_line =  self.graphwidget2.plot(self.x, self.z1, pen=pen1)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        #self.current_timer_graph.timeout.connect(self.update_cpu)
        
    def update_plot_data(self):
        self.timestamp += 1
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.
        
        self.z1 = self.z1[1:]  # Remove the first
        self.z1.append( randint(0,100)) 
          # Update the data.
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.graphwidget1.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.y[-self.graph_lim:]), max(self.y[-self.graph_lim:])])
        self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.graphwidget2.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.z1[-self.graph_lim:]), max(self.z1[-self.graph_lim:])])
        self.graphwidget2.plot(self.x, self.z1, pen=pen1)

    @pyqtSlot()
    def startVideo(self, camera_name):
        self.timer = QTimer(self)  # Create Timer        
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(1)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame,face_locations,face_names):

        # face recognition
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
            """
            if (len(name) > 0 and name != "Unknown"):
                currentTime = dt.datetime.now()
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
        return frame


    def update_frame(self):
        sfr = SimpleFacerec()
        sfr.load_encoding_images("images/")
        self.capture = cv2.VideoCapture(0)
        frame = self.capture.read()
        face_locations, face_names = sfr.detect_known_faces(frame)
        self.displayImage(frame, face_locations, face_names, 1)

    def displayImage(self, frame, face_locations, face_names, window=1):
        image = cv2.resize(frame, (640, 480))
        try:
            image = self.face_rec_(image,face_locations, face_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
