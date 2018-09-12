from DriveSerial.constants import *
import sys
from PyQt4 import QtCore, QtGui
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

    th_vector_load = thGenerator()
    th = th_vector_load.gen_SteadySeq(mode=LOADTH, load=[10, 100, 5], speed=None, steadytime=60, direction=DOWNWARDS,
                                      transtime=20)
    print('Vector load th=', th_vector_load.th)

    th_vector_speed = thGenerator()
    th = th_vector_speed.gen_SteadySeq(mode=SPEEDTH, load=[10, 100, 5], speed=[600, 2100, 100], steadytime=30,
                                       direction=UPWARDS, transtime=10)
    print('Vector speed th=', th_vector_speed.th)

    th_vector_speedload = thGenerator()
    th = th_vector_speedload.gen_SteadyTable(mode=SPEEDLOADTH, load=[10, 100, 10], speed=[600, 2000, 200],
                                             steadytime=30, direction=UPWARDS, transtime=0.5)
    print('Vector speed th=', th_vector_speedload.th)

    app = QtGui.QApplication(sys.argv)
    myapp = Main_Window()
    myapp.show()
    sys.exit(app.exec_())
