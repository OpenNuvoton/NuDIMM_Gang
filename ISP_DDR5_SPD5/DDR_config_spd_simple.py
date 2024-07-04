import sys 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QThread, QObject, QRegExp, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator

from simple_config_spd import Ui_Dialog
from datetime import datetime, timedelta

def get_first_day_of_week(year, week_number):
    # ISO 8601 week date system: Week 1 is the week with the first Thursday of the year
    # January 4th is always in week 1.
    fourth_jan = datetime(year, 1, 4)
    delta_days = timedelta(days=(week_number-1)*7 - fourth_jan.weekday())
    first_day_of_week = fourth_jan + delta_days
    return QDate(first_day_of_week.year, first_day_of_week.month, first_day_of_week.day)

def qdate_to_year_week(qdate):
    # Convert QDate to datetime.date
    date_py = datetime(qdate.year(), qdate.month(), qdate.day())
    # Get ISO year, week number, and weekday
    
    iso_year, iso_week, _ = date_py.isocalendar()
    return iso_year, iso_week    
class Dialog_Ui_3(QDialog, Ui_Dialog):

    data_updated = pyqtSignal(object)

    def __init__(self, config = [], parent=None):
        super(Dialog_Ui_3, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        opts = QtCore.Qt.FindChildrenRecursively
        spinboxes = self.findChildren(QtWidgets.QSpinBox, options=opts)
        for box in spinboxes:
            box.wheelEvent = lambda *event: None
            
        comboboxes = self.findChildren(QtWidgets.QComboBox, options=opts)
        for box in comboboxes:
            box.wheelEvent = lambda *event: None
            
        self.lineEdit_521.setValidator(QRegExpValidator(QRegExp("[ -~]+$"), self))
        
        self.wconfig = config
        self.getConfig()

        self.all_ff = True
        for i in range(0, 1024):
            if self.wconfig[i] != 0xFF:
                self.all_ff == False
                break
                
        crc_16 = self.calculate_CRC()
        #print(crc_16 & 0xFF, self.wconfig[510])
        #print(crc_16 >> 8, self.wconfig[511] )

    def getConfig(self):
        #used byte: 2 ~ 7, 24 ~ 28, 30 ~ 37, (38 ~ 47), 192, 194 ~ 213, 234 ~ 235, 512 ~ 550, 551 ~ 553 
        #byte_2
        if self.getValue(2) == 0x12: self.comboBox_2.setCurrentIndex(0)
        if self.getValue(2) == 0x14: self.comboBox_2.setCurrentIndex(1)
        #byte_3
        if self.getBits(3, 7, 1) == 0: self.comboBox_3.setCurrentIndex(0)
        if self.getBits(3, 4, 4) == 0x1001: self.comboBox_3.setCurrentIndex(1)
        if self.getBits(3, 4, 4) == 0x1010: self.comboBox_3.setCurrentIndex(2)
        t = self.getBits(3, 0, 4)
        self.comboBox_3_1.setCurrentIndex(t - 1 if t <= 8 else t - 2)
        #byte_4
        self.comboBox_4.setCurrentIndex(self.getBits(4, 5, 3))
        self.comboBox_4_1.setCurrentIndex(self.getBits(4, 0, 5))
        #byte_5
        self.comboBox_5.setCurrentIndex(self.getBits(5, 5, 1) * 3 + self.getBits(5, 0, 2))
        #byte_6
        self.comboBox_6.setCurrentIndex(self.getBits(6, 5, 3))
        #byte_7
        self.comboBox_7.setCurrentIndex(self.getBits(7, 5, 3))
        self.comboBox_7_1.setCurrentIndex(self.getBits(7, 0, 2))
        #byte_24 ~ byte_28
        #self.spinBox_24.setValue(self.getValue(24))
        #self.spinBox_25.setValue(self.getValue(25))
        #self.spinBox_26.setValue(self.getValue(26))
        #self.spinBox_27.setValue(self.getValue(27))
        #self.spinBox_28.setValue(self.getValue(28))
        for i in range(0, 40):
            row, column  = divmod(i, 8)
            getattr(self, f'checkBox_{i+1}').setChecked(self.getBits(24 + row, column, 1))
        #byte_30 ~ byte_53
        self.spinBox_30.setValue(self.getValue(31) * 256 + self.getValue(30))
        self.spinBox_32.setValue(self.getValue(33) * 256 + self.getValue(32))
        self.spinBox_34.setValue(self.getValue(35) * 256 + self.getValue(34))
        self.spinBox_36.setValue(self.getValue(37) * 256 + self.getValue(36))
        self.spinBox_38.setValue(self.getValue(39) * 256 + self.getValue(38))
        self.spinBox_40.setValue(self.getValue(41) * 256 + self.getValue(40))
        self.spinBox_42.setValue(self.getValue(43) * 256 + self.getValue(42))
        self.spinBox_44.setValue(self.getValue(45) * 256 + self.getValue(44))
        self.spinBox_46.setValue(self.getValue(47) * 256 + self.getValue(46))
        #byte_192
        self.lineEdit_192.setValue(self.getBits(192, 4, 4), self.getBits(192, 0 ,4))
        #byte_194 ~ byte_197
        self.lineEdit_194.setValue(self.getValue(195) * 256 + self.getValue(194))
        self.checkBox_196.setChecked(self.getBits(196, 7, 1))
        self.comboBox_196_1.setCurrentIndex(self.getBits(196, 0, 4))
        self.lineEdit_197.setValue(self.getBits(197, 4, 4), self.getBits(197, 0 ,4))
        #byte_198 ~ byte_201
        self.lineEdit_198.setValue(self.getValue(199) * 256 + self.getValue(198))
        self.checkBox_200.setChecked(self.getBits(200, 7, 1))
        self.comboBox_200_1.setCurrentIndex(self.getBits(200, 0, 4))
        self.lineEdit_201.setValue(self.getBits(201, 4, 4), self.getBits(201, 0 ,4))
        #byte_202 ~ byte_205
        self.lineEdit_202.setValue(self.getValue(203) * 256 + self.getValue(202))
        self.checkBox_204.setChecked(self.getBits(204, 7, 1))
        self.comboBox_204_1.setCurrentIndex(self.getBits(204, 0, 4))
        self.lineEdit_205.setValue(self.getBits(205, 4, 4), self.getBits(205, 0 ,4))
        #byte_206 ~ byte_209
        self.lineEdit_206.setValue(self.getValue(207) * 256 + self.getValue(206))
        self.checkBox_208.setChecked(self.getBits(208, 7, 1))
        self.comboBox_208_1.setCurrentIndex(self.getBits(208, 0, 4))
        self.lineEdit_209.setValue(self.getBits(209, 4, 4), self.getBits(209, 0 ,4))
        #byte_210 ~ byte_213
        self.lineEdit_210.setValue(self.getValue(211) * 256 + self.getValue(210))
        self.checkBox_212.setChecked(self.getBits(212, 7, 1))
        self.checkBox_212_2.setChecked(self.getBits(212, 6, 1))
        self.comboBox_212_1.setCurrentIndex(self.getBits(212, 0, 4))
        self.lineEdit_213.setValue(self.getBits(213, 4, 4), self.getBits(213, 0 ,4))
        #byte_234
        self.comboBox_234.setCurrentIndex(self.getBits(234, 6, 1))
        self.spinBox_234_1.setValue(self.getBits(234, 3, 3))
        #byte_235
        self.comboBox_235.setCurrentIndex(self.getBits(235, 5, 3))
        self.comboBox_235_1.setCurrentIndex(self.getBits(235, 3, 2))
        self.comboBox_235_2.setCurrentIndex(self.getBits(235, 0, 3))
        #byte_512 ~ byte_554
        self.lineEdit_512.setValue(self.getValue(513) * 256 + self.getValue(512))
        self.spinBox_514.setValue(self.getValue(514))
        try:
            self.dateEdit_515.setDate(get_first_day_of_week(2000 + int(format(self.getValue(515), 'x')), int(format(self.getValue(516), 'x'))))
        except:
            self.dateEdit_515.setDate(QDate(2000,1,7))
        self.lineEdit_517.setValue(self.getValue(517) * 256 * 256 * 256 + self.getValue(518) * 256 * 256 + self.getValue(519) * 256 + self.getValue(520))
        t = ""
        for ti in range (0,30):
            t = t + chr(self.getValue(521 + ti))
        self.lineEdit_521.setText(t)
        self.spinBox_551.setValue(self.getValue(551))
        self.lineEdit_552.setValue(self.getValue(553) * 256 + self.getValue(552))
        
    def auto_config(self):  
        #byte_0
        self.updateValue(0, 0x30)
        #byte_1
        self.updateValue(1, 0x10)
        #byte_8 ~ byte_11
        self.updateZero(8, 12)
        #byte_12
        self.updateValue(12, 0x20)
        #byte_13
        self.updateValue(13, 0x02)
        #byte_14
        self.updateValue(14, 0x0)
        #byte_19
        self.updateValue(19, 0x0)
        #byte_20 ~ byte_23
        self.updateValue(20, 0x65)
        self.updateValue(21, 0x01)
        self.updateValue(22, 0xF2)
        self.updateValue(23, 0x03)
        #byte_48 ~ byte_53
        self.updateZero(48, 54)
        #byte_54 ~ byte_69
        self.updateZero(54, 70)
        #byte_70 ~ byte_72
        self.updateValue(70, 0x88)
        self.updateValue(71, 0x13)
        self.updateValue(72, 0x08)
        #byte_73 ~ byte_75
        self.updateValue(73, 0x88)
        self.updateValue(74, 0x13)
        self.updateValue(75, 0x08)
        #byte_76 ~ byte_78
        self.updateValue(76, 0x20)
        self.updateValue(77, 0x4E)
        self.updateValue(78, 0x20)
        #byte_79 ~ byte_81
        self.updateValue(79, 0x10)
        self.updateValue(80, 0x27)
        self.updateValue(81, 0x10)
        #byte_82 ~ byte_84
        self.updateValue(82, 0xA4)
        self.updateValue(83, 0x2C)
        self.updateValue(84, 0x20)
        #byte_85 ~ byte_87
        self.updateValue(85, 0x10)
        self.updateValue(86, 0x27)
        self.updateValue(87, 0x10)
        #byte_88 ~ byte_90
        self.updateValue(88, 0xC4)
        self.updateValue(89, 0x09)
        self.updateValue(90, 0x04)
        #byte_91 ~ byte_93
        self.updateValue(91, 0x4C)
        self.updateValue(92, 0x1D)
        self.updateValue(93, 0x0C)
        #byte_94 ~ byte_96
        #byte_97 ~ byte_99
        #byte_100 ~ byte_102
        self.updateZero(94, 103)
        #byte_193
        self.updateValue(193, 0x0)
        #byte_230
        self.updateValue(230, 0x11)
        #byte_231
        self.updateValue(231, 0x01)
        #byte_232
        self.updateValue(232, 0x0)
        #byte_233
        self.updateValue(233, 0x81)
        #byte_240 ~ byte_257
        self.updateZero(240, 258)
        #byte_554
        self.updateValue(554, 0xFF)
        #byte_555 ~ byte_639(pass)
        #byte_640 ~ byte_1023(pass)
        self.updateZero(555, 1024)
        
    def setConfig(self):
        #byte_2
        self.updateValue(2, 2 * self.comboBox_2.currentIndex() + 0x12)
        #byte_3
        if self.comboBox_3.currentIndex() == 0: self.updateBits(3, 4, 4, 0x0000)
        if self.comboBox_3.currentIndex() == 1: self.updateBits(3, 4, 4, 0x1001)
        if self.comboBox_3.currentIndex() == 2: self.updateBits(3, 4, 4, 0x1010)
        t = self.comboBox_3_1.currentIndex() + 1 if self.comboBox_3_1.currentIndex() < 8 else self.comboBox_3_1.currentIndex() + 2
        self.updateBits(3, 0, 4, t)
        #byte_4
        self.updateBits(4, 5, 3, self.comboBox_4.currentIndex())
        self.updateBits(4, 0, 5, self.comboBox_4_1.currentIndex())
        #byte_5
        self.updateBits(5, 5, 3, self.comboBox_5.currentIndex() // 3)
        self.updateBits(5, 0, 5, self.comboBox_5.currentIndex() % 3)
        #byte_6
        self.updateBits(6, 5, 3, self.comboBox_6.currentIndex())
        #byte_7
        self.updateBits(7, 5, 3, self.comboBox_7.currentIndex())
        self.updateBits(7, 3, 2, 0)
        self.updateBits(7, 0, 3, self.comboBox_7_1.currentIndex())
        #byte_15 ~ 18
        self.updateZero(15, 19)
        #byte_24 ~ byte_28
        #self.updateValue(24, self.spinBox_24.value())
        #self.updateValue(25, self.spinBox_25.value())
        #self.updateValue(26, self.spinBox_26.value())
        #self.updateValue(27, self.spinBox_27.value())
        #self.updateValue(28, self.spinBox_28.value())
        for i in range(0, 40):
            row, column  = divmod(i, 8)
            self.updateBits(24 + row, column, 1, getattr(self, f'checkBox_{i+1}').isChecked())
        #byte_29
        self.updateValue(29, 0)
        #byte_30 ~ byte_47
        self.updateValue(30, self.spinBox_30.value() % 256)
        self.updateValue(31, self.spinBox_30.value() // 256)
        self.updateValue(32, self.spinBox_32.value() % 256)
        self.updateValue(33, self.spinBox_32.value() // 256)
        self.updateValue(34, self.spinBox_34.value() % 256)
        self.updateValue(35, self.spinBox_34.value() // 256)
        self.updateValue(36, self.spinBox_36.value() % 256)
        self.updateValue(37, self.spinBox_36.value() // 256)
        self.updateValue(38, self.spinBox_38.value() % 256)
        self.updateValue(39, self.spinBox_38.value() // 256)
        self.updateValue(40, self.spinBox_40.value() % 256)
        self.updateValue(41, self.spinBox_40.value() // 256)
        self.updateValue(42, self.spinBox_42.value() % 256)
        self.updateValue(43, self.spinBox_42.value() // 256)
        self.updateValue(44, self.spinBox_44.value() % 256)
        self.updateValue(45, self.spinBox_44.value() // 256)
        self.updateValue(46, self.spinBox_46.value() % 256)
        self.updateValue(47, self.spinBox_46.value() // 256)
        #byte_103 ~ byte_127
        self.updateZero(103, 128)
        #byte_128 ~ byte_191
        self.updateZero(128, 192)
        #byte_192
        self.updateBits(192, 4, 4, self.lineEdit_192.value()[0])
        self.updateBits(192, 0, 4, self.lineEdit_192.value()[1])
        #byte_194 ~ byte_197
        self.updateValue(194, self.lineEdit_194.value() % 256)
        self.updateValue(195, self.lineEdit_194.value() // 256)
        self.updateBits(196, 7, 1, self.checkBox_196.isChecked())
        self.updateBits(196, 4, 3, 0)
        self.updateBits(196, 0, 4, self.comboBox_196_1.currentIndex())
        self.updateBits(197, 4, 4, self.lineEdit_197.value()[0])
        self.updateBits(197, 0, 4, self.lineEdit_197.value()[1])
        #byte_198 ~ byte_201
        self.updateValue(198, self.lineEdit_198.value() % 256)
        self.updateValue(199, self.lineEdit_198.value() // 256)
        self.updateBits(200, 7, 1, self.checkBox_200.isChecked())
        self.updateBits(200, 4, 3, 0)
        self.updateBits(200, 0, 4, self.comboBox_200_1.currentIndex())
        self.updateBits(201, 4, 4, self.lineEdit_201.value()[0])
        self.updateBits(201, 0, 4, self.lineEdit_201.value()[1])
        #byte_202 ~ byte_205
        self.updateValue(202, self.lineEdit_202.value() % 256)
        self.updateValue(203, self.lineEdit_202.value() // 256)
        self.updateBits(204, 7, 1, self.checkBox_204.isChecked())
        self.updateBits(204, 4, 3, 0)
        self.updateBits(204, 0, 4, self.comboBox_204_1.currentIndex())
        self.updateBits(205, 4, 4, self.lineEdit_205.value()[0])
        self.updateBits(205, 0, 4, self.lineEdit_205.value()[1])
        #byte_206 ~ byte_209
        self.updateValue(206, self.lineEdit_206.value() % 256)
        self.updateValue(207, self.lineEdit_206.value() // 256)
        self.updateBits(208, 7, 1, self.checkBox_208.isChecked())
        self.updateBits(208, 4, 3, 0)
        self.updateBits(208, 0, 4, self.comboBox_208_1.currentIndex())
        self.updateBits(209, 4, 4, self.lineEdit_209.value()[0])
        self.updateBits(209, 0, 4, self.lineEdit_209.value()[1])
        #byte_210 ~ byte_213
        self.updateValue(210, self.lineEdit_210.value() % 256)
        self.updateValue(211, self.lineEdit_210.value() // 256)
        self.updateBits(212, 7, 1, self.checkBox_212.isChecked())
        self.updateBits(212, 6, 1, self.checkBox_212_2.isChecked())
        self.updateBits(212, 4, 2, 0)
        self.updateBits(212, 0, 4, self.comboBox_212_1.currentIndex())
        self.updateBits(213, 4, 4, self.lineEdit_213.value()[0])
        self.updateBits(213, 0, 4, self.lineEdit_213.value()[1])
        #byte_214 ~ byte_229
        self.updateZero(214, 230)
        #byte_234 
        self.updateBits(234, 7, 1, 0)
        self.updateBits(234, 6, 1, self.comboBox_234.currentIndex())
        self.updateBits(234, 3, 3, self.spinBox_234_1.value() - 1)
        self.updateBits(234, 0, 3, 0)
        #byte_235
        self.updateBits(235, 5, 3, self.comboBox_235.currentIndex())
        self.updateBits(235, 3, 2, self.comboBox_235_1.currentIndex())
        self.updateBits(235, 0, 3, self.comboBox_235_2.currentIndex())
        #byte_236 ~ byte_239
        self.updateZero(236, 240)
        #byte_258 ~ byte_447
        self.updateZero(258, 448)
        #byte_448 ~ byte_509
        self.updateZero(448, 510)
        #else 
        if self.all_ff == True:
            self.auto_config()
        #byte_510 ~ byte_511
        crc_16 = self.calculate_CRC()
        self.updateValue(510, crc_16 & 0xFF)
        self.updateValue(511, crc_16 >> 8)
        #byte_512 ~ byte_554
        self.updateValue(512, self.lineEdit_512.value() % 256)
        self.updateValue(513, self.lineEdit_512.value() // 256)
        self.updateValue(514, self.spinBox_514.value())
        self.updateValue(515, int(f"0x{qdate_to_year_week(self.dateEdit_515.date())[0] - 2000}", 16)) 
        self.updateValue(516, int(f"0x{qdate_to_year_week(self.dateEdit_515.date())[1]}", 16))
        t = self.lineEdit_517.value() % (256 * 256)
        self.updateValue(520, t % 256)
        self.updateValue(519, t // 256)
        t = self.lineEdit_517.value() // (256 * 256)
        self.updateValue(518, t % 256)
        self.updateValue(517, t // 256)
        t = self.lineEdit_521.text()
        for ti in range (0,30):
            if len(t) > 0:
                self.updateValue(521 + ti, ord(t[0]))
                t = t[1:]
            else:
                self.updateValue(521 + ti, 0x20)
        self.updateValue(551, self.spinBox_551.value())
        self.updateValue(552, self.lineEdit_552.value() % 256)
        self.updateValue(553, self.lineEdit_552.value() // 256)
        
    # Prefix with '0x' and convert back to integer with base 16
   
        #byte_555 ~ byte_639(pass)
        #byte_640 ~ byte_1023(pass)
        config = self.wconfig
        self.data_updated.emit(config)
        
    def closeEvent(self, event):
        self.setConfig()  # Call update_data when dialog is about to close
        super().closeEvent(event)
     
    def updateZero(self, num1, num2):
        for i in range(num1,num2):
            self.wconfig[i] = 0
     
    def updateValue(self, num, value):
        self.wconfig[num] = value
        
    def getValue(self, num):
        return self.wconfig[num]    
    
    def updateBits(self, num, lsb, bits, value):
        _mask = (1 << bits) - 1 
        self.wconfig[num] &= ~(_mask << lsb)
        self.wconfig[num] |= ((value &_mask) << lsb)
        
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
    
    myapp = Dialog_Ui_3()
    myapp.show()
    
    sys.exit(app.exec_())