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
        self.buttonOKCancel = QtGui.QDialogButtonBox(Dialog_sequence_gen)
        self.buttonOKCancel.setEnabled(True)
        self.buttonOKCancel.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonOKCancel.setOrientation(QtCore.Qt.Horizontal)
        self.buttonOKCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonOKCancel.setObjectName(_fromUtf8("buttonOKCancel"))
        self.layoutWidget = QtGui.QWidget(Dialog_sequence_gen)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 16, 260, 217))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_type = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_type.setMargin(1)
        self.verticalLayout_type.setSpacing(3)
        self.verticalLayout_type.setObjectName(_fromUtf8("verticalLayout_type"))
        self.label_seq_gen = QtGui.QLabel(self.layoutWidget)
        self.label_seq_gen.setObjectName(_fromUtf8("label_seq_gen"))
        self.verticalLayout_type.addWidget(self.label_seq_gen)
        self.listWidget_types = QtGui.QListWidget(self.layoutWidget)
        self.listWidget_types.setObjectName(_fromUtf8("listWidget_types"))
        self.verticalLayout_type.addWidget(self.listWidget_types)
        self.pushButton_open_existing_seq = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_open_existing_seq.setObjectName(_fromUtf8("pushButton_open_existing_seq"))
        self.verticalLayout_type.addWidget(self.pushButton_open_existing_seq)
        self.pushButton_reset_seq_gen = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_reset_seq_gen.setObjectName(_fromUtf8("pushButton_reset_seq_gen"))
        self.verticalLayout_type.addWidget(self.pushButton_reset_seq_gen)
        self.layoutWidget1 = QtGui.QWidget(Dialog_sequence_gen)
        self.layoutWidget1.setGeometry(QtCore.QRect(300, 20, 331, 52))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_seq_name = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_seq_name.setMargin(1)
        self.verticalLayout_seq_name.setSpacing(3)
        self.verticalLayout_seq_name.setObjectName(_fromUtf8("verticalLayout_seq_name"))
        self.label_gen_seq_name = QtGui.QLabel(self.layoutWidget1)
        self.label_gen_seq_name.setObjectName(_fromUtf8("label_gen_seq_name"))
        self.verticalLayout_seq_name.addWidget(self.label_gen_seq_name)
        self.lineEdit_gen_seq_name = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_gen_seq_name.setEnabled(False)
        self.lineEdit_gen_seq_name.setMaxLength(127)
        self.lineEdit_gen_seq_name.setObjectName(_fromUtf8("lineEdit_gen_seq_name"))
        self.verticalLayout_seq_name.addWidget(self.lineEdit_gen_seq_name)
        self.layoutWidget2 = QtGui.QWidget(Dialog_sequence_gen)
        self.layoutWidget2.setGeometry(QtCore.QRect(293, 120, 344, 54))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_slope_time = QtGui.QLabel(self.layoutWidget2)
        self.label_slope_time.setObjectName(_fromUtf8("label_slope_time"))
        self.verticalLayout.addWidget(self.label_slope_time)
        self.doubleSpinBox_slope_time = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.doubleSpinBox_slope_time.setEnabled(False)
        self.doubleSpinBox_slope_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_slope_time.setMaximum(3600.0)
        self.doubleSpinBox_slope_time.setSingleStep(30.0)
        self.doubleSpinBox_slope_time.setProperty("value", 300.0)
        self.doubleSpinBox_slope_time.setObjectName(_fromUtf8("doubleSpinBox_slope_time"))
        self.verticalLayout.addWidget(self.doubleSpinBox_slope_time)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_steady_time = QtGui.QLabel(self.layoutWidget2)
        self.label_steady_time.setObjectName(_fromUtf8("label_steady_time"))
        self.verticalLayout_2.addWidget(self.label_steady_time)
        self.doubleSpinBox_steady_time = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.doubleSpinBox_steady_time.setEnabled(False)
        self.doubleSpinBox_steady_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_steady_time.setMaximum(3600.0)
        self.doubleSpinBox_steady_time.setSingleStep(30.0)
        self.doubleSpinBox_steady_time.setProperty("value", 120.0)
        self.doubleSpinBox_steady_time.setObjectName(_fromUtf8("doubleSpinBox_steady_time"))
        self.verticalLayout_2.addWidget(self.doubleSpinBox_steady_time)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_move_time = QtGui.QLabel(self.layoutWidget2)
        self.label_move_time.setObjectName(_fromUtf8("label_move_time"))
        self.verticalLayout_3.addWidget(self.label_move_time)
        self.doubleSpinBox_move_time = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.doubleSpinBox_move_time.setEnabled(False)
        self.doubleSpinBox_move_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_move_time.setMaximum(600.0)
        self.doubleSpinBox_move_time.setSingleStep(5.0)
        self.doubleSpinBox_move_time.setProperty("value", 20.0)
        self.doubleSpinBox_move_time.setObjectName(_fromUtf8("doubleSpinBox_move_time"))
        self.verticalLayout_3.addWidget(self.doubleSpinBox_move_time)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_res_time = QtGui.QLabel(self.layoutWidget2)
        self.label_res_time.setObjectName(_fromUtf8("label_res_time"))
        self.verticalLayout_4.addWidget(self.label_res_time)
        self.doubleSpinBox_res_time = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.doubleSpinBox_res_time.setEnabled(False)
        self.doubleSpinBox_res_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_res_time.setDecimals(0)
        self.doubleSpinBox_res_time.setMinimum(5.0)
        self.doubleSpinBox_res_time.setMaximum(10000.0)
        self.doubleSpinBox_res_time.setSingleStep(50.0)
        self.doubleSpinBox_res_time.setProperty("value", 50.0)
        self.doubleSpinBox_res_time.setObjectName(_fromUtf8("doubleSpinBox_res_time"))
        self.verticalLayout_4.addWidget(self.doubleSpinBox_res_time)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.layoutWidget3 = QtGui.QWidget(Dialog_sequence_gen)
        self.layoutWidget3.setGeometry(QtCore.QRect(21, 250, 611, 52))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.horizontalLayout_speed = QtGui.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_speed.setObjectName(_fromUtf8("horizontalLayout_speed"))
        self.verticalLayout_rpm_min = QtGui.QVBoxLayout()
        self.verticalLayout_rpm_min.setMargin(1)
        self.verticalLayout_rpm_min.setSpacing(3)
        self.verticalLayout_rpm_min.setObjectName(_fromUtf8("verticalLayout_rpm_min"))
        self.label_speed_min = QtGui.QLabel(self.layoutWidget3)
        self.label_speed_min.setObjectName(_fromUtf8("label_speed_min"))
        self.verticalLayout_rpm_min.addWidget(self.label_speed_min)
        self.spinBox_rpm_min = QtGui.QSpinBox(self.layoutWidget3)
        self.spinBox_rpm_min.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_rpm_min.sizePolicy().hasHeightForWidth())
        self.spinBox_rpm_min.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.spinBox_rpm_min.setFont(font)
        self.spinBox_rpm_min.setFrame(True)
        self.spinBox_rpm_min.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_rpm_min.setMinimum(400)
        self.spinBox_rpm_min.setMaximum(2500)
        self.spinBox_rpm_min.setSingleStep(10)
        self.spinBox_rpm_min.setProperty("value", 1000)
        self.spinBox_rpm_min.setObjectName(_fromUtf8("spinBox_rpm_min"))
        self.verticalLayout_rpm_min.addWidget(self.spinBox_rpm_min)
        self.horizontalLayout_speed.addLayout(self.verticalLayout_rpm_min)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_speed_max = QtGui.QLabel(self.layoutWidget3)
        self.label_speed_max.setObjectName(_fromUtf8("label_speed_max"))
        self.verticalLayout_5.addWidget(self.label_speed_max)
        self.spinBox_rpm_max = QtGui.QSpinBox(self.layoutWidget3)
        self.spinBox_rpm_max.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_rpm_max.sizePolicy().hasHeightForWidth())
        self.spinBox_rpm_max.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.spinBox_rpm_max.setFont(font)
        self.spinBox_rpm_max.setFrame(True)
        self.spinBox_rpm_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_rpm_max.setMinimum(400)
        self.spinBox_rpm_max.setMaximum(2500)
        self.spinBox_rpm_max.setSingleStep(10)
        self.spinBox_rpm_max.setProperty("value", 2000)
        self.spinBox_rpm_max.setObjectName(_fromUtf8("spinBox_rpm_max"))
        self.verticalLayout_5.addWidget(self.spinBox_rpm_max)
        self.horizontalLayout_speed.addLayout(self.verticalLayout_5)
        self.verticalLayout_rpm_step = QtGui.QVBoxLayout()
        self.verticalLayout_rpm_step.setMargin(1)
        self.verticalLayout_rpm_step.setSpacing(3)
        self.verticalLayout_rpm_step.setObjectName(_fromUtf8("verticalLayout_rpm_step"))
        self.label_speed_step = QtGui.QLabel(self.layoutWidget3)
        self.label_speed_step.setObjectName(_fromUtf8("label_speed_step"))
        self.verticalLayout_rpm_step.addWidget(self.label_speed_step)
        self.spinBox_rpm_step = QtGui.QSpinBox(self.layoutWidget3)
        self.spinBox_rpm_step.setEnabled(False)
        self.spinBox_rpm_step.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_rpm_step.setMinimum(25)
        self.spinBox_rpm_step.setMaximum(2500)
        self.spinBox_rpm_step.setSingleStep(10)
        self.spinBox_rpm_step.setProperty("value", 200)
        self.spinBox_rpm_step.setObjectName(_fromUtf8("spinBox_rpm_step"))
        self.verticalLayout_rpm_step.addWidget(self.spinBox_rpm_step)
        self.horizontalLayout_speed.addLayout(self.verticalLayout_rpm_step)
        self.verticalLayout_rpm_direction = QtGui.QVBoxLayout()
        self.verticalLayout_rpm_direction.setMargin(1)
        self.verticalLayout_rpm_direction.setSpacing(3)
        self.verticalLayout_rpm_direction.setObjectName(_fromUtf8("verticalLayout_rpm_direction"))
        self.label_speed_direction = QtGui.QLabel(self.layoutWidget3)
        self.label_speed_direction.setObjectName(_fromUtf8("label_speed_direction"))
        self.verticalLayout_rpm_direction.addWidget(self.label_speed_direction)
        self.horizontalLayout_speed_direction = QtGui.QHBoxLayout()
        self.horizontalLayout_speed_direction.setObjectName(_fromUtf8("horizontalLayout_speed_direction"))
        self.checkBox_rpm_dir_TD = QtGui.QCheckBox(self.layoutWidget3)
        self.checkBox_rpm_dir_TD.setEnabled(False)
        self.checkBox_rpm_dir_TD.setAutoExclusive(False)
        self.checkBox_rpm_dir_TD.setObjectName(_fromUtf8("checkBox_rpm_dir_TD"))
        self.horizontalLayout_speed_direction.addWidget(self.checkBox_rpm_dir_TD)
        self.checkBox_rpm_dir_BU = QtGui.QCheckBox(self.layoutWidget3)
        self.checkBox_rpm_dir_BU.setEnabled(False)
        self.checkBox_rpm_dir_BU.setChecked(True)
        self.checkBox_rpm_dir_BU.setAutoExclusive(False)
        self.checkBox_rpm_dir_BU.setObjectName(_fromUtf8("checkBox_rpm_dir_BU"))
        self.horizontalLayout_speed_direction.addWidget(self.checkBox_rpm_dir_BU)
        self.verticalLayout_rpm_direction.addLayout(self.horizontalLayout_speed_direction)
        self.horizontalLayout_speed.addLayout(self.verticalLayout_rpm_direction)
        self.verticalLayout_rpm_repetition = QtGui.QVBoxLayout()
        self.verticalLayout_rpm_repetition.setMargin(1)
        self.verticalLayout_rpm_repetition.setSpacing(3)
        self.verticalLayout_rpm_repetition.setObjectName(_fromUtf8("verticalLayout_rpm_repetition"))
        self.label_speed_repetition = QtGui.QLabel(self.layoutWidget3)
        self.label_speed_repetition.setObjectName(_fromUtf8("label_speed_repetition"))
        self.verticalLayout_rpm_repetition.addWidget(self.label_speed_repetition)
        self.horizontalLayout_speed_repetition = QtGui.QHBoxLayout()
        self.horizontalLayout_speed_repetition.setObjectName(_fromUtf8("horizontalLayout_speed_repetition"))
        self.checkBox_rpm_repetition = QtGui.QCheckBox(self.layoutWidget3)
        self.checkBox_rpm_repetition.setEnabled(False)
        self.checkBox_rpm_repetition.setAutoExclusive(False)
        self.checkBox_rpm_repetition.setObjectName(_fromUtf8("checkBox_rpm_repetition"))
        self.horizontalLayout_speed_repetition.addWidget(self.checkBox_rpm_repetition)
        self.verticalLayout_rpm_repetition.addLayout(self.horizontalLayout_speed_repetition)
        self.horizontalLayout_speed.addLayout(self.verticalLayout_rpm_repetition)
        self.layoutWidget4 = QtGui.QWidget(Dialog_sequence_gen)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 310, 611, 53))
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.horizontalLayout_load = QtGui.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_load.setObjectName(_fromUtf8("horizontalLayout_load"))
        self.horizontalLayout_LOAD = QtGui.QHBoxLayout()
        self.horizontalLayout_LOAD.setObjectName(_fromUtf8("horizontalLayout_LOAD"))
        self.verticalLayout_load_min = QtGui.QVBoxLayout()
        self.verticalLayout_load_min.setMargin(1)
        self.verticalLayout_load_min.setSpacing(3)
        self.verticalLayout_load_min.setObjectName(_fromUtf8("verticalLayout_load_min"))
        self.label_load_min = QtGui.QLabel(self.layoutWidget4)
        self.label_load_min.setObjectName(_fromUtf8("label_load_min"))
        self.verticalLayout_load_min.addWidget(self.label_load_min)
        self.doubleSpinBox_load_min = QtGui.QDoubleSpinBox(self.layoutWidget4)
        self.doubleSpinBox_load_min.setEnabled(False)
        self.doubleSpinBox_load_min.setFrame(True)
        self.doubleSpinBox_load_min.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_load_min.setDecimals(1)
        self.doubleSpinBox_load_min.setSingleStep(0.0)
        self.doubleSpinBox_load_min.setProperty("value", 10.0)
        self.doubleSpinBox_load_min.setObjectName(_fromUtf8("doubleSpinBox_load_min"))
        self.verticalLayout_load_min.addWidget(self.doubleSpinBox_load_min)
        self.horizontalLayout_LOAD.addLayout(self.verticalLayout_load_min)
        self.verticalLayout_load_max = QtGui.QVBoxLayout()
        self.verticalLayout_load_max.setMargin(1)
        self.verticalLayout_load_max.setSpacing(3)
        self.verticalLayout_load_max.setObjectName(_fromUtf8("verticalLayout_load_max"))
        self.label_load_max = QtGui.QLabel(self.layoutWidget4)
        self.label_load_max.setObjectName(_fromUtf8("label_load_max"))
        self.verticalLayout_load_max.addWidget(self.label_load_max)
        self.doubleSpinBox_load_max = QtGui.QDoubleSpinBox(self.layoutWidget4)
        self.doubleSpinBox_load_max.setEnabled(False)
        self.doubleSpinBox_load_max.setFrame(True)
        self.doubleSpinBox_load_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_load_max.setDecimals(1)
        self.doubleSpinBox_load_max.setProperty("value", 90.0)
        self.doubleSpinBox_load_max.setObjectName(_fromUtf8("doubleSpinBox_load_max"))
        self.verticalLayout_load_max.addWidget(self.doubleSpinBox_load_max)
        self.horizontalLayout_LOAD.addLayout(self.verticalLayout_load_max)
        self.verticalLayout_load_step = QtGui.QVBoxLayout()
        self.verticalLayout_load_step.setMargin(1)
        self.verticalLayout_load_step.setSpacing(3)
        self.verticalLayout_load_step.setObjectName(_fromUtf8("verticalLayout_load_step"))
        self.label_load_step = QtGui.QLabel(self.layoutWidget4)
        self.label_load_step.setObjectName(_fromUtf8("label_load_step"))
        self.verticalLayout_load_step.addWidget(self.label_load_step)
        self.doubleSpinBox_load_step = QtGui.QDoubleSpinBox(self.layoutWidget4)
        self.doubleSpinBox_load_step.setEnabled(False)
        self.doubleSpinBox_load_step.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_load_step.setDecimals(1)
        self.doubleSpinBox_load_step.setObjectName(_fromUtf8("doubleSpinBox_load_step"))
        self.verticalLayout_load_step.addWidget(self.doubleSpinBox_load_step)
        self.horizontalLayout_LOAD.addLayout(self.verticalLayout_load_step)
        self.verticalLayout_rpm_direction_2 = QtGui.QVBoxLayout()
        self.verticalLayout_rpm_direction_2.setMargin(1)
        self.verticalLayout_rpm_direction_2.setSpacing(3)
        self.verticalLayout_rpm_direction_2.setObjectName(_fromUtf8("verticalLayout_rpm_direction_2"))
        self.label_load_direction = QtGui.QLabel(self.layoutWidget4)
        self.label_load_direction.setObjectName(_fromUtf8("label_load_direction"))
        self.verticalLayout_rpm_direction_2.addWidget(self.label_load_direction)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.checkBox_load_dir_TD = QtGui.QCheckBox(self.layoutWidget4)
        self.checkBox_load_dir_TD.setEnabled(False)
        self.checkBox_load_dir_TD.setAutoExclusive(False)
        self.checkBox_load_dir_TD.setObjectName(_fromUtf8("checkBox_load_dir_TD"))
        self.horizontalLayout_4.addWidget(self.checkBox_load_dir_TD)
        self.checkBox_load_dir_BU = QtGui.QCheckBox(self.layoutWidget4)
        self.checkBox_load_dir_BU.setEnabled(False)
        self.checkBox_load_dir_BU.setChecked(True)
        self.checkBox_load_dir_BU.setAutoExclusive(False)
        self.checkBox_load_dir_BU.setObjectName(_fromUtf8("checkBox_load_dir_BU"))
        self.horizontalLayout_4.addWidget(self.checkBox_load_dir_BU)
        self.verticalLayout_rpm_direction_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_LOAD.addLayout(self.verticalLayout_rpm_direction_2)
        self.horizontalLayout_load.addLayout(self.horizontalLayout_LOAD)
        self.verticalLayout_load_repetition = QtGui.QVBoxLayout()
        self.verticalLayout_load_repetition.setMargin(1)
        self.verticalLayout_load_repetition.setSpacing(3)
        self.verticalLayout_load_repetition.setObjectName(_fromUtf8("verticalLayout_load_repetition"))
        self.label_load_repetition = QtGui.QLabel(self.layoutWidget4)
        self.label_load_repetition.setObjectName(_fromUtf8("label_load_repetition"))
        self.verticalLayout_load_repetition.addWidget(self.label_load_repetition)
        self.horizontalLayout_load_repetition = QtGui.QHBoxLayout()
        self.horizontalLayout_load_repetition.setObjectName(_fromUtf8("horizontalLayout_load_repetition"))
        self.checkBox_load_repetition = QtGui.QCheckBox(self.layoutWidget4)
        self.checkBox_load_repetition.setEnabled(False)
        self.checkBox_load_repetition.setAutoExclusive(False)
        self.checkBox_load_repetition.setObjectName(_fromUtf8("checkBox_load_repetition"))
        self.horizontalLayout_load_repetition.addWidget(self.checkBox_load_repetition)
        self.verticalLayout_load_repetition.addLayout(self.horizontalLayout_load_repetition)
        self.horizontalLayout_load.addLayout(self.verticalLayout_load_repetition)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.buttonOKCancel.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(Dialog_sequence_gen)
        QtCore.QObject.connect(self.buttonOKCancel, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_sequence_gen.accept)
        QtCore.QObject.connect(self.buttonOKCancel, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_sequence_gen.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_sequence_gen)

    def retranslateUi(self, Dialog_sequence_gen):
        Dialog_sequence_gen.setWindowTitle(_translate("Dialog_sequence_gen", "Dialog", None))
        self.label_seq_gen.setText(_translate("Dialog_sequence_gen", "Choose the type of sequence to be generated", None))
        self.pushButton_open_existing_seq.setText(_translate("Dialog_sequence_gen", "Open existing sequence for edit", None))
        self.pushButton_reset_seq_gen.setText(_translate("Dialog_sequence_gen", "Reset all choice (and input)", None))
        self.label_gen_seq_name.setToolTip(_translate("Dialog_sequence_gen", "Insert the name you want assign to the sequence to be generated", None))
        self.label_gen_seq_name.setText(_translate("Dialog_sequence_gen", "Name of the sequence to be generated", None))
        self.lineEdit_gen_seq_name.setText(_translate("Dialog_sequence_gen", "SeqType", None))
        self.label_slope_time.setText(_translate("Dialog_sequence_gen", "Slope time [s]", None))
        self.label_steady_time.setText(_translate("Dialog_sequence_gen", "Steady time [s]", None))
        self.label_move_time.setText(_translate("Dialog_sequence_gen", "Move time [s]", None))
        self.label_res_time.setText(_translate("Dialog_sequence_gen", "dt res. [ms]", None))
        self.doubleSpinBox_res_time.setSuffix(_translate("Dialog_sequence_gen", " ms", None))
        self.label_speed_min.setText(_translate("Dialog_sequence_gen", "RPM min", None))
        self.label_speed_max.setText(_translate("Dialog_sequence_gen", "RPM max", None))
        self.label_speed_step.setText(_translate("Dialog_sequence_gen", "RPM step", None))
        self.label_speed_direction.setText(_translate("Dialog_sequence_gen", "Sequence or slope direction", None))
        self.checkBox_rpm_dir_TD.setText(_translate("Dialog_sequence_gen", "Top>Down", None))
        self.checkBox_rpm_dir_BU.setText(_translate("Dialog_sequence_gen", "Bottom>Up", None))
        self.label_speed_repetition.setText(_translate("Dialog_sequence_gen", "Sequence or slope repetition", None))
        self.checkBox_rpm_repetition.setText(_translate("Dialog_sequence_gen", "Go and Back", None))
        self.label_load_min.setText(_translate("Dialog_sequence_gen", "LOAD min", None))
        self.label_load_max.setText(_translate("Dialog_sequence_gen", "LOAD max", None))
        self.label_load_step.setText(_translate("Dialog_sequence_gen", "LOAD step", None))
        self.label_load_direction.setText(_translate("Dialog_sequence_gen", "Sequence or slope direction", None))
        self.checkBox_load_dir_TD.setText(_translate("Dialog_sequence_gen", "Top>Down", None))
        self.checkBox_load_dir_BU.setText(_translate("Dialog_sequence_gen", "Bottom>Up", None))
        self.label_load_repetition.setText(_translate("Dialog_sequence_gen", "Sequence or slope repetition", None))
        self.checkBox_load_repetition.setText(_translate("Dialog_sequence_gen", "Go and Back", None))

