from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtWidgets import QDialog,QMessageBox
from PyQt5.uic import loadUi
import sys  # We need sys so that we can pass argv to QApplication
import os
import folium
import io
from PyQt5.QtWebEngineWidgets import QWebEngineView
from collections import deque
from random import randint

class Ui_OutputDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Ui_OutputDialog, self).__init__(*args, **kwargs)
        self.ui = loadUi(r"C:\Users\chirag c\Desktop\docs\face\outputwindow.ui", self)
        self.traces = dict()
        self.timestamp = 0
        self.timeaxis = []
        self.graphwidget1 = PlotWidget(title="Men Count")
        x1_axis = self.graphwidget1.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (seconds)')
        y1_axis = self.graphwidget1.getAxis('left')
        y1_axis.setLabel(text='Number of Men')
        self.ui.gridLayout.addWidget(self.graphwidget1, 0, 0, 1, 3)
        
        self.graphwidget2 = PlotWidget(title="Women Count")
        x1_axis = self.graphwidget2.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (seconds)')
        y1_axis = self.graphwidget2.getAxis('left')
        y1_axis.setLabel(text='Number of Women')
        self.ui.gridLayout_2.addWidget(self.graphwidget2, 0, 0, 1, 3)
        
        self.current_timer_graph = None
        self.graph_lim = 10
        self.deque_timestamp = deque([], maxlen=self.graph_lim+20)
        
        my_map2 = folium.Map(location = [12.840829280387942, 80.15340683965688],zoom_start = 12)
        folium.CircleMarker(location = [12.840829280387942, 80.15340683965688],radius = 50, popup = ' FRI ').add_to(my_map2)       
        # save map data to data object
        data = io.BytesIO()
        my_map2.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.ui.gridLayout_4.addWidget(webView)
        
        
        self.x = list(range(10))  # 100 time points
        self.y = [randint(0,10) for _ in range(10)]  # 100 data points
        self.z1 = [randint(0,10) for _ in range(10)]  # 100 data points
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
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,10))  # Add a new random value.
        
        self.z1 = self.z1[1:]  # Remove the first
        self.z1.append( randint(0,10)) 
          # Update the data.
        pen = pg.mkPen(color=(255, 0, 0))
        pen1 = pg.mkPen(color=(0, 0, 255))
        self.graphwidget1.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.y[-self.graph_lim:]), max(self.y[-self.graph_lim:])])
        self.graphwidget1.plot(self.x, self.y, pen=pen)
        self.graphwidget2.setRange(xRange=[min(self.x[-self.graph_lim:]), max(self.x[-self.graph_lim:])], yRange=[min(self.z1[-self.graph_lim:]), max(self.z1[-self.graph_lim:])])
        self.graphwidget2.plot(self.x, self.z1, pen=pen1)
        image1 = QPixmap("images\Messi.webp")
        gri
        
app = QtWidgets.QApplication(sys.argv)
w = Ui_OutputDialog()
w.show()
sys.exit(app.exec_())