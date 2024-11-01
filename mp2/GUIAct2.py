# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUIAct2UYShhV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.TimerSwitch = QPushButton(self.centralwidget)
        self.TimerSwitch.setObjectName(u"TimerSwitch")
        self.TimerSwitch.setGeometry(QRect(580, 140, 181, 131))
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(40, 350, 461, 191))
        self.splitter.setOrientation(Qt.Horizontal)
        self.LED1Switch = QPushButton(self.splitter)
        self.LED1Switch.setObjectName(u"LED1Switch")
        self.splitter.addWidget(self.LED1Switch)
        self.LED2BrightnessDial = QDial(self.splitter)
        self.LED2BrightnessDial.setObjectName(u"LED2BrightnessDial")
        self.splitter.addWidget(self.LED2BrightnessDial)
        self.Timer = QLCDNumber(self.centralwidget)
        self.Timer.setObjectName(u"Timer")
        self.Timer.setGeometry(QRect(580, 60, 181, 51))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 60, 531, 211))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.PicLabel = QLabel(self.layoutWidget)
        self.PicLabel.setObjectName(u"PicLabel")

        self.horizontalLayout_2.addWidget(self.PicLabel)

        self.TextLabel = QLabel(self.layoutWidget)
        self.TextLabel.setObjectName(u"TextLabel")

        self.horizontalLayout_2.addWidget(self.TextLabel)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.TimerSwitch.setText(QCoreApplication.translate("MainWindow", u"Temporizador Cambio Im\u00e1genes On / Off", None))
        self.LED1Switch.setText(QCoreApplication.translate("MainWindow", u"Primer LED On / Off", None))
        self.PicLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.TextLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

