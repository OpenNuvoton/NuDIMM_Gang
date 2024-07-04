import sys 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QThread, QObject, QRegExp, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator

from checker_ui import Ui_Dialog

class Dialog_Ui_4(QDialog, Ui_Dialog):

    def __init__(self, config = [], parent=None):
        super(Dialog_Ui_4, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        opts = QtCore.Qt.FindChildrenRecursively
        spinboxes = self.findChildren(QtWidgets.QSpinBox, options=opts)
        for box in spinboxes:
            box.wheelEvent = lambda *event: None
        
        self.lineEdit_serial.setValidator(QRegExpValidator(QRegExp("[ -~]{8,12}"), self))
        self.lineEdit_serial.textChanged.connect(self.text_changed)
        self.spinBox_length.valueChanged.connect(self.text_changed)
        self.text_changed()
        
    def text_changed(self):
        serial_len = self.spinBox_length.value()
        if len(self.lineEdit_serial.text()) == serial_len:
            self.label_check.setText('Check result: <font color="green">Pass<font>')
        else:
            self.label_check.setText('Check result: <font color="red">Fail<font>')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    
    myapp = Dialog_Ui_4()
    myapp.show()
    
    sys.exit(app.exec_())