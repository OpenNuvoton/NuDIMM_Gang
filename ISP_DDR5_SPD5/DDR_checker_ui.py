import sys 

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QDate, QThread, QObject, QRegularExpression, Qt, Signal, Slot
from PySide6.QtWidgets import QDialog, QStyledItemDelegate, QLineEdit, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator

from checker_ui import Ui_Dialog

class Dialog_Ui_4(QDialog, Ui_Dialog):

    data_updated = Signal(object)

    def __init__(self, serial_num = [], parent=None):
        super(Dialog_Ui_4, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.serial_num = serial_num
        
        opts = QtCore.Qt.FindChildrenRecursively
        spinboxes = self.findChildren(QtWidgets.QSpinBox, options=opts)
        for box in spinboxes:
            box.wheelEvent = lambda *event: None
        
        for i in range(1, 6):        
            self.__dict__[f'lineEdit_serial_{i%5}'].setValidator(QRegularExpressionValidator(QRegularExpression("[ -~]{8,12}"), self))
            if self.serial_num[(i - 1)%5]:
                self.__dict__[f'lineEdit_serial_{i%5}'].setText("{:08X}".format(self.serial_num[(i - 1)%5]))
                
        self.pushButton.clicked.connect(self.update_serial_num)
        
    def update_serial_num(self):
        for i in range(1, 6):        
            if self.__dict__[f'lineEdit_serial_{i%5}'].hasAcceptableInput():
                self.serial_num[(i - 1)%5] = int(self.__dict__[f'lineEdit_serial_{i%5}'].text(), 16)
    
        self.data_updated.emit(self.serial_num)
        self.accept() 
                

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    
    myapp = Dialog_Ui_4()
    myapp.show()
    
    sys.exit(app.exec_())