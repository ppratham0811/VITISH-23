# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Chirag C\vit\docs\face\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(676, 326)
        Dialog.setMinimumSize(QtCore.QSize(508, 259))
        Dialog.setMaximumSize(QtCore.QSize(1900, 1600))
        Dialog.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Chirag C\\vit\\docs\\face\\icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("background-color:rgb(250,250,250);")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 391, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logolabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.logolabel.setMaximumSize(QtCore.QSize(1000, 1001))
        self.logolabel.setText("")
        self.logolabel.setPixmap(QtGui.QPixmap("c:\\Users\\Chirag C\\vit\\docs\\face\\logo.png"))
        self.logolabel.setScaledContents(True)
        self.logolabel.setObjectName("logolabel")
        self.horizontalLayout.addWidget(self.logolabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(480, 270, 93, 36))
        self.runButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Roboto Condensed Light")
        font.setPointSize(13)
        self.runButton.setFont(font)
        self.runButton.setIconSize(QtCore.QSize(30, 20))
        self.runButton.setObjectName("runButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(420, 60, 231, 201))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setIndent(20)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(430, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "R-Surveillance System"))
        self.runButton.setText(_translate("Dialog", "Start"))
        self.label.setText(_translate("Dialog", "The most advanced Surveillance system create to moniter and detected terrorist, wanted criminals and other dangerous people using the principles of deep learning and facial recognition."))
        self.label_2.setText(_translate("Dialog", "RS-System"))
import resource_rc