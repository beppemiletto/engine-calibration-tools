from DriveSerial.thGenerator import *
from DriveSerial.constants import *
import sys
from PyQt4 import QtCore, QtGui
from DriveSerial.UI_DriveTestBed import Ui_TBDriveClient


## class for building the GUI
class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TBDriveClient()
        self.ui.setupUi(self)
        self.filename = None
        # here we connect signals with our slots
        QtCore.QObject.connect(self.ui.actionOpen, QtCore.SIGNAL("activated()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("clicked()"), self.file_save)

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
            file.write(self.ui.editor_window.toPlainText())
            file.close()


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
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
