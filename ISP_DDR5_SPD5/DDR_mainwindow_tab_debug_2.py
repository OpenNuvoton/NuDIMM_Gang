# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DDR5_tab_debug.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1026, 1000)
        MainWindow.setMaximumSize(QSize(1200, 1200))
        MainWindow.setBaseSize(QSize(800, 800))
        self.actionLoad_Setting = QAction(MainWindow)
        self.actionLoad_Setting.setObjectName(u"actionLoad_Setting")
        self.actionLoad_Setting.setIconVisibleInMenu(True)
        self.actionSave_Setting = QAction(MainWindow)
        self.actionSave_Setting.setObjectName(u"actionSave_Setting")
        self.actionSave_Setting.setIconVisibleInMenu(True)
        self.actionOffline_Setting = QAction(MainWindow)
        self.actionOffline_Setting.setObjectName(u"actionOffline_Setting")
        self.actionExport_SPD_Information = QAction(MainWindow)
        self.actionExport_SPD_Information.setObjectName(u"actionExport_SPD_Information")
        self.actionImport_SPD_Information = QAction(MainWindow)
        self.actionImport_SPD_Information.setObjectName(u"actionImport_SPD_Information")
        self.actionShow_SPD_Information = QAction(MainWindow)
        self.actionShow_SPD_Information.setObjectName(u"actionShow_SPD_Information")
        self.actionSPD_Information_Setting = QAction(MainWindow)
        self.actionSPD_Information_Setting.setObjectName(u"actionSPD_Information_Setting")
        self.actionImport_SPD_file = QAction(MainWindow)
        self.actionImport_SPD_file.setObjectName(u"actionImport_SPD_file")
        self.actionExport_SPD_file = QAction(MainWindow)
        self.actionExport_SPD_file.setObjectName(u"actionExport_SPD_file")
        self.actionSimple = QAction(MainWindow)
        self.actionSimple.setObjectName(u"actionSimple")
        self.actionUser_Manual = QAction(MainWindow)
        self.actionUser_Manual.setObjectName(u"actionUser_Manual")
        self.actionVersion = QAction(MainWindow)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionExtend_Modes = QAction(MainWindow)
        self.actionExtend_Modes.setObjectName(u"actionExtend_Modes")
        self.actionExtend_Modes.setCheckable(True)
        self.actionExtend_Modes.setChecked(False)
        self.actionExtend_Modes.setIconVisibleInMenu(True)
        self.actionExtend_Mode = QAction(MainWindow)
        self.actionExtend_Mode.setObjectName(u"actionExtend_Mode")
        self.actionExtend_Mode.setCheckable(True)
        self.actionSerial_Checker = QAction(MainWindow)
        self.actionSerial_Checker.setObjectName(u"actionSerial_Checker")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_nuvoton = QLabel(self.centralwidget)
        self.label_nuvoton.setObjectName(u"label_nuvoton")
        self.label_nuvoton.setMaximumSize(QSize(1200, 16777215))

        self.verticalLayout_3.addWidget(self.label_nuvoton)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setBaseSize(QSize(1000, 1000))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 999, 923))
        self.scrollAreaWidgetContents.setBaseSize(QSize(1000, 1000))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab = QTabWidget(self.scrollAreaWidgetContents)
        self.tab.setObjectName(u"tab")
        self.tab.setMaximumSize(QSize(16777215, 800))
        self.tab_connect = QWidget()
        self.tab_connect.setObjectName(u"tab_connect")
        self.verticalLayout = QVBoxLayout(self.tab_connect)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.ConnectGroupBox = QGroupBox(self.tab_connect)
        self.ConnectGroupBox.setObjectName(u"ConnectGroupBox")
        self.ConnectGroupBox.setMinimumSize(QSize(0, 75))
        font = QFont()
        font.setBold(True)
        self.ConnectGroupBox.setFont(font)
        self.ConnectGroupBox.setStyleSheet(u"QGroupBox{ font-weight: bold; }")
        self.ConnectLayout = QHBoxLayout(self.ConnectGroupBox)
        self.ConnectLayout.setSpacing(12)
        self.ConnectLayout.setObjectName(u"ConnectLayout")
        self.ConnectLayout.setContentsMargins(24, 6, 24, 6)
        self.btn_connect = QPushButton(self.ConnectGroupBox)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setMinimumSize(QSize(160, 0))
        self.btn_connect.setMaximumSize(QSize(160, 16777215))
        self.btn_connect.setAutoFillBackground(False)
        self.btn_connect.setCheckable(False)
        self.btn_connect.setAutoDefault(False)
        self.btn_connect.setFlat(False)

        self.ConnectLayout.addWidget(self.btn_connect)

        self.label_connect = QLabel(self.ConnectGroupBox)
        self.label_connect.setObjectName(u"label_connect")
        self.label_connect.setMargin(0)
        self.label_connect.setIndent(4)

        self.ConnectLayout.addWidget(self.label_connect)

        self.ConnectLayout.setStretch(1, 3)

        self.verticalLayout.addWidget(self.ConnectGroupBox)

        self.horizontalGroupBox = QGroupBox(self.tab_connect)
        self.horizontalGroupBox.setObjectName(u"horizontalGroupBox")
        self.horizontalGroupBox.setMinimumSize(QSize(0, 75))
        self.horizontalGroupBox.setStyleSheet(u"QGroupBox{ font-weight: bold; }")
        self.Total_Connect = QHBoxLayout(self.horizontalGroupBox)
        self.Total_Connect.setSpacing(12)
        self.Total_Connect.setObjectName(u"Total_Connect")
        self.Total_Connect.setContentsMargins(24, 6, 24, 6)
        self.btn_slot = QPushButton(self.horizontalGroupBox)
        self.btn_slot.setObjectName(u"btn_slot")
        self.btn_slot.setMinimumSize(QSize(160, 0))
        self.btn_slot.setMaximumSize(QSize(160, 16777215))

        self.Total_Connect.addWidget(self.btn_slot)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Total_Connect.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.horizontalGroupBox)

        self.InfoGroupBox = QGroupBox(self.tab_connect)
        self.InfoGroupBox.setObjectName(u"InfoGroupBox")
        self.InfoGroupBox.setMinimumSize(QSize(0, 400))
        self.InfoGroupBox.setStyleSheet(u"QGroupBox{ font-weight: bold; }")
        self.horizontalLayout_2 = QHBoxLayout(self.InfoGroupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SlotGroupBox_0 = QGroupBox(self.InfoGroupBox)
        self.SlotGroupBox_0.setObjectName(u"SlotGroupBox_0")
        self.SlotGroupBox_0.setMinimumSize(QSize(0, 132))
        self.Slot_0_Layout = QVBoxLayout(self.SlotGroupBox_0)
        self.Slot_0_Layout.setObjectName(u"Slot_0_Layout")
        self.Slot_0_Layout.setContentsMargins(6, 0, 6, 0)
        self.Slot_0_2 = QFrame(self.SlotGroupBox_0)
        self.Slot_0_2.setObjectName(u"Slot_0_2")
        self.Slot_0_2.setStyleSheet(u".QFrame { border: 2px solid gray; }")
        self.verticalLayout_5 = QVBoxLayout(self.Slot_0_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_5 = QLabel(self.Slot_0_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_5)

        self.label_slot_0 = QLabel(self.Slot_0_2)
        self.label_slot_0.setObjectName(u"label_slot_0")
        self.label_slot_0.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0)

        self.label_slot_0_rom = QLabel(self.Slot_0_2)
        self.label_slot_0_rom.setObjectName(u"label_slot_0_rom")
        self.label_slot_0_rom.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_rom)

        self.label_slot_0_fw = QLabel(self.Slot_0_2)
        self.label_slot_0_fw.setObjectName(u"label_slot_0_fw")
        self.label_slot_0_fw.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_fw)

        self.label_slot_0_info_1 = QLabel(self.Slot_0_2)
        self.label_slot_0_info_1.setObjectName(u"label_slot_0_info_1")
        self.label_slot_0_info_1.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_info_1)

        self.label_slot_0_info_2 = QLabel(self.Slot_0_2)
        self.label_slot_0_info_2.setObjectName(u"label_slot_0_info_2")
        self.label_slot_0_info_2.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_info_2)

        self.label_slot_0_info_3 = QLabel(self.Slot_0_2)
        self.label_slot_0_info_3.setObjectName(u"label_slot_0_info_3")
        self.label_slot_0_info_3.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_info_3)

        self.label_slot_0_info_4 = QLabel(self.Slot_0_2)
        self.label_slot_0_info_4.setObjectName(u"label_slot_0_info_4")
        self.label_slot_0_info_4.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_info_4)

        self.label_slot_0_info_5 = QLabel(self.Slot_0_2)
        self.label_slot_0_info_5.setObjectName(u"label_slot_0_info_5")
        self.label_slot_0_info_5.setIndent(4)

        self.verticalLayout_5.addWidget(self.label_slot_0_info_5)


        self.Slot_0_Layout.addWidget(self.Slot_0_2)


        self.horizontalLayout_2.addWidget(self.SlotGroupBox_0)

        self.SlotGroupBox_1 = QGroupBox(self.InfoGroupBox)
        self.SlotGroupBox_1.setObjectName(u"SlotGroupBox_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SlotGroupBox_1.sizePolicy().hasHeightForWidth())
        self.SlotGroupBox_1.setSizePolicy(sizePolicy)
        self.SlotGroupBox_1.setMinimumSize(QSize(0, 132))
        self.Slot_1_Layout = QVBoxLayout(self.SlotGroupBox_1)
        self.Slot_1_Layout.setSpacing(4)
        self.Slot_1_Layout.setObjectName(u"Slot_1_Layout")
        self.Slot_1_Layout.setContentsMargins(6, 0, 6, 0)
        self.Slot_1_2 = QFrame(self.SlotGroupBox_1)
        self.Slot_1_2.setObjectName(u"Slot_1_2")
        self.Slot_1_2.setMinimumSize(QSize(0, 60))
        self.Slot_1_2.setStyleSheet(u".QFrame { border: 2px solid gray; }")
        self.Slot_1_2.setFrameShape(QFrame.NoFrame)
        self.Slot_1_2.setFrameShadow(QFrame.Plain)
        self.verticalLayout_14 = QVBoxLayout(self.Slot_1_2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_16 = QLabel(self.Slot_1_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)
        self.label_16.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_16)

        self.label_slot_1 = QLabel(self.Slot_1_2)
        self.label_slot_1.setObjectName(u"label_slot_1")
        self.label_slot_1.setMinimumSize(QSize(160, 0))
        self.label_slot_1.setMargin(0)
        self.label_slot_1.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1)

        self.label_slot_1_rom = QLabel(self.Slot_1_2)
        self.label_slot_1_rom.setObjectName(u"label_slot_1_rom")
        self.label_slot_1_rom.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_rom)

        self.label_slot_1_fw = QLabel(self.Slot_1_2)
        self.label_slot_1_fw.setObjectName(u"label_slot_1_fw")
        self.label_slot_1_fw.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_fw)

        self.label_slot_1_info_1 = QLabel(self.Slot_1_2)
        self.label_slot_1_info_1.setObjectName(u"label_slot_1_info_1")
        self.label_slot_1_info_1.setMargin(0)
        self.label_slot_1_info_1.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_info_1)

        self.label_slot_1_info_2 = QLabel(self.Slot_1_2)
        self.label_slot_1_info_2.setObjectName(u"label_slot_1_info_2")
        self.label_slot_1_info_2.setMargin(0)
        self.label_slot_1_info_2.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_info_2)

        self.label_slot_1_info_3 = QLabel(self.Slot_1_2)
        self.label_slot_1_info_3.setObjectName(u"label_slot_1_info_3")
        self.label_slot_1_info_3.setMargin(0)
        self.label_slot_1_info_3.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_info_3)

        self.label_slot_1_info_4 = QLabel(self.Slot_1_2)
        self.label_slot_1_info_4.setObjectName(u"label_slot_1_info_4")
        self.label_slot_1_info_4.setMargin(0)
        self.label_slot_1_info_4.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_info_4)

        self.label_slot_1_info_5 = QLabel(self.Slot_1_2)
        self.label_slot_1_info_5.setObjectName(u"label_slot_1_info_5")
        self.label_slot_1_info_5.setMargin(0)
        self.label_slot_1_info_5.setIndent(4)

        self.verticalLayout_14.addWidget(self.label_slot_1_info_5)


        self.Slot_1_Layout.addWidget(self.Slot_1_2)


        self.horizontalLayout_2.addWidget(self.SlotGroupBox_1)

        self.SlotGroupBox_2 = QGroupBox(self.InfoGroupBox)
        self.SlotGroupBox_2.setObjectName(u"SlotGroupBox_2")
        self.SlotGroupBox_2.setMinimumSize(QSize(0, 132))
        self.Slot_2_Layout = QVBoxLayout(self.SlotGroupBox_2)
        self.Slot_2_Layout.setSpacing(4)
        self.Slot_2_Layout.setObjectName(u"Slot_2_Layout")
        self.Slot_2_Layout.setContentsMargins(6, 0, 6, 0)
        self.Slot_2_2 = QFrame(self.SlotGroupBox_2)
        self.Slot_2_2.setObjectName(u"Slot_2_2")
        self.Slot_2_2.setMinimumSize(QSize(0, 60))
        self.Slot_2_2.setStyleSheet(u".QFrame { border: 2px solid gray; }")
        self.Slot_2_2.setFrameShape(QFrame.Box)
        self.Slot_2_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_13 = QVBoxLayout(self.Slot_2_2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_18 = QLabel(self.Slot_2_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)
        self.label_18.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_18)

        self.label_slot_2 = QLabel(self.Slot_2_2)
        self.label_slot_2.setObjectName(u"label_slot_2")
        self.label_slot_2.setMinimumSize(QSize(160, 0))
        self.label_slot_2.setMargin(0)
        self.label_slot_2.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2)

        self.label_slot_2_rom = QLabel(self.Slot_2_2)
        self.label_slot_2_rom.setObjectName(u"label_slot_2_rom")
        self.label_slot_2_rom.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_rom)

        self.label_slot_2_fw = QLabel(self.Slot_2_2)
        self.label_slot_2_fw.setObjectName(u"label_slot_2_fw")
        self.label_slot_2_fw.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_fw)

        self.label_slot_2_info_1 = QLabel(self.Slot_2_2)
        self.label_slot_2_info_1.setObjectName(u"label_slot_2_info_1")
        self.label_slot_2_info_1.setMargin(0)
        self.label_slot_2_info_1.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_info_1)

        self.label_slot_2_info_2 = QLabel(self.Slot_2_2)
        self.label_slot_2_info_2.setObjectName(u"label_slot_2_info_2")
        self.label_slot_2_info_2.setMargin(0)
        self.label_slot_2_info_2.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_info_2)

        self.label_slot_2_info_3 = QLabel(self.Slot_2_2)
        self.label_slot_2_info_3.setObjectName(u"label_slot_2_info_3")
        self.label_slot_2_info_3.setMargin(0)
        self.label_slot_2_info_3.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_info_3)

        self.label_slot_2_info_4 = QLabel(self.Slot_2_2)
        self.label_slot_2_info_4.setObjectName(u"label_slot_2_info_4")
        self.label_slot_2_info_4.setMargin(0)
        self.label_slot_2_info_4.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_info_4)

        self.label_slot_2_info_5 = QLabel(self.Slot_2_2)
        self.label_slot_2_info_5.setObjectName(u"label_slot_2_info_5")
        self.label_slot_2_info_5.setLineWidth(2)
        self.label_slot_2_info_5.setMidLineWidth(1)
        self.label_slot_2_info_5.setMargin(0)
        self.label_slot_2_info_5.setIndent(4)

        self.verticalLayout_13.addWidget(self.label_slot_2_info_5)


        self.Slot_2_Layout.addWidget(self.Slot_2_2)


        self.horizontalLayout_2.addWidget(self.SlotGroupBox_2)

        self.SlotGroupBox_3 = QGroupBox(self.InfoGroupBox)
        self.SlotGroupBox_3.setObjectName(u"SlotGroupBox_3")
        self.SlotGroupBox_3.setMinimumSize(QSize(0, 132))
        self.SlotGroupBox_3.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.Slot_3_Layout = QVBoxLayout(self.SlotGroupBox_3)
        self.Slot_3_Layout.setSpacing(4)
        self.Slot_3_Layout.setObjectName(u"Slot_3_Layout")
        self.Slot_3_Layout.setContentsMargins(6, 0, 6, 0)
        self.Slot_3_2 = QFrame(self.SlotGroupBox_3)
        self.Slot_3_2.setObjectName(u"Slot_3_2")
        self.Slot_3_2.setMinimumSize(QSize(0, 60))
        self.Slot_3_2.setStyleSheet(u".QFrame { border: 2px solid gray; }")
        self.Slot_3_2.setFrameShape(QFrame.NoFrame)
        self.Slot_3_2.setFrameShadow(QFrame.Plain)
        self.verticalLayout_10 = QVBoxLayout(self.Slot_3_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_19 = QLabel(self.Slot_3_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)
        self.label_19.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_19)

        self.label_slot_3 = QLabel(self.Slot_3_2)
        self.label_slot_3.setObjectName(u"label_slot_3")
        self.label_slot_3.setMinimumSize(QSize(160, 0))
        self.label_slot_3.setMargin(0)
        self.label_slot_3.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3)

        self.label_slot_3_rom = QLabel(self.Slot_3_2)
        self.label_slot_3_rom.setObjectName(u"label_slot_3_rom")
        self.label_slot_3_rom.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_rom)

        self.label_slot_3_fw = QLabel(self.Slot_3_2)
        self.label_slot_3_fw.setObjectName(u"label_slot_3_fw")
        self.label_slot_3_fw.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_fw)

        self.label_slot_3_info_1 = QLabel(self.Slot_3_2)
        self.label_slot_3_info_1.setObjectName(u"label_slot_3_info_1")
        self.label_slot_3_info_1.setMargin(0)
        self.label_slot_3_info_1.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_info_1)

        self.label_slot_3_info_2 = QLabel(self.Slot_3_2)
        self.label_slot_3_info_2.setObjectName(u"label_slot_3_info_2")
        self.label_slot_3_info_2.setMargin(0)
        self.label_slot_3_info_2.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_info_2)

        self.label_slot_3_info_3 = QLabel(self.Slot_3_2)
        self.label_slot_3_info_3.setObjectName(u"label_slot_3_info_3")
        self.label_slot_3_info_3.setMargin(0)
        self.label_slot_3_info_3.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_info_3)

        self.label_slot_3_info_4 = QLabel(self.Slot_3_2)
        self.label_slot_3_info_4.setObjectName(u"label_slot_3_info_4")
        self.label_slot_3_info_4.setMargin(0)
        self.label_slot_3_info_4.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_info_4)

        self.label_slot_3_info_5 = QLabel(self.Slot_3_2)
        self.label_slot_3_info_5.setObjectName(u"label_slot_3_info_5")
        self.label_slot_3_info_5.setMargin(0)
        self.label_slot_3_info_5.setIndent(4)

        self.verticalLayout_10.addWidget(self.label_slot_3_info_5)


        self.Slot_3_Layout.addWidget(self.Slot_3_2)


        self.horizontalLayout_2.addWidget(self.SlotGroupBox_3)

        self.SlotGroupBox_4 = QGroupBox(self.InfoGroupBox)
        self.SlotGroupBox_4.setObjectName(u"SlotGroupBox_4")
        self.SlotGroupBox_4.setMinimumSize(QSize(0, 132))
        self.SlotGroupBox_4.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.SlotGroupBox_4.setFlat(False)
        self.SlotGroupBox_4.setCheckable(False)
        self.Slot_4_Layout = QVBoxLayout(self.SlotGroupBox_4)
        self.Slot_4_Layout.setSpacing(4)
        self.Slot_4_Layout.setObjectName(u"Slot_4_Layout")
        self.Slot_4_Layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.Slot_4_Layout.setContentsMargins(6, 0, 6, 0)
        self.Slot_4_2 = QFrame(self.SlotGroupBox_4)
        self.Slot_4_2.setObjectName(u"Slot_4_2")
        self.Slot_4_2.setMinimumSize(QSize(0, 60))
        self.Slot_4_2.setStyleSheet(u".QFrame { border: 2px solid gray; }")
        self.Slot_4_2.setFrameShape(QFrame.NoFrame)
        self.Slot_4_2.setFrameShadow(QFrame.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.Slot_4_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_22 = QLabel(self.Slot_4_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font)
        self.label_22.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_22)

        self.label_slot_4 = QLabel(self.Slot_4_2)
        self.label_slot_4.setObjectName(u"label_slot_4")
        self.label_slot_4.setMinimumSize(QSize(160, 0))
        self.label_slot_4.setMargin(0)
        self.label_slot_4.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4)

        self.label_slot_4_rom = QLabel(self.Slot_4_2)
        self.label_slot_4_rom.setObjectName(u"label_slot_4_rom")
        self.label_slot_4_rom.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_rom)

        self.label_slot_4_fw = QLabel(self.Slot_4_2)
        self.label_slot_4_fw.setObjectName(u"label_slot_4_fw")
        self.label_slot_4_fw.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_fw)

        self.label_slot_4_info_1 = QLabel(self.Slot_4_2)
        self.label_slot_4_info_1.setObjectName(u"label_slot_4_info_1")
        self.label_slot_4_info_1.setMargin(0)
        self.label_slot_4_info_1.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_info_1)

        self.label_slot_4_info_2 = QLabel(self.Slot_4_2)
        self.label_slot_4_info_2.setObjectName(u"label_slot_4_info_2")
        self.label_slot_4_info_2.setMargin(0)
        self.label_slot_4_info_2.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_info_2)

        self.label_slot_4_info_3 = QLabel(self.Slot_4_2)
        self.label_slot_4_info_3.setObjectName(u"label_slot_4_info_3")
        self.label_slot_4_info_3.setMargin(0)
        self.label_slot_4_info_3.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_info_3)

        self.label_slot_4_info_4 = QLabel(self.Slot_4_2)
        self.label_slot_4_info_4.setObjectName(u"label_slot_4_info_4")
        self.label_slot_4_info_4.setMargin(0)
        self.label_slot_4_info_4.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_info_4)

        self.label_slot_4_info_5 = QLabel(self.Slot_4_2)
        self.label_slot_4_info_5.setObjectName(u"label_slot_4_info_5")
        self.label_slot_4_info_5.setMargin(0)
        self.label_slot_4_info_5.setIndent(4)

        self.verticalLayout_8.addWidget(self.label_slot_4_info_5)


        self.Slot_4_Layout.addWidget(self.Slot_4_2)


        self.horizontalLayout_2.addWidget(self.SlotGroupBox_4)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 1)

        self.verticalLayout.addWidget(self.InfoGroupBox)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 3)
        self.tab.addTab(self.tab_connect, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_12 = QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalWidget_2 = QWidget(self.tab_2)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        self.horizontalWidget_2.setMinimumSize(QSize(0, 54))
        self.horizontalLayout_15 = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(24, 4, 24, 4)
        self.label_21 = QLabel(self.horizontalWidget_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)
        self.label_21.setIndent(4)

        self.horizontalLayout_15.addWidget(self.label_21)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_22)

        self.radioButton_slot_0 = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_0.setObjectName(u"radioButton_slot_0")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_0)

        self.radioButton_slot_1 = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_1.setObjectName(u"radioButton_slot_1")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_1)

        self.radioButton_slot_2 = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_2.setObjectName(u"radioButton_slot_2")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_2)

        self.radioButton_slot_3 = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_3.setObjectName(u"radioButton_slot_3")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_3)

        self.radioButton_slot_4 = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_4.setObjectName(u"radioButton_slot_4")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_4)

        self.radioButton_slot_all = QRadioButton(self.horizontalWidget_2)
        self.radioButton_slot_all.setObjectName(u"radioButton_slot_all")

        self.horizontalLayout_15.addWidget(self.radioButton_slot_all)


        self.verticalLayout_12.addWidget(self.horizontalWidget_2)

        self.horizontalWidget_3 = QWidget(self.tab_2)
        self.horizontalWidget_3.setObjectName(u"horizontalWidget_3")
        self.horizontalWidget_3.setMinimumSize(QSize(0, 54))
        self.horizontalLayout_16 = QHBoxLayout(self.horizontalWidget_3)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(24, 4, 24, 4)
        self.pushButton_setting = QPushButton(self.horizontalWidget_3)
        self.pushButton_setting.setObjectName(u"pushButton_setting")
        self.pushButton_setting.setMinimumSize(QSize(200, 0))
        self.pushButton_setting.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_16.addWidget(self.pushButton_setting)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_2)


        self.verticalLayout_12.addWidget(self.horizontalWidget_3)

        self.spd_operation = QGroupBox(self.tab_2)
        self.spd_operation.setObjectName(u"spd_operation")
        self.spd_operation.setMinimumSize(QSize(0, 75))
        self.spd_operation.setStyleSheet(u"QGroupBox{ font-weight: bold; }")
        self.horizontalLayout_9 = QHBoxLayout(self.spd_operation)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(24, 4, 24, 4)
        self.pushButton_read_board = QPushButton(self.spd_operation)
        self.pushButton_read_board.setObjectName(u"pushButton_read_board")
        self.pushButton_read_board.setMinimumSize(QSize(160, 0))
        self.pushButton_read_board.setMaximumSize(QSize(160, 16777215))
        self.pushButton_read_board.setFocusPolicy(Qt.StrongFocus)
        self.pushButton_read_board.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_read_board.setAutoDefault(False)

        self.horizontalLayout_9.addWidget(self.pushButton_read_board)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.pushButton_read = QPushButton(self.spd_operation)
        self.pushButton_read.setObjectName(u"pushButton_read")
        self.pushButton_read.setMinimumSize(QSize(160, 0))
        self.pushButton_read.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_9.addWidget(self.pushButton_read)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.horizontalLayout_9.setStretch(1, 1)
        self.horizontalLayout_9.setStretch(2, 1)

        self.verticalLayout_12.addWidget(self.spd_operation)

        self.horizontalWidget = QWidget(self.tab_2)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        self.horizontalWidget.setMinimumSize(QSize(0, 54))
        self.horizontalLayout_14 = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(24, 4, 24, 4)
        self.label_read_byte = QLabel(self.horizontalWidget)
        self.label_read_byte.setObjectName(u"label_read_byte")
        self.label_read_byte.setIndent(4)

        self.horizontalLayout_14.addWidget(self.label_read_byte)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_23)

        self.radioButton_page_1 = QRadioButton(self.horizontalWidget)
        self.radioButton_page_1.setObjectName(u"radioButton_page_1")
        self.radioButton_page_1.setChecked(True)

        self.horizontalLayout_14.addWidget(self.radioButton_page_1)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_25)

        self.radioButton_page_2 = QRadioButton(self.horizontalWidget)
        self.radioButton_page_2.setObjectName(u"radioButton_page_2")

        self.horizontalLayout_14.addWidget(self.radioButton_page_2)


        self.verticalLayout_12.addWidget(self.horizontalWidget)

        self.verticalWidget = QWidget(self.tab_2)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalLayout_11 = QVBoxLayout(self.verticalWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.Table_spd_2 = QTableWidget(self.verticalWidget)
        if (self.Table_spd_2.columnCount() < 16):
            self.Table_spd_2.setColumnCount(16)
        __qtablewidgetitem = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(14, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.Table_spd_2.setHorizontalHeaderItem(15, __qtablewidgetitem15)
        if (self.Table_spd_2.rowCount() < 32):
            self.Table_spd_2.setRowCount(32)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(4, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(5, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(6, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(7, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(8, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(9, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(10, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(11, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(12, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(13, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(14, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(15, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(16, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(17, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(18, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(19, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(20, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(21, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(22, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(23, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(24, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(25, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(26, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(27, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(28, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(29, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(30, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.Table_spd_2.setVerticalHeaderItem(31, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.Table_spd_2.setItem(0, 0, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.Table_spd_2.setItem(0, 1, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.Table_spd_2.setItem(0, 2, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.Table_spd_2.setItem(1, 0, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.Table_spd_2.setItem(1, 1, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.Table_spd_2.setItem(1, 2, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.Table_spd_2.setItem(2, 0, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.Table_spd_2.setItem(2, 1, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.Table_spd_2.setItem(2, 2, __qtablewidgetitem56)
        self.Table_spd_2.setObjectName(u"Table_spd_2")
        sizePolicy.setHeightForWidth(self.Table_spd_2.sizePolicy().hasHeightForWidth())
        self.Table_spd_2.setSizePolicy(sizePolicy)
        self.Table_spd_2.setMinimumSize(QSize(850, 0))
        self.Table_spd_2.setMaximumSize(QSize(850, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        self.Table_spd_2.setFont(font1)
        self.Table_spd_2.setStyleSheet(u"QHeaderView::section::horizontal {border: 1px solid black;}\n"
"QHeaderView::section::vertical {border: 1px solid black;}")
        self.Table_spd_2.setFrameShape(QFrame.Panel)
        self.Table_spd_2.setFrameShadow(QFrame.Plain)
        self.Table_spd_2.setLineWidth(1)
        self.Table_spd_2.setMidLineWidth(0)
        self.Table_spd_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.Table_spd_2.setAutoScrollMargin(12)
        self.Table_spd_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Table_spd_2.setTextElideMode(Qt.ElideMiddle)
        self.Table_spd_2.setShowGrid(True)
        self.Table_spd_2.setSortingEnabled(False)
        self.Table_spd_2.setWordWrap(True)
        self.Table_spd_2.horizontalHeader().setCascadingSectionResizes(False)
        self.Table_spd_2.horizontalHeader().setMinimumSectionSize(16)
        self.Table_spd_2.horizontalHeader().setDefaultSectionSize(16)
        self.Table_spd_2.horizontalHeader().setProperty("showSortIndicator", False)
        self.Table_spd_2.horizontalHeader().setStretchLastSection(False)
        self.Table_spd_2.verticalHeader().setCascadingSectionResizes(False)
        self.Table_spd_2.verticalHeader().setMinimumSectionSize(16)
        self.Table_spd_2.verticalHeader().setDefaultSectionSize(16)
        self.Table_spd_2.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_11.addWidget(self.Table_spd_2)


        self.verticalLayout_12.addWidget(self.verticalWidget)

        self.verticalLayout_12.setStretch(0, 1)
        self.verticalLayout_12.setStretch(1, 1)
        self.verticalLayout_12.setStretch(2, 1)
        self.verticalLayout_12.setStretch(3, 1)
        self.verticalLayout_12.setStretch(4, 7)
        self.tab.addTab(self.tab_2, "")
        self.tab_online = QWidget()
        self.tab_online.setObjectName(u"tab_online")
        self.verticalLayout_9 = QVBoxLayout(self.tab_online)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.SettingWidget_2 = QWidget(self.tab_online)
        self.SettingWidget_2.setObjectName(u"SettingWidget_2")
        self.SettingWidget_2.setMinimumSize(QSize(0, 600))
        self.OptionLayout_2 = QVBoxLayout(self.SettingWidget_2)
        self.OptionLayout_2.setSpacing(6)
        self.OptionLayout_2.setObjectName(u"OptionLayout_2")
        self.OptionLayout_2.setContentsMargins(6, 0, 6, 0)
        self.verticalGroupBox = QGroupBox(self.SettingWidget_2)
        self.verticalGroupBox.setObjectName(u"verticalGroupBox")
        self.verticalGroupBox.setMinimumSize(QSize(0, 120))
        self.verticalGroupBox.setStyleSheet(u"QGroupBox{ font-weight: bold; }")
        self.verticalLayout_15 = QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.File_Layout = QWidget(self.verticalGroupBox)
        self.File_Layout.setObjectName(u"File_Layout")
        self.File_Layout.setMinimumSize(QSize(0, 45))
        self.horizontalLayout_4 = QHBoxLayout(self.File_Layout)
        self.horizontalLayout_4.setSpacing(12)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(24, 0, 24, 0)
        self.label_15 = QLabel(self.File_Layout)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(120, 0))
        self.label_15.setMargin(0)
        self.label_15.setIndent(4)

        self.horizontalLayout_4.addWidget(self.label_15)

        self.lineEdit_ap = QLineEdit(self.File_Layout)
        self.lineEdit_ap.setObjectName(u"lineEdit_ap")

        self.horizontalLayout_4.addWidget(self.lineEdit_ap)

        self.horizontalSpacer_24 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_24)

        self.btn_ap = QPushButton(self.File_Layout)
        self.btn_ap.setObjectName(u"btn_ap")
        self.btn_ap.setMinimumSize(QSize(160, 0))
        self.btn_ap.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_4.addWidget(self.btn_ap)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 6)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 2)

        self.verticalLayout_15.addWidget(self.File_Layout)

        self.File_APROM_Info = QWidget(self.verticalGroupBox)
        self.File_APROM_Info.setObjectName(u"File_APROM_Info")
        self.File_APROM_Info.setMinimumSize(QSize(0, 45))
        self.File_APROM_Info.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_7 = QHBoxLayout(self.File_APROM_Info)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(24, 0, 24, 0)
        self.horizontalSpacer_17 = QSpacerItem(120, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_17)

        self.label_file_size = QLabel(self.File_APROM_Info)
        self.label_file_size.setObjectName(u"label_file_size")
        self.label_file_size.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_file_size.setIndent(8)

        self.horizontalLayout_7.addWidget(self.label_file_size)

        self.label_file_checksum = QLabel(self.File_APROM_Info)
        self.label_file_checksum.setObjectName(u"label_file_checksum")
        self.label_file_checksum.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_file_checksum.setIndent(4)

        self.horizontalLayout_7.addWidget(self.label_file_checksum)

        self.horizontalSpacer_21 = QSpacerItem(160, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_21)


        self.verticalLayout_15.addWidget(self.File_APROM_Info)

        self.horizontalWidget_4 = QWidget(self.verticalGroupBox)
        self.horizontalWidget_4.setObjectName(u"horizontalWidget_4")
        self.horizontalWidget_4.setMinimumSize(QSize(0, 45))
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalWidget_4)
        self.horizontalLayout_10.setSpacing(12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(24, 0, 24, 0)
        self.label = QLabel(self.horizontalWidget_4)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setIndent(4)

        self.horizontalLayout_10.addWidget(self.label)

        self.lineEdit_spd = QLineEdit(self.horizontalWidget_4)
        self.lineEdit_spd.setObjectName(u"lineEdit_spd")

        self.horizontalLayout_10.addWidget(self.lineEdit_spd)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)

        self.btn_spd = QPushButton(self.horizontalWidget_4)
        self.btn_spd.setObjectName(u"btn_spd")
        self.btn_spd.setMinimumSize(QSize(160, 0))
        self.btn_spd.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_10.addWidget(self.btn_spd)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 6)
        self.horizontalLayout_10.setStretch(2, 1)
        self.horizontalLayout_10.setStretch(3, 2)

        self.verticalLayout_15.addWidget(self.horizontalWidget_4)

        self.verticalLayout_15.setStretch(0, 1)
        self.verticalLayout_15.setStretch(1, 1)
        self.verticalLayout_15.setStretch(2, 1)

        self.OptionLayout_2.addWidget(self.verticalGroupBox)

        self.Setting = QGroupBox(self.SettingWidget_2)
        self.Setting.setObjectName(u"Setting")
        self.Setting.setMinimumSize(QSize(0, 240))
        self.verticalLayout_7 = QVBoxLayout(self.Setting)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.Layout_Select_2 = QWidget(self.Setting)
        self.Layout_Select_2.setObjectName(u"Layout_Select_2")
        self.Layout_Select_2.setMinimumSize(QSize(0, 60))
        self.Slot_Select_Layout_2 = QHBoxLayout(self.Layout_Select_2)
        self.Slot_Select_Layout_2.setSpacing(4)
        self.Slot_Select_Layout_2.setObjectName(u"Slot_Select_Layout_2")
        self.Slot_Select_Layout_2.setContentsMargins(24, 0, 24, 0)
        self.label_17 = QLabel(self.Layout_Select_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(160, 0))
        self.label_17.setMargin(0)
        self.label_17.setIndent(4)

        self.Slot_Select_Layout_2.addWidget(self.label_17)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Slot_Select_Layout_2.addItem(self.horizontalSpacer_18)

        self.checkBox_slot_0 = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_0.setObjectName(u"checkBox_slot_0")
        self.checkBox_slot_0.setMinimumSize(QSize(100, 0))
        self.checkBox_slot_0.setMaximumSize(QSize(100, 16777215))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_0)

        self.checkBox_slot_1 = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_1.setObjectName(u"checkBox_slot_1")
        self.checkBox_slot_1.setMinimumSize(QSize(100, 0))
        self.checkBox_slot_1.setMaximumSize(QSize(100, 16777215))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_1)

        self.checkBox_slot_2 = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_2.setObjectName(u"checkBox_slot_2")
        self.checkBox_slot_2.setMinimumSize(QSize(100, 0))
        self.checkBox_slot_2.setMaximumSize(QSize(100, 16777215))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_2)

        self.checkBox_slot_3 = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_3.setObjectName(u"checkBox_slot_3")
        self.checkBox_slot_3.setMinimumSize(QSize(100, 0))
        self.checkBox_slot_3.setMaximumSize(QSize(100, 16777215))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_3)

        self.checkBox_slot_4 = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_4.setObjectName(u"checkBox_slot_4")
        self.checkBox_slot_4.setEnabled(True)
        self.checkBox_slot_4.setMinimumSize(QSize(100, 0))
        self.checkBox_slot_4.setMaximumSize(QSize(100, 16777215))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_4)

        self.checkBox_slot_all = QCheckBox(self.Layout_Select_2)
        self.checkBox_slot_all.setObjectName(u"checkBox_slot_all")
        self.checkBox_slot_all.setMinimumSize(QSize(80, 0))

        self.Slot_Select_Layout_2.addWidget(self.checkBox_slot_all)

        self.Slot_Select_Layout_2.setStretch(0, 1)
        self.Slot_Select_Layout_2.setStretch(1, 1)
        self.Slot_Select_Layout_2.setStretch(2, 1)
        self.Slot_Select_Layout_2.setStretch(3, 1)
        self.Slot_Select_Layout_2.setStretch(4, 1)
        self.Slot_Select_Layout_2.setStretch(5, 1)
        self.Slot_Select_Layout_2.setStretch(6, 1)

        self.verticalLayout_7.addWidget(self.Layout_Select_2)

        self.Layout_Offline = QWidget(self.Setting)
        self.Layout_Offline.setObjectName(u"Layout_Offline")
        self.Layout_Offline.setMinimumSize(QSize(0, 60))
        self.horizontalLayout = QHBoxLayout(self.Layout_Offline)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(24, 0, 24, 0)
        self.label_9 = QLabel(self.Layout_Offline)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(160, 0))
        self.label_9.setIndent(4)

        self.horizontalLayout.addWidget(self.label_9)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.radioButton_online = QRadioButton(self.Layout_Offline)
        self.radioButton_online.setObjectName(u"radioButton_online")
        self.radioButton_online.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_online)

        self.radioButton_offline = QRadioButton(self.Layout_Offline)
        self.radioButton_offline.setObjectName(u"radioButton_offline")

        self.horizontalLayout.addWidget(self.radioButton_offline)


        self.verticalLayout_7.addWidget(self.Layout_Offline)

        self.horizontalWidget_1 = QWidget(self.Setting)
        self.horizontalWidget_1.setObjectName(u"horizontalWidget_1")
        self.horizontalLayout_13 = QHBoxLayout(self.horizontalWidget_1)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(24, 0, 24, 0)
        self.label_2 = QLabel(self.horizontalWidget_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setIndent(4)

        self.horizontalLayout_13.addWidget(self.label_2)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_8)

        self.checkBox_ap = QCheckBox(self.horizontalWidget_1)
        self.checkBox_ap.setObjectName(u"checkBox_ap")

        self.horizontalLayout_13.addWidget(self.checkBox_ap)

        self.horizontalSpacer_19 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_19)

        self.checkBox_spd = QCheckBox(self.horizontalWidget_1)
        self.checkBox_spd.setObjectName(u"checkBox_spd")

        self.horizontalLayout_13.addWidget(self.checkBox_spd)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_7)


        self.verticalLayout_7.addWidget(self.horizontalWidget_1)

        self.horizontalWidget_5 = QWidget(self.Setting)
        self.horizontalWidget_5.setObjectName(u"horizontalWidget_5")
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalWidget_5)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.btn_program = QPushButton(self.horizontalWidget_5)
        self.btn_program.setObjectName(u"btn_program")
        self.btn_program.setMinimumSize(QSize(160, 0))
        self.btn_program.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_11.addWidget(self.btn_program)


        self.verticalLayout_7.addWidget(self.horizontalWidget_5)

        self.Layout_Bar = QWidget(self.Setting)
        self.Layout_Bar.setObjectName(u"Layout_Bar")
        self.Layout_Bar.setMinimumSize(QSize(0, 60))
        self.horizontalLayout_8 = QHBoxLayout(self.Layout_Bar)
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(24, 0, 24, 0)
        self.label_progress_state = QLabel(self.Layout_Bar)
        self.label_progress_state.setObjectName(u"label_progress_state")
        self.label_progress_state.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_8.addWidget(self.label_progress_state)

        self.progressBar = QProgressBar(self.Layout_Bar)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_8.addWidget(self.progressBar)


        self.verticalLayout_7.addWidget(self.Layout_Bar)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 1)
        self.verticalLayout_7.setStretch(3, 1)
        self.verticalLayout_7.setStretch(4, 1)

        self.OptionLayout_2.addWidget(self.Setting)

        self.OptionLayout_2.setStretch(0, 3)
        self.OptionLayout_2.setStretch(1, 5)

        self.verticalLayout_9.addWidget(self.SettingWidget_2)

        self.tab.addTab(self.tab_online, "")

        self.verticalLayout_2.addWidget(self.tab)

        self.verticalGroupBox_1 = QGroupBox(self.scrollAreaWidgetContents)
        self.verticalGroupBox_1.setObjectName(u"verticalGroupBox_1")
        self.verticalGroupBox_1.setMinimumSize(QSize(0, 220))
        self.verticalLayout_16 = QVBoxLayout(self.verticalGroupBox_1)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(4, 8, 4, 4)
        self.text_browser = QTextBrowser(self.verticalGroupBox_1)
        self.text_browser.setObjectName(u"text_browser")
        self.text_browser.setMinimumSize(QSize(0, 200))

        self.verticalLayout_16.addWidget(self.text_browser)


        self.verticalLayout_2.addWidget(self.verticalGroupBox_1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1026, 18))
        self.menubar.setDefaultUp(False)
        self.menuProject = QMenu(self.menubar)
        self.menuProject.setObjectName(u"menuProject")
        self.menuProject.setGeometry(QRect(158, 103, 110, 93))
        self.menuSPD_Info = QMenu(self.menubar)
        self.menuSPD_Info.setObjectName(u"menuSPD_Info")
        self.menuEdit_SPD_Information = QMenu(self.menuSPD_Info)
        self.menuEdit_SPD_Information.setObjectName(u"menuEdit_SPD_Information")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuSPD_Info.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuProject.addAction(self.actionLoad_Setting)
        self.menuProject.addAction(self.actionSave_Setting)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionSerial_Checker)
        self.menuSPD_Info.addSeparator()
        self.menuSPD_Info.addAction(self.actionImport_SPD_file)
        self.menuSPD_Info.addAction(self.actionExport_SPD_file)
        self.menuSPD_Info.addAction(self.menuEdit_SPD_Information.menuAction())
        self.menuEdit_SPD_Information.addAction(self.actionSPD_Information_Setting)
        self.menuHelp.addAction(self.actionUser_Manual)
        self.menuHelp.addAction(self.actionVersion)

        self.retranslateUi(MainWindow)

        self.tab.setCurrentIndex(2)
        self.btn_connect.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_Setting.setText(QCoreApplication.translate("MainWindow", u"Load Setting", None))
        self.actionSave_Setting.setText(QCoreApplication.translate("MainWindow", u"Save Setting", None))
        self.actionOffline_Setting.setText(QCoreApplication.translate("MainWindow", u"Write bin into Data Flash", None))
        self.actionExport_SPD_Information.setText(QCoreApplication.translate("MainWindow", u"Export SPD Information", None))
        self.actionImport_SPD_Information.setText(QCoreApplication.translate("MainWindow", u"Import SPD Information", None))
        self.actionShow_SPD_Information.setText(QCoreApplication.translate("MainWindow", u"SPD Information Setting (Complete)", None))
        self.actionSPD_Information_Setting.setText(QCoreApplication.translate("MainWindow", u"SPD Information Setting (Simple)", None))
        self.actionImport_SPD_file.setText(QCoreApplication.translate("MainWindow", u"Import SPD file", None))
        self.actionExport_SPD_file.setText(QCoreApplication.translate("MainWindow", u"Export SPD file", None))
        self.actionSimple.setText(QCoreApplication.translate("MainWindow", u"Simple", None))
        self.actionUser_Manual.setText(QCoreApplication.translate("MainWindow", u"User Manual", None))
        self.actionVersion.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.actionExtend_Modes.setText(QCoreApplication.translate("MainWindow", u"Extend Mode", None))
        self.actionExtend_Mode.setText(QCoreApplication.translate("MainWindow", u"Extend_Mode", None))
        self.actionSerial_Checker.setText(QCoreApplication.translate("MainWindow", u"Serial Checker", None))
        self.label_nuvoton.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ConnectGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"USB Connection", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_connect.setText(QCoreApplication.translate("MainWindow", u"USB Status: Disconnected ", None))
        self.horizontalGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"DIMM Connection", None))
        self.btn_slot.setText(QCoreApplication.translate("MainWindow", u"Check Connection", None))
        self.InfoGroupBox.setTitle(QCoreApplication.translate("MainWindow", u" Slot Information", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"SLOT 0", None))
        self.label_slot_0.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.label_slot_0_rom.setText(QCoreApplication.translate("MainWindow", u"Boot Status: None", None))
        self.label_slot_0_fw.setText(QCoreApplication.translate("MainWindow", u"FW Version: NAN", None))
        self.label_slot_0_info_1.setText(QCoreApplication.translate("MainWindow", u"Customer ID: NAN", None))
        self.label_slot_0_info_2.setText(QCoreApplication.translate("MainWindow", u"Chip ID: NAN", None))
        self.label_slot_0_info_3.setText(QCoreApplication.translate("MainWindow", u"LED ID: NAN", None))
        self.label_slot_0_info_4.setText(QCoreApplication.translate("MainWindow", u"Project ID: NAN", None))
        self.label_slot_0_info_5.setText(QCoreApplication.translate("MainWindow", u"FT ID: NAN", None))
        self.SlotGroupBox_1.setTitle("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"SLOT 1", None))
        self.label_slot_1.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.label_slot_1_rom.setText(QCoreApplication.translate("MainWindow", u"Boot Status: None", None))
        self.label_slot_1_fw.setText(QCoreApplication.translate("MainWindow", u"FW Version: NAN", None))
        self.label_slot_1_info_1.setText(QCoreApplication.translate("MainWindow", u"Customer ID: NAN", None))
        self.label_slot_1_info_2.setText(QCoreApplication.translate("MainWindow", u"Chip ID: NAN", None))
        self.label_slot_1_info_3.setText(QCoreApplication.translate("MainWindow", u"LED ID: NAN", None))
        self.label_slot_1_info_4.setText(QCoreApplication.translate("MainWindow", u"Project ID: NAN", None))
        self.label_slot_1_info_5.setText(QCoreApplication.translate("MainWindow", u"FT ID: NAN", None))
        self.SlotGroupBox_2.setTitle("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"SLOT 2", None))
        self.label_slot_2.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.label_slot_2_rom.setText(QCoreApplication.translate("MainWindow", u"Boot Status: None", None))
        self.label_slot_2_fw.setText(QCoreApplication.translate("MainWindow", u"FW Version: NAN", None))
        self.label_slot_2_info_1.setText(QCoreApplication.translate("MainWindow", u"Customer ID: NAN", None))
        self.label_slot_2_info_2.setText(QCoreApplication.translate("MainWindow", u"Chip ID: NAN", None))
        self.label_slot_2_info_3.setText(QCoreApplication.translate("MainWindow", u"LED ID: NAN", None))
        self.label_slot_2_info_4.setText(QCoreApplication.translate("MainWindow", u"Project ID: NAN", None))
        self.label_slot_2_info_5.setText(QCoreApplication.translate("MainWindow", u"FT ID: NAN", None))
        self.SlotGroupBox_3.setTitle("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"SLOT 3", None))
        self.label_slot_3.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.label_slot_3_rom.setText(QCoreApplication.translate("MainWindow", u"Boot Status: None", None))
        self.label_slot_3_fw.setText(QCoreApplication.translate("MainWindow", u"FW Version: NAN", None))
        self.label_slot_3_info_1.setText(QCoreApplication.translate("MainWindow", u"Customer ID: NAN", None))
        self.label_slot_3_info_2.setText(QCoreApplication.translate("MainWindow", u"Chip ID: NAN", None))
        self.label_slot_3_info_3.setText(QCoreApplication.translate("MainWindow", u"LED ID: NAN", None))
        self.label_slot_3_info_4.setText(QCoreApplication.translate("MainWindow", u"Project ID: NAN", None))
        self.label_slot_3_info_5.setText(QCoreApplication.translate("MainWindow", u"FT ID: NAN", None))
        self.SlotGroupBox_4.setTitle("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"SLOT 4", None))
        self.label_slot_4.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.label_slot_4_rom.setText(QCoreApplication.translate("MainWindow", u"Boot Status: None", None))
        self.label_slot_4_fw.setText(QCoreApplication.translate("MainWindow", u"FW Version: NAN", None))
        self.label_slot_4_info_1.setText(QCoreApplication.translate("MainWindow", u"Customer ID: NAN", None))
        self.label_slot_4_info_2.setText(QCoreApplication.translate("MainWindow", u"Chip ID: NAN", None))
        self.label_slot_4_info_3.setText(QCoreApplication.translate("MainWindow", u"LED ID: NAN", None))
        self.label_slot_4_info_4.setText(QCoreApplication.translate("MainWindow", u"Project ID: NAN", None))
        self.label_slot_4_info_5.setText(QCoreApplication.translate("MainWindow", u"FT ID: NAN", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_connect), QCoreApplication.translate("MainWindow", u"Connection and Information", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"SLOT Selection", None))
        self.radioButton_slot_0.setText(QCoreApplication.translate("MainWindow", u"SLOT 0", None))
        self.radioButton_slot_1.setText(QCoreApplication.translate("MainWindow", u"SLOT 1", None))
        self.radioButton_slot_2.setText(QCoreApplication.translate("MainWindow", u"SLOT 2", None))
        self.radioButton_slot_3.setText(QCoreApplication.translate("MainWindow", u"SLOT 3", None))
        self.radioButton_slot_4.setText(QCoreApplication.translate("MainWindow", u"SLOT 4", None))
        self.radioButton_slot_all.setText(QCoreApplication.translate("MainWindow", u"ALL SLOT", None))
        self.pushButton_setting.setText(QCoreApplication.translate("MainWindow", u"Show SPD Information", None))
        self.spd_operation.setTitle(QCoreApplication.translate("MainWindow", u"SPD Operation", None))
        self.pushButton_read_board.setText(QCoreApplication.translate("MainWindow", u"Read from Board", None))
        self.pushButton_read.setText(QCoreApplication.translate("MainWindow", u"Read from DIMM", None))
        self.label_read_byte.setText(QCoreApplication.translate("MainWindow", u"Byte 0x000 (0)", None))
        self.radioButton_page_1.setText(QCoreApplication.translate("MainWindow", u"byte 0 ~ 511", None))
        self.radioButton_page_2.setText(QCoreApplication.translate("MainWindow", u"byte 512 ~ 1023", None))
        ___qtablewidgetitem = self.Table_spd_2.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem1 = self.Table_spd_2.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem2 = self.Table_spd_2.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem3 = self.Table_spd_2.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem4 = self.Table_spd_2.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"4", None));
        ___qtablewidgetitem5 = self.Table_spd_2.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qtablewidgetitem6 = self.Table_spd_2.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"6", None));
        ___qtablewidgetitem7 = self.Table_spd_2.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"7", None));
        ___qtablewidgetitem8 = self.Table_spd_2.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"8", None));
        ___qtablewidgetitem9 = self.Table_spd_2.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"9", None));
        ___qtablewidgetitem10 = self.Table_spd_2.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"A", None));
        ___qtablewidgetitem11 = self.Table_spd_2.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"B", None));
        ___qtablewidgetitem12 = self.Table_spd_2.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"C", None));
        ___qtablewidgetitem13 = self.Table_spd_2.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"D", None));
        ___qtablewidgetitem14 = self.Table_spd_2.horizontalHeaderItem(14)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"E", None));
        ___qtablewidgetitem15 = self.Table_spd_2.horizontalHeaderItem(15)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"F", None));
        ___qtablewidgetitem16 = self.Table_spd_2.verticalHeaderItem(0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"000", None));
        ___qtablewidgetitem17 = self.Table_spd_2.verticalHeaderItem(1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"010", None));
        ___qtablewidgetitem18 = self.Table_spd_2.verticalHeaderItem(2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"020", None));
        ___qtablewidgetitem19 = self.Table_spd_2.verticalHeaderItem(3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"030", None));
        ___qtablewidgetitem20 = self.Table_spd_2.verticalHeaderItem(4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"040", None));
        ___qtablewidgetitem21 = self.Table_spd_2.verticalHeaderItem(5)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"050", None));
        ___qtablewidgetitem22 = self.Table_spd_2.verticalHeaderItem(6)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"060", None));
        ___qtablewidgetitem23 = self.Table_spd_2.verticalHeaderItem(7)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"070", None));
        ___qtablewidgetitem24 = self.Table_spd_2.verticalHeaderItem(8)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"080", None));
        ___qtablewidgetitem25 = self.Table_spd_2.verticalHeaderItem(9)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"090", None));
        ___qtablewidgetitem26 = self.Table_spd_2.verticalHeaderItem(10)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"0A0", None));
        ___qtablewidgetitem27 = self.Table_spd_2.verticalHeaderItem(11)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"0B0", None));
        ___qtablewidgetitem28 = self.Table_spd_2.verticalHeaderItem(12)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"0C0", None));
        ___qtablewidgetitem29 = self.Table_spd_2.verticalHeaderItem(13)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"0D0", None));
        ___qtablewidgetitem30 = self.Table_spd_2.verticalHeaderItem(14)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"0E0", None));
        ___qtablewidgetitem31 = self.Table_spd_2.verticalHeaderItem(15)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"0F0", None));
        ___qtablewidgetitem32 = self.Table_spd_2.verticalHeaderItem(16)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"100", None));
        ___qtablewidgetitem33 = self.Table_spd_2.verticalHeaderItem(17)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"110", None));
        ___qtablewidgetitem34 = self.Table_spd_2.verticalHeaderItem(18)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"120", None));
        ___qtablewidgetitem35 = self.Table_spd_2.verticalHeaderItem(19)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"130", None));
        ___qtablewidgetitem36 = self.Table_spd_2.verticalHeaderItem(20)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"140", None));
        ___qtablewidgetitem37 = self.Table_spd_2.verticalHeaderItem(21)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"150", None));
        ___qtablewidgetitem38 = self.Table_spd_2.verticalHeaderItem(22)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"160", None));
        ___qtablewidgetitem39 = self.Table_spd_2.verticalHeaderItem(23)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"170", None));
        ___qtablewidgetitem40 = self.Table_spd_2.verticalHeaderItem(24)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"180", None));
        ___qtablewidgetitem41 = self.Table_spd_2.verticalHeaderItem(25)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"190", None));
        ___qtablewidgetitem42 = self.Table_spd_2.verticalHeaderItem(26)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"1A0", None));
        ___qtablewidgetitem43 = self.Table_spd_2.verticalHeaderItem(27)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"1B0", None));
        ___qtablewidgetitem44 = self.Table_spd_2.verticalHeaderItem(28)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"1C0", None));
        ___qtablewidgetitem45 = self.Table_spd_2.verticalHeaderItem(29)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"1D0", None));
        ___qtablewidgetitem46 = self.Table_spd_2.verticalHeaderItem(30)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"1E0", None));
        ___qtablewidgetitem47 = self.Table_spd_2.verticalHeaderItem(31)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"1F0", None));

        __sortingEnabled = self.Table_spd_2.isSortingEnabled()
        self.Table_spd_2.setSortingEnabled(False)
        ___qtablewidgetitem48 = self.Table_spd_2.item(0, 0)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem49 = self.Table_spd_2.item(0, 1)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem50 = self.Table_spd_2.item(0, 2)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem51 = self.Table_spd_2.item(1, 0)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem52 = self.Table_spd_2.item(1, 1)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem53 = self.Table_spd_2.item(1, 2)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem54 = self.Table_spd_2.item(2, 0)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem55 = self.Table_spd_2.item(2, 1)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        ___qtablewidgetitem56 = self.Table_spd_2.item(2, 2)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("MainWindow", u"FF", None));
        self.Table_spd_2.setSortingEnabled(__sortingEnabled)

        self.tab.setTabText(self.tab.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"SPD Information", None))
        self.verticalGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"File Information", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"APROM File:", None))
        self.btn_ap.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_file_size.setText(QCoreApplication.translate("MainWindow", u"APROM File Size: 00000000 Bytes", None))
        self.label_file_checksum.setText(QCoreApplication.translate("MainWindow", u"APROM File Checksum: 0xFFFF", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"SPD File:", None))
        self.btn_spd.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.Setting.setTitle("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"SLOT Selection:", None))
        self.checkBox_slot_0.setText(QCoreApplication.translate("MainWindow", u"SLOT 0", None))
        self.checkBox_slot_1.setText(QCoreApplication.translate("MainWindow", u"SLOT 1", None))
        self.checkBox_slot_2.setText(QCoreApplication.translate("MainWindow", u"SLOT 2", None))
        self.checkBox_slot_3.setText(QCoreApplication.translate("MainWindow", u"SLOT 3", None))
        self.checkBox_slot_4.setText(QCoreApplication.translate("MainWindow", u"SLOT 4", None))
        self.checkBox_slot_all.setText(QCoreApplication.translate("MainWindow", u"All SLOT", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Mode Selection", None))
        self.radioButton_online.setText(QCoreApplication.translate("MainWindow", u"Online Mode", None))
        self.radioButton_offline.setText(QCoreApplication.translate("MainWindow", u"Offline Mode with SPD", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Programming Selection", None))
        self.checkBox_ap.setText(QCoreApplication.translate("MainWindow", u"APROM", None))
        self.checkBox_spd.setText(QCoreApplication.translate("MainWindow", u"SPD", None))
        self.btn_program.setText(QCoreApplication.translate("MainWindow", u"Program", None))
        self.label_progress_state.setText(QCoreApplication.translate("MainWindow", u"Progress: Writing", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_online), QCoreApplication.translate("MainWindow", u"Programming Setting", None))
        self.verticalGroupBox_1.setTitle(QCoreApplication.translate("MainWindow", u"Message Stack", None))
        self.menuProject.setTitle(QCoreApplication.translate("MainWindow", u"Project", None))
        self.menuSPD_Info.setTitle(QCoreApplication.translate("MainWindow", u"SPD Info", None))
        self.menuEdit_SPD_Information.setTitle(QCoreApplication.translate("MainWindow", u"Edit SPD Information", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

