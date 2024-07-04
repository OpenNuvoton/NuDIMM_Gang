from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QThread, QObject, QRegExp, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QStyledItemDelegate, QLineEdit, QMessageBox

from config_spd_2 import Ui_Dialog
from list_table import dimm_type, pmic, ts5, module_speed

class Dialog_Ui_2(QDialog, Ui_Dialog):

    def __init__(self, config = [], parent=None):
        super(Dialog_Ui_2, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        opts = QtCore.Qt.FindChildrenRecursively
        spinboxes = self.findChildren(QtWidgets.QSpinBox, options=opts)
        for box in spinboxes:
            box.wheelEvent = lambda *event: None
            
        comboboxes = self.findChildren(QtWidgets.QComboBox, options=opts)
        for box in comboboxes:
            box.wheelEvent = lambda *event: None
            
        self.wconfig = config
        self.update_list()
        
    def update_list(self):
        #used byte: 2 ~ 7, 24 ~ 28, 30 ~ 37, (38 ~ 47), 192, 194 ~ 213, 234 ~ 235, 512 ~ 550, 552 ~ 553 
        if self.getValue(2) == 0x12: self.label_2.setText("DDR5 SDRAM");
        elif self.getValue(2) == 0x14: self.label_2.setText("DDR5 NVDIMM-P");
        else: self.label_2.setText("Unknown or not support");
        self.label_4.setText(dimm_type[min(11, self.getBits(3, 0, 4))]);
        if self.getBits(4, 0, 5) == 0: self.label_6.setText("No Defined");
        else: self.label_6.setText(f'{4 * min(8, self.getBits(4, 0, 5))} GB');
        self.label_8.setText(f'{min(8, 1 + self.getBits(234, 3, 3))} Ranks');
        module_speed_len = len(module_speed)
        for i in range(module_speed_len):
            if (self.getValue(24) == module_speed[i][1] and self.getValue(25) == module_speed[i][2] and self.getValue(26) == module_speed[i][3]
                and self.getValue(27) == module_speed[i][4] and self.getValue(28) == module_speed[i][5]):
                self.label_10.setText(f'{module_speed[i][0]} MHz');
                break
        t = 2 ** min(3, self.getBits(235, 5, 3))
        t2 = 4 * min(2, self.getBits(235, 3, 2)) + 8 * (2 ** min(3, self.getBits(235, 0, 3)))
        self.label_12.setText(f'{t} ch, {t * t2} bit');
        self.label_14.setText("1.1V/1.1V/1.8V");
        t = 4 * (2 ** min(3, self.getBits(6, 5, 3)))
        self.label_16.setText(f'{int(4 * min(8, self.getBits(4, 0, 5)) / t)} Gb');
        self.label_18.setText(f'{t} bit');
        self.label_20.setText(f'{2 ** min(2, self.getBits(7, 0, 2))} banks, {2 ** min(3, self.getBits(7, 5, 3))} groups');
        self.label_22.setText(f'{min(2, self.getBits(5, 0, 2)) + 16}');
        self.label_24.setText(f'{self.getBits(5, 5, 1) + 10}');
        clstr = ""
        for i in range(0, 40):
            t, t2  = divmod(i, 8)
            if self.getBits(24 + t, t2, 1) == 1: clstr = clstr + f'{i * 2 + 20}' + " ";
        self.label_26.setText(clstr);
        self.label_28.setText(f'{self.getValue(31) * 256 + self.getValue(30)}');
        self.label_30.setText(f'{self.getValue(33) * 256 + self.getValue(32)}');
        self.label_32.setText(f'{self.getValue(35) * 256 + self.getValue(34)}');
        self.label_34.setText(f'{self.getValue(37) * 256 + self.getValue(36)}');
        self.label_36.setText(hex(self.calculate_CRC()))
        t = self.getValue(517) * 256 * 256 * 256 + self.getValue(518) * 256 * 256 + self.getValue(519) * 256 + self.getValue(520)
        self.label_38.setText(hex(t))
        pstr = ""
        for ti in range (0,30):
            pstr = pstr + chr(self.getValue(521 + ti))
        self.label_40.setText(pstr)
        self.label_42.setText(hex(self.getValue(553) * 256 + self.getValue(552)))
        self.label_44.setText(hex(self.getValue(513) * 256 + self.getValue(512)))
        self.label_46.setText(hex(self.getValue(514)))
        try:
            t = int(format(self.getValue(515), 'x'))
            t2 = int(format(self.getValue(516), 'x'))
        except Exception as e:
            t = 0
            t2 = 0
        self.label_48.setText(f'{t}{t2}')
        self.label_53.setText(f'{self.getBits(192, 4, 4)}.{self.getBits(192, 0 ,4)}')
        self.label_55.setText(hex(self.getValue(195) * 256 + self.getValue(194)))
        self.label_57.setText(f'{self.getBits(197, 4, 4)}.{self.getBits(197, 0, 4)}')
        if self.getBits(196, 0, 4) == 0: self.label_59.setText("SPD5118")
        elif self.getBits(196, 0, 4) == 1: self.label_59.setText("ESPD5216")
        self.label_61.setText(hex(self.getValue(199) * 256 + self.getValue(198)))
        self.label_63.setText(f'{self.getBits(201, 4, 4)}.{self.getBits(201, 0, 4)}')
        self.label_65.setText(pmic[min(6, self.getBits(200, 0, 4))])
        self.label_67.setText(hex(self.getValue(203) * 256 + self.getValue(202)))
        self.label_69.setText(f'{self.getBits(205, 4, 4)}.{self.getBits(205, 0, 4)}')
        self.label_71.setText(pmic[min(6, self.getBits(204, 0, 4))])
        self.label_73.setText(hex(self.getValue(207) * 256 + self.getValue(206)))
        self.label_75.setText(f'{self.getBits(209, 4, 4)}.{self.getBits(209, 0, 4)}')
        self.label_77.setText(pmic[min(6, self.getBits(208, 0, 4))])
        self.label_79.setText(hex(self.getValue(211) * 256 + self.getValue(210)))
        self.label_81.setText(f'{self.getBits(213, 4, 4)}.{self.getBits(213, 0, 4)}')
        self.label_83.setText(ts5[min(3, self.getBits(212, 0, 4))])
        
    def getValue(self, num):
        return self.wconfig[num]
        
    def getBits(self, num, lsb, bits):
        _mask = (1 << bits) - 1
        value = (self.wconfig[num] & (_mask << lsb)) >> lsb
        return value
        
    def calculate_CRC(self):
        crc = 0
        index = 0
        while (index <= 509):
            crc = crc ^ (self.wconfig[index] << 8)
            index = index + 1
            for i in range(0,8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = (crc << 1)
        return crc & 0xFFFF
        
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    myapp = Dialog_Ui_2()
    myapp.show()
    
    sys.exit(app.exec_())