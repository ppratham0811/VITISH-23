import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
import time
from PyQt5.QtWidgets import QApplication, QDialog
from out_window import Ui_OutputDialog
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QVBoxLayout

class Ui_Dialog123(QDialog):
    def __init__(self):
        super(Ui_Dialog123, self).__init__()
        loadUi(r"C:\Users\Chirag C\vit\docs\face\loading.ui", self)
        self.progressBar.setValue(0)
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(100)
        self._new_window = None
        self.Videocapture_ = None

    def refreshAll(self):
        self.Videocapture_ = "0"

    @pyqtSlot()        
    def run(self):
        value = self.progressBar.value()
        if value < 100:
            value = value + 1
            self.progressBar.setValue(value)
        else:
            self.timer.stop()
        if value == 100:
            self.refreshAll()
            print(self.Videocapture_)
            self.hide()  # hide the main window
            self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog123()
    ui.show()
    sys.exit(app.exec_())
