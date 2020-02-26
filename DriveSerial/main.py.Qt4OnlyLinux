from DriveSerial.constants import *
import sys
from PyQt4 import QtCore, QtGui
import pickle
from DriveSerial.UI_DriveTestBed import Ui_TBDriveClient
from DriveSerial.DI_seqence_gen import Ui_Dialog_sequence_gen
from DriveSerial.thGenerator import *

## classes for building the GUIs

class ui_First(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TBDriveClient()
        self.ui.setupUi(self)
        self.filename = None
        self.gen_res = False


class ui_seq_gen(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog_sequence_gen()
        self.ui.setupUi(self)
        self.value_changed=False
        seq_types = SEQ_TYPES_DESCR
        for key, type in seq_types.items():
            item = QtGui.QListWidgetItem(type['name'])
            tooltip = type['description']
            self.ui.listWidget_types.addItem(item)

        self.ui.listWidget_types.currentItemChanged.connect(self.on_type_changed)
        self.ui.buttonOKCancel.rejected.connect(self.cancel_gen)
        self.ui.buttonOKCancel.accepted.connect(self.accept_gen)
        # self.ui.spinBox_rpm_min.changeEvent.connect(self.on_value_changed)
        # self.ui.spinBox_rpm_max.changeEvent.connect(self.on_value_changed)

    def cancel_gen(self):
        print("Sequence generation cancelled")

    def accept_gen(self):
        print("Sequence generation accepted")
        self.rpm_min = self.ui.spinBox_rpm_min.value()
        self.rpm_max = self.ui.spinBox_rpm_max.value()
        self.rpm_step = self.ui.spinBox_rpm_step.value()
        self.rpm_dir_TD = self.ui.checkBox_rpm_dir_TD.checkState()
        self.rpm_dir_BU = self.ui.checkBox_rpm_dir_BU.checkState()
        self.rpm_repetition = self.ui.checkBox_rpm_repetition.checkState()

        self.move_time = self.ui.doubleSpinBox_move_time.value()
        self.steady_time = self.ui.doubleSpinBox_steady_time.value()
        self.slope_time = self.ui.doubleSpinBox_slope_time.value()
        self.res_time = self.ui.doubleSpinBox_res_time.value()

        self.gen_seq_name = self.ui.lineEdit_gen_seq_name.text()

        self.load_min = self.ui.doubleSpinBox_load_min.value()
        self.load_max = self.ui.doubleSpinBox_load_max.value()
        self.load_step = self.ui.doubleSpinBox_load_step.value()
        self.load_dir_TD = self.ui.checkBox_load_dir_TD.checkState()
        self.load_dir_BU = self.ui.checkBox_load_dir_BU.checkState()
        self.load_repetition = self.ui.checkBox_load_repetition.checkState()



        if self.gen_seq_type_selected == LOADTH:
            if self.load_dir_BU:
                first_direction = UPWARDS
            elif self.load_dir_TD:
                first_direction = DOWNWARDS
            else:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("Not determined direction")
                msg.setInformativeText("You have not specify correctly the direction of the time history. Default UPWARD (bottom-up) assumed")
                msg.setWindowTitle("Warning!")
                msg.setDetailedText("The details are as follows:")
                msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                retval = msg.exec_()
                print
                "value of pressed message box button:", retval
                first_direction = UPWARDS

            th_vector = thGenerator()
            self.th = th_vector.gen_SteadySeq(mode=LOADTH,
                                                   load=[self.load_min, self.load_max, self.load_step],
                                                   speed=None,
                                                   steadytime=self.steady_time,
                                                   direction=first_direction,
                                                   transtime=self.move_time,
                                                   repetition = self.load_repetition,
                                                   name = self.gen_seq_name)

            print(self.th)

        if self.gen_seq_type_selected == SPEEDTH:
            if self.rpm_dir_BU:
                first_direction = UPWARDS
            elif self.rpm_dir_TD:
                first_direction = DOWNWARDS
            else:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("Not determined direction")
                msg.setInformativeText("You have not specify correctly the direction of the time history. Default UPWARD (bottom-up) assumed")
                msg.setWindowTitle("Warning!")
                msg.setDetailedText("The details are as follows:")
                msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                retval = msg.exec_()
                print
                "value of pressed message box button:", retval
                first_direction = UPWARDS

            th_vector = thGenerator()
            self.th = th_vector.gen_SteadySeq( mode = SPEEDTH,
                                                   load=None,
                                                   speed=[self.rpm_min, self.rpm_max, self.rpm_step],
                                                   steadytime=self.steady_time,
                                                   direction=first_direction,
                                                   transtime=self.move_time,
                                                   repetition = self.rpm_repetition,
                                                   name = self.gen_seq_name )

            print(self.th)
        try:
            if len(self.th) > 1:
                print('save the time history {}.ext'.format(self.gen_seq_name))
                try:
                    filename= self.gen_seq_name+'.pickle'
                    with open(filename, 'wb') as handle:
                        pickle.dump(self.th, handle, protocol=pickle.HIGHEST_PROTOCOL)
                except:
                    print("file recording problems!!")

        except:
            print("nothing to save")

    def on_type_changed(self,curr, prev):


        if prev == None:
            print("type changed to {}:{} {}".format(curr.text(),self.ui.listWidget_types.currentRow() ,curr.toolTip()))

        else:
            print("type changed from {} to {}:{} {}".format(prev.text(),curr.text(),self.ui.listWidget_types.currentRow() ,curr.toolTip()))
            if self.value_changed:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("Values already changed")
                msg.setInformativeText("You have already modified some values in controls.Do you want cancel them")
                msg.setWindowTitle("Warning!")
                msg.setDetailedText("The details are as follows:")
                msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

                retval = msg.exec_()
                print
                "value of pressed message box button:", retval
            self.disable_all_control()
        self.gen_seq_type_selected = self.ui.listWidget_types.currentRow()+1

        self.ui.doubleSpinBox_res_time.setEnabled(True)
        if self.gen_seq_type_selected == SPEEDTH:
            self.ui.spinBox_rpm_min.setEnabled(True)
            self.ui.spinBox_rpm_max.setEnabled(True)
            self.ui.spinBox_rpm_step.setEnabled(True)
            self.ui.doubleSpinBox_move_time.setEnabled(True)
            self.ui.doubleSpinBox_steady_time.setEnabled(True)
            self.ui.lineEdit_gen_seq_name.setEnabled(True)
            self.ui.checkBox_rpm_dir_TD.setEnabled(True)
            self.ui.checkBox_rpm_dir_BU.setEnabled(True)
            self.ui.checkBox_rpm_repetition.setEnabled(True)

        elif self.gen_seq_type_selected == LOADTH:
            self.ui.doubleSpinBox_load_min.setEnabled(True)
            self.ui.doubleSpinBox_load_max.setEnabled(True)
            self.ui.doubleSpinBox_load_step.setEnabled(True)
            self.ui.doubleSpinBox_move_time.setEnabled(True)
            self.ui.doubleSpinBox_steady_time.setEnabled(True)
            self.ui.lineEdit_gen_seq_name.setEnabled(True)
            self.ui.checkBox_load_dir_TD.setEnabled(True)
            self.ui.checkBox_load_dir_BU.setEnabled(True)
            self.ui.checkBox_load_repetition.setEnabled(True)

        elif self.gen_seq_type_selected == LOADSPEEDTH or self.gen_seq_type_selected == SPEEDLOADTH:
            self.ui.doubleSpinBox_load_min.setEnabled(True)
            self.ui.doubleSpinBox_load_max.setEnabled(True)
            self.ui.doubleSpinBox_load_step.setEnabled(True)
            self.ui.doubleSpinBox_move_time.setEnabled(True)
            self.ui.doubleSpinBox_steady_time.setEnabled(True)
            self.ui.lineEdit_gen_seq_name.setEnabled(True)
            self.ui.checkBox_load_dir_TD.setEnabled(True)
            self.ui.checkBox_load_dir_BU.setEnabled(True)

            self.ui.spinBox_rpm_min.setEnabled(True)
            self.ui.spinBox_rpm_max.setEnabled(True)
            self.ui.spinBox_rpm_step.setEnabled(True)
            # self.ui.doubleSpinBox_move_time.setEnabled(True)
            # self.ui.doubleSpinBox_steady_time.setEnabled(True)
            # self.ui.lineEdit_gen_seq_name.setEnabled(True)
            self.ui.checkBox_rpm_dir_TD.setEnabled(True)
            self.ui.checkBox_rpm_dir_BU.setEnabled(True)
        elif self.gen_seq_type_selected == LOADSLOPE :
            self.ui.doubleSpinBox_slope_time.setEnabled(True)
            self.ui.doubleSpinBox_load_min.setEnabled(True)
            self.ui.doubleSpinBox_load_max.setEnabled(True)
            self.ui.doubleSpinBox_steady_time.setEnabled(True)
            self.ui.lineEdit_gen_seq_name.setEnabled(True)
            self.ui.checkBox_load_dir_TD.setEnabled(True)
            self.ui.checkBox_load_dir_BU.setEnabled(True)
            self.ui.checkBox_load_repetition.setEnabled(True)

        elif self.gen_seq_type_selected == SPEEDSLOPE:
            self.ui.doubleSpinBox_slope_time.setEnabled(True)

            self.ui.doubleSpinBox_steady_time.setEnabled(True)
            self.ui.lineEdit_gen_seq_name.setEnabled(True)

            self.ui.spinBox_rpm_min.setEnabled(True)
            self.ui.spinBox_rpm_max.setEnabled(True)
            self.ui.checkBox_rpm_dir_TD.setEnabled(True)
            self.ui.checkBox_rpm_dir_BU.setEnabled(True)
            self.ui.checkBox_rpm_repetition.setEnabled(True)



    def on_value_changed(self):
        self.value_changed=True

    def disable_all_control(self):

        self.ui.spinBox_rpm_min.setEnabled(False)
        self.ui.spinBox_rpm_max.setEnabled(False)
        self.ui.spinBox_rpm_step.setEnabled(False)
        self.ui.checkBox_rpm_dir_TD.setEnabled(False)
        self.ui.checkBox_rpm_dir_BU.setEnabled(False)
        self.ui.checkBox_rpm_repetition.setEnabled(False)

        self.ui.doubleSpinBox_move_time.setEnabled(False)
        self.ui.doubleSpinBox_steady_time.setEnabled(False)
        self.ui.doubleSpinBox_slope_time.setEnabled(False)
        self.ui.doubleSpinBox_res_time.setEnabled(False)

        self.ui.lineEdit_gen_seq_name.setEnabled(False)

        self.ui.doubleSpinBox_load_min.setEnabled(False)
        self.ui.doubleSpinBox_load_max.setEnabled(False)
        self.ui.doubleSpinBox_load_step.setEnabled(False)
        self.ui.checkBox_load_dir_TD.setEnabled(False)
        self.ui.checkBox_load_dir_BU.setEnabled(False)
        self.ui.checkBox_load_repetition.setEnabled(False)

class Main_Window(ui_First):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)

        # here we connect signals with our slots
        QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("activated()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("activated()"), self.file_save)
        QtCore.QObject.connect(self.ui.action_Generate, QtCore.SIGNAL("activated()"), self.gen_sequence)


        # here we define children dialogues windows
        self.dialog_seq_gen= Seq_gen(self)


    def on_pushButton_clicked(self):
        self.dialog.show()

    def gen_sequence(self):



        self.dialog_seq_gen.show()

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            text = open(self.filename).read()
            self.ui.textEdit.setText(text)

    def file_save(self):
        from os.path import isfile
        if isfile(self.filename):
            file = open(self.filename, 'w')
            file.write(self.ui.textEdit.toPlainText())
            file.close()



class Seq_gen(ui_seq_gen):
    def __init__(self, parent=None):
        super(Seq_gen, self).__init__(parent)



if __name__ == '__main__':
    """ Only for testing functions"""

    # th_vector_load = thGenerator()
    # th = th_vector_load.gen_SteadySeq(mode=LOADTH, load=[10, 100, 5], speed=None, steadytime=60, direction=DOWNWARDS,
    #                                   transtime=20)
    # print('Vector load th=', th_vector_load.th)
    #
    # th_vector_speed = thGenerator()
    # th = th_vector_speed.gen_SteadySeq(mode=SPEEDTH, load=[10, 100, 5], speed=[600, 2100, 100], steadytime=30,
    #                                    direction=UPWARDS, transtime=10)
    # print('Vector speed th=', th_vector_speed.th)
    #
    # th_vector_speedload = thGenerator()
    # th = th_vector_speedload.gen_SteadyTable(mode=SPEEDLOADTH, load=[10, 100, 10], speed=[600, 2000, 200],
    #                                          steadytime=30, direction=UPWARDS, transtime=0.5)
    # print('Vector speed th=', th_vector_speedload.th)

    app = QtGui.QApplication(sys.argv)
    myapp = Main_Window()
    myapp.show()
    sys.exit(app.exec_())
