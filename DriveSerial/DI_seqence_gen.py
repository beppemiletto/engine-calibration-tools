# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DI_seqence_gen.ui'
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

class Ui_Dialog_sequence_gen(object):
    def setupUi(self, Dialog_sequence_gen):
        Dialog_sequence_gen.setObjectName(_fromUtf8("Dialog_sequence_gen"))
        Dialog_sequence_gen.resize(640, 480)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_sequence_gen)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(Dialog_sequence_gen)
        self.widget.setGeometry(QtCore.QRect(20, 16, 260, 217))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_seq_gen = QtGui.QLabel(self.widget)
        self.label_seq_gen.setObjectName(_fromUtf8("label_seq_gen"))
        self.verticalLayout.addWidget(self.label_seq_gen)
        self.listView_types = QtGui.QListView(self.widget)
        self.listView_types.setObjectName(_fromUtf8("listView_types"))
        self.verticalLayout.addWidget(self.listView_types)

        self.retranslateUi(Dialog_sequence_gen)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_sequence_gen.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_sequence_gen.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_sequence_gen)

    def retranslateUi(self, Dialog_sequence_gen):
        Dialog_sequence_gen.setWindowTitle(_translate("Dialog_sequence_gen", "Dialog", None))
        self.label_seq_gen.setText(_translate("Dialog_sequence_gen", "Choose the type of sequence to be generated", None))

