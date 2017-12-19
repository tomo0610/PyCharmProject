# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test.ui'
#
# Created: Sat Nov 25 20:52:37 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TestWindow(object):
    def setupUi(self, TestWindow):
        TestWindow.setObjectName("TestWindow")
        TestWindow.setEnabled(True)
        TestWindow.resize(800, 600)
        TestWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtGui.QWidget(TestWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 510, 75, 23))
        self.pushButton.setObjectName("pushButton")
        TestWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TestWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        TestWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TestWindow)
        self.statusbar.setObjectName("statusbar")
        TestWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TestWindow)
        QtCore.QMetaObject.connectSlotsByName(TestWindow)

    def retranslateUi(self, TestWindow):
        TestWindow.setWindowTitle(QtGui.QApplication.translate("TestWindow", "TestWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TestWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

