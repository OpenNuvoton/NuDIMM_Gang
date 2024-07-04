from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QThread, QObject, QRegExp, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator

from config_spd import Ui_Dialog
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
class Dialog_Ui(QDialog, Ui_Dialog):

    data_updated = pyqtSignal(object)

    def __init__(self, config = [], parent=None):
        super(Dialog_Ui, self).__init__(parent)
        self.setupUi(self)
        
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
        #byte_0
        self.spinBox_0.setValue(self.getBits(0, 7, 1) * 16 + self.getBits(0, 0, 4))
        t = self.getBits(0, 4, 3)
        self.comboBox_0.setCurrentIndex(4 if (t <= 0 or t >= 5) else t - 1)
        #byte_1
        self.lineEdit_1.setValue(self.getBits(1, 4, 4), self.getBits(1, 0 ,4))
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
        #byte_8
        self.comboBox_8.setCurrentIndex(self.getBits(8, 5, 3))
        self.comboBox_8_1.setCurrentIndex(self.getBits(8, 0, 5))
        #byte_9
        self.comboBox_9.setCurrentIndex(self.getBits(9, 5, 1) * 3 + self.getBits(9, 0, 2))
        #byte_10
        self.comboBox_10.setCurrentIndex(self.getBits(10, 5, 3))
        #byte_11
        self.comboBox_11.setCurrentIndex(self.getBits(11, 5, 2))
        self.comboBox_11_1.setCurrentIndex(self.getBits(11, 0, 2))
        #byte_12
        self.comboBox_12.setCurrentIndex(self.getBits(12, 7, 1))
        self.checkBox_12_1.setChecked(self.getBits(12, 5, 1))
        self.checkBox_12_2.setChecked(self.getBits(12, 4, 1))
        self.checkBox_12_3.setChecked(self.getBits(12, 1, 1))
        #byte_13
        self.checkBox_13.setChecked(self.getBits(13, 4, 1))
        self.comboBox_13_1.setCurrentIndex(self.getBits(13, 0, 2))
        #byte_14
        self.checkBox_14.setChecked(self.getBits(14, 3, 1))
        self.checkBox_14_1.setChecked(self.getBits(14, 0, 1))
        if self.getBits(14, 1, 2) == 0: self.comboBox_14_2.setCurrentIndex(0)
        if self.getBits(14, 1, 2) == 0x10: self.comboBox_14_2.setCurrentIndex(1)
        if self.getBits(14, 1, 2) == 0x11: self.comboBox_14_2.setCurrentIndex(2)
        #byte_19
        self.checkBox_19.setChecked(self.getBits(19, 0, 1))
        #byte_20 ~ byte_23
        self.spinBox_20.setValue(self.getValue(21) * 256 + self.getValue(20))
        self.spinBox_22.setValue(self.getValue(23) * 256 + self.getValue(22))
        #byte_24 ~ byte_28
        self.spinBox_24.setValue(self.getValue(24))
        self.spinBox_25.setValue(self.getValue(25))
        self.spinBox_26.setValue(self.getValue(26))
        self.spinBox_27.setValue(self.getValue(27))
        self.spinBox_28.setValue(self.getValue(28))
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
        self.spinBox_48.setValue(self.getValue(49) * 256 + self.getValue(48))
        self.spinBox_50.setValue(self.getValue(51) * 256 + self.getValue(50))
        self.spinBox_52.setValue(self.getValue(53) * 256 + self.getValue(52))
        #byte_54 ~ byte_55
        self.checkBox_54.setChecked(self.getBits(54, 0, 1))
        self.comboBox_54_1.setCurrentIndex(self.getBits(54, 5, 3) - 2 if self.getBits(54, 5, 3) >= 3 else 0)
        self.comboBox_54_2.setCurrentIndex(self.getBits(54, 1, 4) - 3 if self.getBits(54, 1, 4) >= 4 else 0)
        self.comboBox_55.setCurrentIndex(self.getBits(55, 6, 2))
        self.comboBox_55_1.setCurrentIndex(self.getBits(55, 3, 1))
        self.comboBox_55_2.setCurrentIndex(self.getBits(55, 1, 2))
        self.checkBox_55_3.setChecked(self.getBits(55, 0, 1))
        #byte_56 ~ byte_57
        self.checkBox_56.setChecked(self.getBits(56, 0, 1))
        self.comboBox_56_1.setCurrentIndex(self.getBits(56, 5, 3) - 2 if self.getBits(56, 5, 3) >= 3 else 0)
        self.comboBox_56_2.setCurrentIndex(self.getBits(56, 1, 4) - 3 if self.getBits(56, 1, 4) >= 4 else 0)
        self.comboBox_57.setCurrentIndex(self.getBits(57, 6, 2))
        self.comboBox_57_1.setCurrentIndex(self.getBits(57, 3, 1))
        self.comboBox_57_2.setCurrentIndex(self.getBits(57, 1, 2))
        self.checkBox_57_3.setChecked(self.getBits(57, 0, 1))
        #byte_58 ~ byte_59
        self.checkBox_58.setChecked(self.getBits(58, 0, 1))
        self.comboBox_58_1.setCurrentIndex(self.getBits(58, 5, 3) - 2 if self.getBits(58, 5, 3) >= 3 else 0)
        self.comboBox_58_2.setCurrentIndex(self.getBits(58, 1, 4) - 3 if self.getBits(58, 1, 4) >= 4 else 0)
        self.comboBox_59.setCurrentIndex(self.getBits(59, 6, 2))
        self.comboBox_59_1.setCurrentIndex(self.getBits(59, 3, 1))
        self.comboBox_59_2.setCurrentIndex(self.getBits(59, 1, 2))
        self.checkBox_59_3.setChecked(self.getBits(59, 0, 1))
        #byte_60 ~ byte_61
        self.checkBox_60.setChecked(self.getBits(60, 0, 1))
        self.comboBox_60_1.setCurrentIndex(self.getBits(60, 5, 3) - 2 if self.getBits(60, 5, 3) >= 3 else 0)
        self.comboBox_60_2.setCurrentIndex(self.getBits(60, 1, 4) - 3 if self.getBits(60, 1, 4) >= 4 else 0)
        self.comboBox_61.setCurrentIndex(self.getBits(61, 6, 2))
        self.comboBox_61_1.setCurrentIndex(self.getBits(61, 3, 1))
        self.comboBox_61_2.setCurrentIndex(self.getBits(61, 1, 2))
        self.checkBox_61_3.setChecked(self.getBits(61, 0, 1))
        #byte_62 ~ byte_63
        self.checkBox_62.setChecked(self.getBits(62, 0, 1))
        self.comboBox_62_1.setCurrentIndex(self.getBits(62, 5, 3) - 2 if self.getBits(62, 5, 3) >= 3 else 0)
        self.comboBox_62_2.setCurrentIndex(self.getBits(62, 1, 4) - 3 if self.getBits(62, 1, 4) >= 4 else 0)
        self.comboBox_63.setCurrentIndex(self.getBits(63, 6, 2))
        self.comboBox_63_1.setCurrentIndex(self.getBits(63, 3, 1))
        self.comboBox_63_2.setCurrentIndex(self.getBits(63, 1, 2))
        self.checkBox_63_3.setChecked(self.getBits(63, 0, 1))
        #byte_64 ~ byte_65
        self.checkBox_64.setChecked(self.getBits(64, 0, 1))
        self.comboBox_64_1.setCurrentIndex(self.getBits(64, 5, 3) - 2 if self.getBits(64, 5, 3) >= 3 else 0)
        self.comboBox_64_2.setCurrentIndex(self.getBits(64, 1, 4) - 3 if self.getBits(64, 1, 4) >= 4 else 0)
        self.comboBox_65.setCurrentIndex(self.getBits(65, 6, 2))
        self.comboBox_65_1.setCurrentIndex(self.getBits(65, 3, 1))
        self.comboBox_65_2.setCurrentIndex(self.getBits(65, 1, 2))
        self.checkBox_65_3.setChecked(self.getBits(65, 0, 1))
        #byte_66 ~ byte_67
        self.checkBox_66.setChecked(self.getBits(66, 0, 1))
        self.comboBox_66_1.setCurrentIndex(self.getBits(66, 5, 3) - 2 if self.getBits(66, 5, 3) >= 3 else 0)
        self.comboBox_66_2.setCurrentIndex(self.getBits(66, 1, 4) - 3 if self.getBits(66, 1, 4) >= 4 else 0)
        self.comboBox_67.setCurrentIndex(self.getBits(67, 6, 2))
        self.comboBox_67_1.setCurrentIndex(self.getBits(67, 3, 1))
        self.comboBox_67_2.setCurrentIndex(self.getBits(67, 1, 2))
        self.checkBox_67_3.setChecked(self.getBits(67, 0, 1))
        #byte_68 ~ byte_69
        self.checkBox_68.setChecked(self.getBits(68, 0, 1))
        self.comboBox_68_1.setCurrentIndex(self.getBits(68, 5, 3) - 2 if self.getBits(68, 5, 3) >= 3 else 0)
        self.comboBox_68_2.setCurrentIndex(self.getBits(68, 1, 4) - 3 if self.getBits(68, 1, 4) >= 4 else 0)
        self.comboBox_69.setCurrentIndex(self.getBits(69, 6, 2))
        self.comboBox_69_1.setCurrentIndex(self.getBits(69, 3, 1))
        self.comboBox_69_2.setCurrentIndex(self.getBits(69, 1, 2))
        self.checkBox_69_3.setChecked(self.getBits(69, 0, 1))
        #byte_70 ~ byte_72
        self.spinBox_70.setValue(self.getValue(71) * 256 + self.getValue(70))
        self.spinBox_72.setValue(self.getValue(72))
        #byte_73 ~ byte_75
        self.spinBox_73.setValue(self.getValue(74) * 256 + self.getValue(73))
        self.spinBox_75.setValue(self.getValue(75))
        #byte_76 ~ byte_78
        self.spinBox_76.setValue(self.getValue(77) * 256 + self.getValue(76))
        self.spinBox_78.setValue(self.getValue(78))
        #byte_79 ~ byte_81
        self.spinBox_79.setValue(self.getValue(80) * 256 + self.getValue(79))
        self.spinBox_81.setValue(self.getValue(81))
        #byte_82 ~ byte_84
        self.spinBox_82.setValue(self.getValue(83) * 256 + self.getValue(82))
        self.spinBox_84.setValue(self.getValue(84))
        #byte_85 ~ byte_87
        self.spinBox_85.setValue(self.getValue(86) * 256 + self.getValue(85))
        self.spinBox_87.setValue(self.getValue(87))
        #byte_88 ~ byte_90
        self.spinBox_88.setValue(self.getValue(89) * 256 + self.getValue(88))
        self.spinBox_90.setValue(self.getValue(90))
        #byte_91 ~ byte_93
        self.spinBox_91.setValue(self.getValue(92) * 256 + self.getValue(91))
        self.spinBox_93.setValue(self.getValue(93))
        #byte_94 ~ byte_96
        self.spinBox_94.setValue(self.getValue(95) * 256 + self.getValue(94))
        self.spinBox_96.setValue(self.getValue(96))
        #byte_97 ~ byte_99
        self.spinBox_97.setValue(self.getValue(98) * 256 + self.getValue(97))
        self.spinBox_99.setValue(self.getValue(99))
        #byte_100 ~ byte_102
        self.spinBox_100.setValue(self.getValue(101) * 256 + self.getValue(100))
        self.spinBox_102.setValue(self.getValue(102))
        #byte_192
        self.lineEdit_192.setValue(self.getBits(192, 4, 4), self.getBits(192, 0 ,4))
        #byte_193
        self.checkBox_193.setChecked(self.getBits(193, 0, 3))
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
        #byte_230 ~ byte_231
        self.spinBox_230.setValue(self.getBits(230, 0, 5) + 15)
        self.spinBox_231.setValue(self.getBits(231, 4, 4) + 1)
        self.spinBox_231_1.setValue(self.getBits(231, 0, 4) + 1)
        #byte_232
        self.comboBox_232.setCurrentIndex(self.getBits(232, 5, 3))
        self.comboBox_232_1.setCurrentIndex(self.getBits(232, 0, 5))
        #byte_233
        self.comboBox_233.setCurrentIndex(self.getBits(233, 4, 4))
        self.comboBox_233_1.setCurrentIndex(self.getBits(233, 0, 2))
        self.checkBox_233_2.setChecked(self.getBits(233, 2, 1))
        #byte_234
        self.comboBox_234.setCurrentIndex(self.getBits(234, 6, 1))
        self.spinBox_234_1.setValue(self.getBits(234, 3, 3))
        #byte_235
        self.comboBox_235.setCurrentIndex(self.getBits(235, 5, 3))
        self.comboBox_235_1.setCurrentIndex(self.getBits(235, 3, 2))
        self.comboBox_235_2.setCurrentIndex(self.getBits(235, 0, 3))
        #byte_240 ~ byte_257
        self.spinBox_240.setValue(self.getValue(240))
        self.spinBox_241.setValue(self.getValue(241))
        self.spinBox_242.setValue(self.getValue(242))
        self.spinBox_243.setValue(self.getValue(243))
        self.spinBox_244.setValue(self.getValue(244))
        self.spinBox_245.setValue(self.getValue(245))
        self.spinBox_246.setValue(self.getValue(246))
        self.spinBox_247.setValue(self.getValue(247))
        self.spinBox_248.setValue(self.getValue(248))
        self.spinBox_249.setValue(self.getValue(249))
        self.spinBox_250.setValue(self.getValue(250))
        self.spinBox_251.setValue(self.getValue(251))
        self.spinBox_252.setValue(self.getValue(252))
        self.spinBox_253.setValue(self.getValue(253))
        self.spinBox_254.setValue(self.getValue(254))
        self.spinBox_255.setValue(self.getValue(255))
        self.spinBox_256.setValue(self.getValue(256))
        self.spinBox_257.setValue(self.getValue(257))
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
        self.spinBox_554.setValue(self.getValue(554))
            
        
    def setConfig(self):
        #byte_0
        t =  self.spinBox_0.value()
        self.updateBits(0, 7, 1, t // 16)
        self.updateBits(0, 0, 4, t % 16)
        t = self.comboBox_0.currentIndex() + 1 if self.comboBox_0.currentIndex() != 4 else 0
        self.updateBits(0, 4, 3, t)
        #byte_1
        self.updateBits(1, 4, 4, self.lineEdit_1.value()[0])
        self.updateBits(1, 0, 4, self.lineEdit_1.value()[1])
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
        #byte_8
        self.updateBits(8, 5, 3, self.comboBox_8.currentIndex())
        self.updateBits(8, 0, 5, self.comboBox_8_1.currentIndex())
        #byte_9
        self.updateBits(9, 5, 3, self.comboBox_9.currentIndex() // 3)
        self.updateBits(9, 0, 5, self.comboBox_9.currentIndex() % 3)
        #byte_10
        self.updateBits(10, 5, 3, self.comboBox_10.currentIndex())
        #byte_11
        self.updateBits(11, 5, 3, self.comboBox_11.currentIndex())
        self.updateBits(11, 3, 2, 0)
        self.updateBits(11, 0, 3, self.comboBox_11_1.currentIndex())
        #byte_12
        self.updateBits(12, 7, 1, self.comboBox_12.currentIndex())
        self.updateBits(12, 6, 1, 0)
        self.updateBits(12, 5, 1, self.checkBox_12_1.isChecked())
        self.updateBits(12, 4, 1, self.checkBox_12_2.isChecked())
        self.updateBits(12, 2, 2, 0)
        self.updateBits(12, 1, 1, self.checkBox_12_3.isChecked())
        self.updateBits(12, 0, 1, 0)
        #byte_13
        self.updateBits(13, 5, 3, 0)
        self.updateBits(13, 4, 1, self.checkBox_13.isChecked())
        self.updateBits(13, 2, 2, 0)
        self.updateBits(13, 0, 2, self.comboBox_13_1.currentIndex())
        #byte_14
        self.updateBits(14, 4, 4, 0)
        self.updateBits(14, 3, 1, self.checkBox_14.isChecked())
        t = self.comboBox_14_2.currentIndex() + 1 if (self.comboBox_14_2.currentIndex() != 0) else 0
        self.updateBits(14, 1, 2, t)
        self.updateBits(14, 0, 1, self.checkBox_14_1.isChecked())
        #byte_15 ~ 18
        self.updateZero(15, 19)
        #byte_19
        self.updateBits(19, 1, 7, 0)
        self.updateBits(19, 0, 1, self.checkBox_19.isChecked())
        #byte_20 ~ byte_23
        self.updateValue(20, self.spinBox_20.value() % 256)
        self.updateValue(21, self.spinBox_20.value() // 256)
        self.updateValue(22, self.spinBox_22.value() % 256)
        self.updateValue(23, self.spinBox_22.value() // 256)
        #byte_24 ~ byte_28
        self.updateValue(24, self.spinBox_24.value())
        self.updateValue(25, self.spinBox_25.value())
        self.updateValue(26, self.spinBox_26.value())
        self.updateValue(27, self.spinBox_27.value())
        self.updateValue(28, self.spinBox_28.value())
        #byte_29
        self.updateValue(29, 0)
        #byte_30 ~ byte_53
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
        self.updateValue(48, self.spinBox_48.value() % 256)
        self.updateValue(49, self.spinBox_48.value() // 256)
        self.updateValue(50, self.spinBox_50.value() % 256)
        self.updateValue(51, self.spinBox_50.value() // 256)
        self.updateValue(52, self.spinBox_52.value() % 256)
        self.updateValue(53, self.spinBox_52.value() // 256)
        #byte_54 ~ byte_55
        self.updateBits(54, 0, 1, self.checkBox_54.isChecked())
        self.updateBits(54, 5, 3, self.comboBox_54_1.currentIndex() + 2 if self.comboBox_54_1.currentIndex()!= 0 else 0)
        self.updateBits(54, 1, 4, self.comboBox_54_2.currentIndex() + 3 if self.comboBox_54_2.currentIndex()!= 0 else 0)
        self.updateBits(55, 6, 2, self.comboBox_55.currentIndex())
        self.updateBits(55, 4, 2, 0)
        self.updateBits(55, 3, 1, self.comboBox_55_1.currentIndex())
        self.updateBits(55, 1, 2, self.comboBox_55_2.currentIndex())
        self.updateBits(55, 0, 1, self.checkBox_55_3.isChecked())
        #byte_56 ~ byte_57
        self.updateBits(56, 0, 1, self.checkBox_56.isChecked())
        self.updateBits(56, 5, 3, self.comboBox_56_1.currentIndex() + 2 if self.comboBox_56_1.currentIndex()!= 0 else 0)
        self.updateBits(56, 1, 4, self.comboBox_56_2.currentIndex() + 3 if self.comboBox_56_2.currentIndex()!= 0 else 0)
        self.updateBits(57, 6, 2, self.comboBox_57.currentIndex())
        self.updateBits(57, 4, 2, 0)
        self.updateBits(57, 3, 1, self.comboBox_57_1.currentIndex())
        self.updateBits(57, 1, 2, self.comboBox_57_2.currentIndex())
        self.updateBits(57, 0, 1, self.checkBox_57_3.isChecked())
        #byte_58 ~ byte_59
        self.updateBits(58, 0, 1, self.checkBox_58.isChecked())
        self.updateBits(58, 5, 3, self.comboBox_58_1.currentIndex() + 2 if self.comboBox_58_1.currentIndex()!= 0 else 0)
        self.updateBits(58, 1, 4, self.comboBox_58_2.currentIndex() + 3 if self.comboBox_58_2.currentIndex()!= 0 else 0)
        self.updateBits(59, 6, 2, self.comboBox_59.currentIndex())
        self.updateBits(59, 4, 2, 0)
        self.updateBits(59, 3, 1, self.comboBox_59_1.currentIndex())
        self.updateBits(59, 1, 2, self.comboBox_59_2.currentIndex())
        self.updateBits(59, 0, 1, self.checkBox_59_3.isChecked())
        #byte_60 ~ byte_61
        self.updateBits(60, 0, 1, self.checkBox_60.isChecked())
        self.updateBits(60, 5, 3, self.comboBox_60_1.currentIndex() + 2 if self.comboBox_60_1.currentIndex()!= 0 else 0)
        self.updateBits(60, 1, 4, self.comboBox_60_2.currentIndex() + 3 if self.comboBox_60_2.currentIndex()!= 0 else 0)
        self.updateBits(61, 6, 2, self.comboBox_61.currentIndex())
        self.updateBits(61, 4, 2, 0)
        self.updateBits(61, 3, 1, self.comboBox_61_1.currentIndex())
        self.updateBits(61, 1, 2, self.comboBox_61_2.currentIndex())
        self.updateBits(61, 0, 1, self.checkBox_61_3.isChecked())
        #byte_62 ~ byte_63
        self.updateBits(62, 0, 1, self.checkBox_62.isChecked())
        self.updateBits(62, 5, 3, self.comboBox_62_1.currentIndex() + 2 if self.comboBox_62_1.currentIndex()!= 0 else 0)
        self.updateBits(62, 1, 4, self.comboBox_62_2.currentIndex() + 3 if self.comboBox_62_2.currentIndex()!= 0 else 0)
        self.updateBits(63, 6, 2, self.comboBox_63.currentIndex())
        self.updateBits(63, 4, 2, 0)
        self.updateBits(63, 3, 1, self.comboBox_63_1.currentIndex())
        self.updateBits(63, 1, 2, self.comboBox_63_2.currentIndex())
        self.updateBits(63, 0, 1, self.checkBox_63_3.isChecked())
        #byte_64 ~ byte_65
        self.updateBits(64, 0, 1, self.checkBox_64.isChecked())
        self.updateBits(64, 5, 3, self.comboBox_64_1.currentIndex() + 2 if self.comboBox_64_1.currentIndex()!= 0 else 0)
        self.updateBits(64, 1, 4, self.comboBox_64_2.currentIndex() + 3 if self.comboBox_64_2.currentIndex()!= 0 else 0)
        self.updateBits(65, 6, 2, self.comboBox_65.currentIndex())
        self.updateBits(65, 4, 2, 0)
        self.updateBits(65, 3, 1, self.comboBox_65_1.currentIndex())
        self.updateBits(65, 1, 2, self.comboBox_65_2.currentIndex())
        self.updateBits(65, 0, 1, self.checkBox_65_3.isChecked())
        #byte_66 ~ byte_67
        self.updateBits(66, 0, 1, self.checkBox_66.isChecked())
        self.updateBits(66, 5, 3, self.comboBox_66_1.currentIndex() + 2 if self.comboBox_66_1.currentIndex()!= 0 else 0)
        self.updateBits(66, 1, 4, self.comboBox_66_2.currentIndex() + 3 if self.comboBox_66_2.currentIndex()!= 0 else 0)
        self.updateBits(67, 6, 2, self.comboBox_67.currentIndex())
        self.updateBits(67, 4, 2, 0)
        self.updateBits(67, 3, 1, self.comboBox_67_1.currentIndex())
        self.updateBits(67, 1, 2, self.comboBox_67_2.currentIndex())
        self.updateBits(67, 0, 1, self.checkBox_67_3.isChecked())
        #byte_68 ~ byte_69
        self.updateBits(68, 0, 1, self.checkBox_68.isChecked())
        self.updateBits(68, 5, 3, self.comboBox_68_1.currentIndex() + 2 if self.comboBox_68_1.currentIndex()!= 0 else 0)
        self.updateBits(68, 1, 4, self.comboBox_68_2.currentIndex() + 3 if self.comboBox_68_2.currentIndex()!= 0 else 0)
        self.updateBits(69, 6, 2, self.comboBox_69.currentIndex())
        self.updateBits(69, 4, 2, 0)
        self.updateBits(69, 3, 1, self.comboBox_69_1.currentIndex())
        self.updateBits(69, 1, 2, self.comboBox_69_2.currentIndex())
        self.updateBits(69, 0, 1, self.checkBox_69_3.isChecked())
        #byte_70 ~ byte_72
        self.updateValue(70, self.spinBox_70.value() % 256)
        self.updateValue(71, self.spinBox_70.value() // 256)
        self.updateValue(72, self.spinBox_72.value())
        #byte_73 ~ byte_75
        self.updateValue(73, self.spinBox_73.value() % 256)
        self.updateValue(74, self.spinBox_73.value() // 256)
        self.updateValue(75, self.spinBox_75.value())
        #byte_76 ~ byte_78
        self.updateValue(76, self.spinBox_76.value() % 256)
        self.updateValue(77, self.spinBox_76.value() // 256)
        self.updateValue(78, self.spinBox_78.value())
        #byte_79 ~ byte_81
        self.updateValue(79, self.spinBox_79.value() % 256)
        self.updateValue(80, self.spinBox_79.value() // 256)
        self.updateValue(81, self.spinBox_81.value())
        #byte_82 ~ byte_84
        self.updateValue(82, self.spinBox_82.value() % 256)
        self.updateValue(83, self.spinBox_82.value() // 256)
        self.updateValue(84, self.spinBox_84.value())
        #byte_85 ~ byte_87
        self.updateValue(85, self.spinBox_85.value() % 256)
        self.updateValue(86, self.spinBox_85.value() // 256)
        self.updateValue(87, self.spinBox_87.value())
        #byte_88 ~ byte_90
        self.updateValue(88, self.spinBox_88.value() % 256)
        self.updateValue(89, self.spinBox_88.value() // 256)
        self.updateValue(90, self.spinBox_90.value())
        #byte_91 ~ byte_93
        self.updateValue(91, self.spinBox_91.value() % 256)
        self.updateValue(92, self.spinBox_91.value() // 256)
        self.updateValue(93, self.spinBox_93.value())
        #byte_94 ~ byte_96
        self.updateValue(94, self.spinBox_94.value() % 256)
        self.updateValue(95, self.spinBox_94.value() // 256)
        self.updateValue(96, self.spinBox_96.value())
        #byte_97 ~ byte_99
        self.updateValue(97, self.spinBox_97.value() % 256)
        self.updateValue(98, self.spinBox_97.value() // 256)
        self.updateValue(99, self.spinBox_99.value())
        #byte_100 ~ byte_102
        self.updateValue(100, self.spinBox_100.value() % 256)
        self.updateValue(101, self.spinBox_100.value() // 256)
        self.updateValue(102, self.spinBox_102.value())
        #byte_103 ~ byte_127
        self.updateZero(103, 128)
        #byte_128 ~ byte_191
        self.updateZero(128, 192)
        #byte_192 ~ byte_213
        self.updateBits(192, 4, 4, self.lineEdit_192.value()[0])
        self.updateBits(192, 0, 4, self.lineEdit_192.value()[1])
        #byte_193
        self.updateValue(193, self.checkBox_193.isChecked())
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
        #byte_230 ~ byte_232
        self.updateValue(230, self.spinBox_230.value() - 15)
        self.updateBits(231, 4, 4, self.spinBox_231.value() - 1)
        self.updateBits(231, 0, 4, self.spinBox_231_1.value() - 1)
        self.updateBits(232, 5, 3, self.comboBox_232.currentIndex())
        self.updateBits(232, 0, 5, self.comboBox_232_1.currentIndex())
        #byte_233
        self.updateBits(233, 4, 4, self.comboBox_233.currentIndex())
        self.updateBits(233, 3, 1, 0)
        self.updateBits(233, 2, 1, self.checkBox_233_2.isChecked())
        self.updateBits(233, 0, 2, self.comboBox_233_1.currentIndex())
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
        #byte_240 ~ byte_257
        self.updateValue(240, self.spinBox_240.value())
        self.updateValue(241, self.spinBox_241.value())
        self.updateValue(242, self.spinBox_242.value())
        self.updateValue(243, self.spinBox_243.value())
        self.updateValue(244, self.spinBox_244.value())
        self.updateValue(245, self.spinBox_245.value())
        self.updateValue(246, self.spinBox_246.value())
        self.updateValue(247, self.spinBox_247.value())
        self.updateValue(248, self.spinBox_248.value())
        self.updateValue(249, self.spinBox_249.value())
        self.updateValue(250, self.spinBox_250.value())
        self.updateValue(251, self.spinBox_251.value())
        self.updateValue(252, self.spinBox_252.value())
        self.updateValue(253, self.spinBox_253.value())
        self.updateValue(254, self.spinBox_254.value())
        self.updateValue(255, self.spinBox_255.value())
        self.updateValue(256, self.spinBox_256.value())
        self.updateValue(257, self.spinBox_257.value())
        #byte_258 ~ byte_447
        self.updateZero(258, 448)
        #byte_448 ~ byte_509
        self.updateZero(448, 510)
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
        self.updateValue(554, self.spinBox_554.value())
        
    # Prefix with '0x' and convert back to integer with base 16
   
        #byte_555 ~ byte_639(pass)
        #byte_640 ~ byte_1023(pass)
        if self.all_ff == True:
            self.updateZero(555, 1024)
            
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

    myapp = Dialog_Ui()
    myapp.show()
    
    sys.exit(app.exec_())