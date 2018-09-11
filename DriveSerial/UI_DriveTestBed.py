# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_DriveTestBed.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TBDriveClient(object):
    def setupUi(self, TBDriveClient):
        TBDriveClient.setObjectName(_fromUtf8("TBDriveClient"))
        TBDriveClient.resize(800, 600)
        self.centralwidget = QtGui.QWidget(TBDriveClient)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 430, 771, 121))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(520, 10, 269, 67))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.PlayButton = QtGui.QPushButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("play_button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayButton.setIcon(icon)
        self.PlayButton.setObjectName(_fromUtf8("PlayButton"))
        self.gridLayout.addWidget(self.PlayButton, 0, 0, 1, 1)
        self.PauseButton = QtGui.QPushButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pause_button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PauseButton.setIcon(icon1)
        self.PauseButton.setObjectName(_fromUtf8("PauseButton"))
        self.gridLayout.addWidget(self.PauseButton, 0, 1, 1, 1)
        self.StopButton = QtGui.QPushButton(self.widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("stop_button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StopButton.setIcon(icon2)
        self.StopButton.setObjectName(_fromUtf8("StopButton"))
        self.gridLayout.addWidget(self.StopButton, 0, 2, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 3)
        self.progressBar.raise_()
        self.PlayButton.raise_()
        self.PauseButton.raise_()
        self.StopButton.raise_()
        self.progressBar.raise_()
        self.textEdit.raise_()
        TBDriveClient.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TBDriveClient)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        TBDriveClient.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TBDriveClient)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TBDriveClient.setStatusBar(self.statusbar)
        self.actionPlaySequence = QtGui.QAction(TBDriveClient)
        self.actionPlaySequence.setObjectName(_fromUtf8("actionPlaySequence"))
        self.actionNew = QtGui.QAction(TBDriveClient)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(TBDriveClient)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(TBDriveClient)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionExit = QtGui.QAction(TBDriveClient)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(TBDriveClient)
        QtCore.QObject.connect(self.PlayButton, QtCore.SIGNAL(_fromUtf8("released()")), self.actionPlaySequence.trigger)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("activated()")), TBDriveClient.close)
        QtCore.QMetaObject.connectSlotsByName(TBDriveClient)

    def retranslateUi(self, TBDriveClient):
        TBDriveClient.setWindowTitle(_translate("TBDriveClient", "MainWindow", None))
        self.PlayButton.setText(_translate("TBDriveClient", "Play", None))
        self.PauseButton.setText(_translate("TBDriveClient", "Pause", None))
        self.StopButton.setText(_translate("TBDriveClient", "STOP", None))
        self.menuFile.setTitle(_translate("TBDriveClient", "File", None))
        self.actionPlaySequence.setText(_translate("TBDriveClient", "PlaySequence", None))
        self.actionPlaySequence.setToolTip(_translate("TBDriveClient", "Activate the Driving Sequence ", None))
        self.actionPlaySequence.setShortcut(_translate("TBDriveClient", "Space", None))
        self.actionNew.setText(_translate("TBDriveClient", "New", None))
        self.actionOpen.setText(_translate("TBDriveClient", "Open", None))
        self.actionSave.setText(_translate("TBDriveClient", "Save", None))
        self.actionExit.setText(_translate("TBDriveClient", "Exit", None))

