import ctypes
import math
import os
import serial
import sys 
import struct

import time
import hid

from ctypes import *
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, QRegExp, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QTextCursor, QIcon, QColor, QBrush, QPixmap
from webbrowser import open_new

from DDR_mainwindow_tab_debug_2 import Ui_MainWindow
from DDR_config import Dialog_Ui_2
from DDR_config_spd_simple import Dialog_Ui_3
from DDR_checker_ui import Dialog_Ui_4
from FlashInfo import *
from PartNumID import *

VOIDFUNCTYPE = CFUNCTYPE(c_void_p)
UINTFUNCTYPE = CFUNCTYPE(c_uint)
RWFUNCTYPE = CFUNCTYPE(c_uint, c_uint, POINTER(c_ubyte))

APP_MODE = False

version_number = "08"
pack_size = 1024

class DEV_IO(Structure):
    _fields_ = [
        ("init",CFUNCTYPE(c_void_p)),                           # be called at init state
        ("open",CFUNCTYPE(c_uint)),                             # return True or False
        ("close",CFUNCTYPE(c_void_p)),                          # no return 
        ("write",CFUNCTYPE(c_uint, c_uint, POINTER(c_ubyte))),  # return 1 when success, 0 when fail
        ("read",CFUNCTYPE(c_uint, c_uint, POINTER(c_ubyte))),   # return read value length
    ]
                
class io_handle_t(Structure):
    _fields_ = [
        ("dev_open", c_uint),
        ("bResendFlag", c_uint),
        ("m_usCheckSum",c_ubyte),
        ("ac_buffer",c_ubyte * (pack_size + 1)),
        ("dev_io",POINTER(c_void_p)),
        ("m_dev_io",DEV_IO),
    ]


class USB_dev_io:

    dev = None
    
    def _init_(self):
        self.dev = None
    
    def USB_init(self):
        self.dev = hid.device()
    
    def USB_open(self):
        test = 0;
        if self.dev == None:
            self.dev = hid.device()
            
        try:
            self.dev.open(0x0416, 0x5020)
        except Exception as e:
            test = 1
            
        if (test > 0):
            print('USB not found')
            return False
        else: 
            print('Get USB information')
            return True
    
    def USB_close(self):
        try:
            if self.dev != None:
                self.dev.close()
            self.dev = None
            print('Close USB Connection')
            
        except Exception as e:
            print(f"Exception occurred: {e}")
            import traceback
            traceback.print_exc()
            
    def USB_write(self, Ctime, buffer):
        try:
            data = (c_ubyte * (pack_size + 1)).from_address(ctypes.addressof(buffer.contents))
            bytes_data = bytearray(data)
            bytes_written = self.dev.write(bytes_data)
            if bytes_written >= len(bytes_data):
                return 1
            else:
                return 0
                
        except Exception as e:
            print(f"Exception occurred: {e}")
            import traceback
            traceback.print_exc()
            return 0
        
    def USB_read(self, Ctime, buffer):
        try:
            return_str = self.dev.read((pack_size + 1), 8000) #return by string
            
            buffer_as_bytes = (c_ubyte * (len(return_str)+1))()
            buffer_as_bytes[1:] = return_str
            memmove(buffer, buffer_as_bytes, len(buffer_as_bytes))
            #print(bytearray(buffer_as_bytes[0:10]), len(buffer_as_bytes) - 1)
            return len(buffer_as_bytes) - 1
            
        except Exception as e:
            print(f"Exception occurred: {e}")
            import traceback
            traceback.print_exc()
            return 0
            
class Worker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    update_progress_signal = pyqtSignal(int, str) 
    update_table_signal = pyqtSignal(int, int)
    change_table_signal = pyqtSignal()
    
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        
    @pyqtSlot()    
    def write_aprom_online(self):
        try:
            self.ui.APROM_file = []
            self.ui.read_APROM_file()
            lenAPROM = self.ui.APROM_size
            start_addr = 0x0
            bsel = self.ui.board_select()
            bext = self.ui.board_ext_select()
                
            page_size = 2048
            pcount = math.ceil(lenAPROM / page_size) 
            
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.ui.lib.Get_Boot(pointer(self.ui.io_handle_t), bsel, bext, byref(Num), byref(Num_ext))
            
            print("--- Try to Erase APROM ---")   
            self.ui.lib.Erase_APROM(pointer(self.ui.io_handle_t), bsel, bext, pcount, start_addr)
            time.sleep(1)
            print("--- Erase APROM Command Done ---")

            print("--- Try to Write APROM ---")
            self.ui.APROM_file_ctypes = (ctypes.c_ubyte * lenAPROM)(*self.ui.APROM_file)
            array_pointer = ctypes.pointer(self.ui.APROM_file_ctypes)
            #b_second = time.time()
            i = 0
            c_state = True
            self.update_progress_signal.emit(0, "Writing")
            while i < lenAPROM:
                if not self.ui.check_connect_board():
                    c_state = False
                    break
                buffer = ctypes.cast(ctypes.addressof(array_pointer.contents) + i, POINTER(c_ubyte))
                dcount = min(pack_size - 12, lenAPROM - i)
                ret = self.ui.lib.Write_APROM(byref(self.ui.io_handle_t), bsel, bext, dcount, start_addr + i, buffer)
                i += dcount
                #print("Write_APROM: " + str(i) + " written.")
                self.update_progress_signal.emit(int(i * 100 / lenAPROM), "Writing")

            #f_second = time.time()
            if not c_state:
                self.update_progress_signal.emit(0, "Writing")
                print("--- Write APROM Interrupted ---")
                self.finished.emit()
                return
                
            print("--- Write APROM Done ---")
            #print("Write APROM: " + str(f_second - b_second) + " seconds cost.")
            
            print("--- Try to Verify APROM ---")
            self.ui.verify = [True, True, True, True, True]
            self.update_progress_signal.emit(0, "Verifying")
            i = 0
            c_state = True
            b_second = time.time()
            if not self.ui.check_connect_board():
                c_state = False
                
            NumID = c_ubyte(0)
            NumID_ext = c_ubyte(0)    

            ret = self.ui.lib.Verify_APROM_Checksum(byref(self.ui.io_handle_t), bsel, bext, self.ui.APROM_crc32_Checksum)
            
            if not c_state:
                self.update_progress_signal.emit(0, "Writing")
                print("--- Verify APROM Interrupted ---")
                self.finished.emit()
                return
                
            self.ui.verify_file(ret)
            print("--- Verify APROM Done ---")
            f_second = time.time()
            print("Verify APROM: " + str(f_second - b_second) + " seconds cost.")
            
            vstr = "Idle"
            if (bext & 0x1):
                vstr = "Success" if self.ui.verify[4] == True else "Fail"
            print("Verify SLOT " + str(0) + ": " + vstr)
            
            for p in range(0, 4): 
                vstr = "Idle"
                if (bsel & (0x1 << p)):
                    vstr = "Success" if self.ui.verify[p] == True else "Fail"
                print("Verify SLOT " + str(p + 1) + ": " + vstr)               
            
            self.finished.emit()            

        except Exception as e:
            print(f"An exception occurred: {e}")
            
            
    @pyqtSlot()    
    def write_aprom_offline(self):
        try:
            self.ui.APROM_file = []
            self.ui.read_APROM_file()
            self.ui.read_SPD_file()
            lenAPROM = self.ui.APROM_size
            file_size_bytes = lenAPROM.to_bytes(4, byteorder='little', signed=False)
            file_size_list = list(file_size_bytes)
            file_crc32_bytes = self.ui.APROM_crc32_Checksum.to_bytes(4, byteorder='little', signed=False)
            file_crc32_list = list(file_crc32_bytes)
            self.ui.APROM_file = file_size_list + file_crc32_list + self.ui.APROM_file
            start_addr = 0x27000
            if self.ui.config[1] != 0xFFFFFFFF and self.ui.config[1] != 0x0:
                start_addr = self.ui.config[1]
            
            print("--- Try to Write Offline APROM ---")
            self.ui.APROM_file_ctypes = (ctypes.c_ubyte * (lenAPROM + 8))(*self.ui.APROM_file)
            array_pointer = ctypes.pointer(self.ui.APROM_file_ctypes)
            
            self.ui.lib.ISP_Erase_DataFlash(byref(self.ui.io_handle_t))
            
            time.sleep(1)
            
            c_state = True
            j = 0
            while j < 0x400:
                if not self.ui.check_connect_board():
                    c_state = False
                    break
                dcount = min(pack_size - 12, 1024 - j)
                data = (c_ubyte * dcount)()
                for c_index, value in enumerate(self.ui.spd_table_f_value[j:j+dcount]):
                    data[c_index] = value
                
                ret = self.ui.lib.ISP_Update_DataFlash(byref(self.ui.io_handle_t), dcount, start_addr + j, byref(data))
                j += dcount
                
            if not c_state:
                print("--- Write Offline APROM Interrupted ---")
                self.finished.emit()
                return
    
            start_addr = start_addr + 0x400
            i = 0
            self.update_progress_signal.emit(0, "Writing")
            while i < lenAPROM + 8:
                if not self.ui.check_connect_board():
                    c_state = False
                    break
                buffer = ctypes.cast(ctypes.addressof(array_pointer.contents) + i, POINTER(c_ubyte))
                dcount = min(pack_size - 12, lenAPROM - i + 8)
                ret = self.ui.lib.ISP_Update_DataFlash(byref(self.ui.io_handle_t), dcount, start_addr + i, buffer)
                i += dcount
                self.update_progress_signal.emit(int(i * 100 / lenAPROM), "Writing")

            if not c_state:
                self.update_progress_signal.emit(0, "Writing")
                print("--- Write Offline APROM Interrupted ---")
                self.finished.emit()
                return
                
            print("--- Write Offline APROM Done ---")
            self.finished.emit()

        except Exception as e:
            print(f"An exception occurred: {e}")
            
    @pyqtSlot()    
    def read_spd_offline(self): 
        try:
            start_addr = 0x27000
            if self.ui.config[1] != 0xFFFFFFFF and self.ui.config[1] != 0x0:
                start_addr = self.ui.config[1]
            
            j = 0
            while j < 0x400:
                data = (c_ubyte * 32)()
                dcount = min(32, 1024 - j)
                ret = self.ui.lib.ISP_Read_DataFlash(byref(self.ui.io_handle_t), dcount, start_addr + j, byref(data))
                if ret:
                    for k in range(0, dcount):
                        value = data[k]
                        self.update_table_signal.emit(j + k, data[k])
                j += dcount
                
            print("--- Read Offline SPD Done ---")
            self.change_table_signal.emit()
            self.finished.emit()
                
        except Exception as e:
            print(f"An exception occurred: {e}")
            
    @pyqtSlot()
    def read_spd(self):
        try:
            bsel = int(self.ui.board_select_solo() & 0xF) 
            bext = 1 if (self.ui.board_select_solo() == 0x10) else 0
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.ui.lib.Get_Boot(pointer(self.ui.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
            rv_s = self.ui.reverse_single(bsel) if (bext == 0) else 4
            if ((boot >> (8 * rv_s)) & 0xFF) == 0x0:
                print(f"--- Read SPD Start ---")
                for h in range(0, 8):
                    for i in range(0, 4):
                        data = (c_ubyte * 32)()
                        self.ui.lib.Read_Info32(pointer(self.ui.io_handle_t), bsel, bext, h, i, byref(data), byref(Num), byref(Num_ext))
                        
                        index = h * 128 + i * 32
                        for j in range(0, 32):
                            self.update_table_signal.emit(index + j, data[j])

                print("--- Read SPD Finish ---")
                self.change_table_signal.emit()
                
            self.finished.emit()

        except Exception as e:
            print(f"An exception occurred: {e}")
            
    @pyqtSlot()
    def write_spd_from_file(self):
        try:
            bsel = self.ui.board_select()
            bext = self.ui.board_ext_select()
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.ui.lib.Get_Boot(pointer(self.ui.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
            self.ui.spd_table_f_value = [0xFF] * 1024
            self.ui.read_SPD_file()
            
            print("--- Write SPD Start ---")
            for h in range(0, 8):
                for i in range(0, 4):
                    index = h * 128 + i * 32
                    data = (c_ubyte * 32)()
                    for c_index, value in enumerate(self.ui.spd_table_f_value[index:index+32]):
                        data[c_index] = value
                    self.ui.lib.Write_Info32(pointer(self.ui.io_handle_t), bsel, bext, h, i, byref(data), byref(Num), byref(Num_ext))
                if (Num.value != bsel):
                    for ri in range(0, 4):
                        if bsel & (0x1 << ri) != 0 and Num.value & (0x1 << ri) == 0:
                            print(f'slot {ri + 1} page {h} is blocked by write protect')
                if (Num_ext.value != bext):
                    if bext != 0 and Num_ext.value == 0:
                        print(f'slot {0} page {h} is blocked by write protect')
            
            print("--- Write SPD Finish ---")
                    
            self.finished.emit()

        except Exception as e:
            print(f"An exception occurred: {e}")
            
class HexDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        # Define a regular expression that matches a 2-digit hex value with "0x" prefix
        regex = QRegExp("^0x[0-9A-Fa-f]{2}$")
        validator = QRegExpValidator(regex, editor)
        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.EditRole)
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)
        
class Main_Ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self) # Call the inherited classes __init__ method

        self.setupUi(self)
        self.s_state = 0
        self.a_state = 0
        
        if APP_MODE:
            image_path = os.path.join(sys._MEIPASS, 'Nuvoton.png')
        else:
            image_path = './image/Nuvoton.png'
            
        self.pixmap = QPixmap(image_path)
        self.label_nuvoton.setPixmap(self.pixmap)
        self.label_nuvoton.setMaximumSize(QSize(1200, 40))
        
        self.setWindowTitle("Nuvoton NuDIMM_Gang v1." + version_number)
        
        self.outputStream = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stdout = self.outputStream
        
        self.conf = ConfigParser()

        self.connect_flag = False

        self.io_handle_t = io_handle_t()
        self.io_handle_t.dev_open = False;
        self.io_handle_t.bResendFlag = False;
        self.io_handle_t.m_uCmdIndex = 1;
        self.io_handle_t.m_usCheckSum = 0;
        self.io_handle_t.ac_buffer = (c_ubyte*(pack_size + 1))()

        self.DEV_IO = DEV_IO()
        
        #USB Version
        self.USB_dev_io = USB_dev_io()
        
        if os.name == 'nt':  # Windows
            self.lib = ctypes.cdll.LoadLibrary('./Gang_USB_Lib.dll')
            #self.lib = ctypes.cdll.LoadLibrary('./ISPLib.dll') 
        
        self.m_ulDeviceID = 0x0
        self.chip_type = 0x0
        self.memory_size = 0
        self.aprom_size = 0
        self.nvm_size = 0
        self.page_size = 0
        self.config = (c_uint * 2)(0xFFFFFFFF,0xFFFFFFFF)
        
        self.update_disconnected_status()
        
        self.read_count = 0
        self.verify = [True, True, True, True, True]
        self.spd_table_value = [0xFF] * 1024
        self.spd_table_w_value = [0xFF] * 1024
        self.spd_table_f_value = [0xFF] * 1024
        
        self.btn_connect.clicked.connect(self.Ui_open)
        self.btn_slot.clicked.connect(lambda: self.Ui_version()) 
        
        self.checkBox_slot_all.clicked.connect(self.check_all)
        
        self.radioButton_slot_1.clicked.connect(lambda: self.radio_spd())
        self.radioButton_slot_2.clicked.connect(lambda: self.radio_spd())
        self.radioButton_slot_3.clicked.connect(lambda: self.radio_spd())
        self.radioButton_slot_4.clicked.connect(lambda: self.radio_spd())
        self.radioButton_slot_0.clicked.connect(lambda: self.radio_spd())
        self.radioButton_slot_all.setVisible(False)
        
        self.radioButton_offline.clicked.connect(self.offline_select)
        self.radioButton_online.clicked.connect(self.offline_select)
        
        self.btn_ap.clicked.connect(self.iniBrowseAPROM)
        self.btn_spd.clicked.connect(self.iniBrowseSPD)
        self.btn_program.clicked.connect(self.Write_Choice)
        
        self.pushButton_read.setVisible(False)
        self.pushButton_read_board.clicked.connect(self.ReadSPD_board)
        self.pushButton_setting.clicked.connect(self.show_Config)
        self.radioButton_page_1.clicked.connect(self.change_spd_table)
        self.radioButton_page_2.clicked.connect(self.change_spd_table)
        
        self.Table_spd_2.itemClicked.connect(self.item_info)
        self.Table_spd_2.itemChanged.connect(self.set_spd_table)
        
        self.actionSave_Setting.triggered.connect(self.Save_Setting)
        self.actionLoad_Setting.triggered.connect(self.Load_Setting)
        self.actionExport_SPD_file.triggered.connect(self.Export_SPD_Information)
        self.actionImport_SPD_file.triggered.connect(self.Import_SPD_Information)
        
        self.actionSPD_Information_Setting.triggered.connect(self.Ui_Config_Simple)
        self.actionSerial_Checker.triggered.connect(self.show_checker)
        
        self.actionVersion.triggered.connect(self.showVersion)
        self.actionUser_Manual.triggered.connect(self.showUM)
        
        delegate = HexDelegate(self.Table_spd_2)
        self.Table_spd_2.setItemDelegate(delegate)
        
        for i in range(0, 512):
            row, column  = divmod(i, 16)
            item = QtWidgets.QTableWidgetItem('0xFF')
            self.Table_spd_2.setItem(row, column, item)
            
        self.Table_spd_2.horizontalHeader().setDefaultSectionSize(48)
        
        self.worker = None
        
        self.lib.Get_Boot.restype = c_ulonglong
        self.lib.Get_Version.restype = c_ulonglong
        self.lib.Read_Reg.restype = c_ulonglong
        self.lib.Verify_APROM_Checksum.restype = c_ulonglong
        
    def DEV_IO_setting(self):
        self.DEV_IO.init = VOIDFUNCTYPE(self.USB_dev_io.USB_init)
        self.DEV_IO.open = UINTFUNCTYPE(self.USB_dev_io.USB_open)
        self.DEV_IO.close = VOIDFUNCTYPE(self.USB_dev_io.USB_close)
        self.DEV_IO.read = RWFUNCTYPE(self.USB_dev_io.USB_read)
        self.DEV_IO.write = RWFUNCTYPE(self.USB_dev_io.USB_write)
        
        self.io_handle_t.m_dev_io = self.DEV_IO
        
    def Ui_open(self):
        self.DEV_IO_setting()
        
        self.lib.ISP_Open.argtypes = [POINTER(io_handle_t)]
        self.lib.ISP_Open.restype = c_uint
        
        self.text_browser.clear()
        
        if not self.connect_flag:
            if self.lib.ISP_Open(byref(self.io_handle_t)):
                self.connect_flag = True 
                self.attempt_connection()
            else:
                print("Connect to DDR5 Control Board Fail")
                self.connect_flag = False
                self.update_disconnected_status()
        else:
            self.connect_flag = False
            self.update_disconnected_status()
            
    def attempt_connection(self):
        for attempt in range(1, 11):
            self.io_handle_t.m_uCmdIndex = 1
            if self.lib.ISP_Connect(byref(self.io_handle_t), 40):
                self.m_ucFW_VER = self.lib.ISP_GetVersion(byref(self.io_handle_t))
                print("Get Control Board Firmware Version")
                self.m_ulDeviceID = self.lib.ISP_GetDeviceID(byref(self.io_handle_t))
                print("Get Control Board Nuvoton UID")
                self.lib.ISP_Read_Config(byref(self.io_handle_t), (self.config))
                self.update_flash()
                print("Get Control Board Nuvoton Config")
                self.label_connect.setText('Status: <font color="green">Connected<font>')
                self.btn_connect.setText("Disconnect")
                return
            print(f"--- Try to Connect to Control Board --- Try Count: {attempt} ---")
        
        print("Connect to DDR5 Control Board Fail")
        self.lib.ISP_Close(byref(self.io_handle_t))
        self.connect_flag = False
    
    def update_disconnected_status(self):
        self.lib.ISP_Close.argtypes = [POINTER(io_handle_t)]
        self.lib.ISP_Close.restype = None
        
        self.lib.ISP_Close(byref(self.io_handle_t))
        self.label_connect.setText('Status: <font color="red">Disconnected<font>')
        
        self.btn_connect.setText("Connect")
        self.update_slot_state(0, 0)
        self.a_state = 0
        self.s_state = 0
        label_t = ["Customer ID: ", "Chip ID: ", "LED ID: ", "Project ID: ", "FT ID: "]
        for i in range(0, 5):
            getattr(self, f'label_slot_{i}').setText(f"Not Connected")
            getattr(self, f'label_slot_{i}_rom').setText(f"Boot Status: None")
            getattr(self, f'label_slot_{i}_fw').setText(f"FW Version: NAN")
            getattr(self, f'Slot_{i}_2').setStyleSheet(".QFrame { border: 2px solid gray; }")
            getattr(self, f'label_slot_{i}').setStyleSheet("color: gray;")
            getattr(self, f'label_slot_{i}_rom').setStyleSheet("color: gray;")
            getattr(self, f'label_slot_{i}_fw').setStyleSheet("color: gray;")
            for j in range(0, 5):    
                label_slot_info = self.__dict__[f'label_slot_{i}_info_{j+1}']
                label_slot_info.setText(label_t[j] + "NAN")
                label_slot_info.setStyleSheet("color: gray;")
    
    def check_all(self):
        if self.checkBox_slot_all.isChecked():
            self.checkBox_slot_1.setChecked(False)
            self.checkBox_slot_2.setChecked(False)
            self.checkBox_slot_3.setChecked(False) 
            self.checkBox_slot_4.setChecked(False)
            self.checkBox_slot_0.setChecked(False)
            self.checkBox_slot_1.setEnabled(False)
            self.checkBox_slot_2.setEnabled(False)
            self.checkBox_slot_3.setEnabled(False) 
            self.checkBox_slot_4.setEnabled(False)
            self.checkBox_slot_0.setEnabled(False)
        else:
            self.checkBox_slot_1.setEnabled(True)
            self.checkBox_slot_2.setEnabled(True)
            self.checkBox_slot_3.setEnabled(True) 
            self.checkBox_slot_4.setEnabled(True)
            self.checkBox_slot_0.setEnabled(True)
    
    def update_slot_state(self, asel, bsel):
        self.checkBox_slot_1.setChecked(bsel & 0x1 and bsel != 0x1F)
        self.checkBox_slot_2.setChecked(bsel & 0x2 and bsel != 0x1F)
        self.checkBox_slot_3.setChecked(bsel & 0x4 and bsel != 0x1F) 
        self.checkBox_slot_4.setChecked(bsel & 0x8 and bsel != 0x1F)
        self.checkBox_slot_0.setChecked(bsel & 0x10 and bsel != 0x1F) 
        self.checkBox_slot_all.setChecked(bsel == 0x1F) 
        self.checkBox_slot_1.setEnabled(asel & 0x1)
        self.checkBox_slot_2.setEnabled(asel & 0x2)
        self.checkBox_slot_3.setEnabled(asel & 0x4) 
        self.checkBox_slot_4.setEnabled(asel & 0x8)
        self.checkBox_slot_0.setEnabled(asel & 0x10)
        self.checkBox_slot_all.setEnabled(asel == 0x1F) 
        self.radioButton_slot_1.setEnabled(asel & 0x1)
        self.radioButton_slot_2.setEnabled(asel & 0x2)
        self.radioButton_slot_3.setEnabled(asel & 0x4)
        self.radioButton_slot_4.setEnabled(asel & 0x8)
        self.radioButton_slot_0.setEnabled(asel & 0x10)
                 
    def update_flash(self):
        chip_name, chip_type, aprom_size, nvm_size, nvm_addr, page_size = GetStaticInfo(self, self.m_ulDeviceID, self.config)
        self.chip_type = chip_type
        self.memory_size = aprom_size + nvm_size
        self.page_size = page_size
        self.aprom_size = aprom_size
        self.nvm_size = nvm_size
        
    def board_select(self):
        bsel = 0
        if self.checkBox_slot_1.isChecked():
            bsel += 0x1
        if self.checkBox_slot_2.isChecked():
            bsel += 0x2
        if self.checkBox_slot_3.isChecked():
            bsel += 0x4
        if self.checkBox_slot_4.isChecked():
            bsel += 0x8  

        if self.checkBox_slot_all.isChecked():
            bsel = 0xF
        
        self.s_state = (self.s_state & ~(0xF)) | bsel
        return bsel
        
    def board_ext_select(self):
        bext = 0
        if self.checkBox_slot_0.isChecked():
            bext = 0x1

        if self.checkBox_slot_all.isChecked():
            bext = 0x1
        
        self.s_state = (self.s_state & ~(0x10)) | (bext << 4)
        return bext
        
    def board_select_solo(self):
        bsel = 0
        if self.radioButton_slot_1.isChecked():
            bsel = 0x1
        elif self.radioButton_slot_2.isChecked():
            bsel = 0x2
        elif self.radioButton_slot_3.isChecked():
            bsel = 0x4
        elif self.radioButton_slot_4.isChecked():
            bsel = 0x8
        elif self.radioButton_slot_0.isChecked():
            bsel = 0x10
        return bsel
        
    def reverse_single(self, bsel):
        if bsel == 8:
            return 3
        elif bsel == 4:
            return 2
        elif bsel == 2:
            return 1
        elif bsel == 1:
            return 0
        
    def reverse_board_select(self, bsel):
        self.checkBox_slot_1.setChecked(bsel & 0x1 and bsel != 0x1F)
        self.checkBox_slot_2.setChecked(bsel & 0x2 and bsel != 0x1F)
        self.checkBox_slot_3.setChecked(bsel & 0x4 and bsel != 0x1F) 
        self.checkBox_slot_4.setChecked(bsel & 0x8 and bsel != 0x1F) 
        self.checkBox_slot_0.setChecked(bsel & 0x10 and bsel != 0x1F) 
        self.checkBox_slot_all.setChecked(bsel == 0x1F)    
        return 
        
    def Ui_erase(self):
        self.text_browser.clear()
        if (self.connect_flag == True):
            bsel = self.board_select()
            bext = self.board_ext_select()
            if (bsel == 0 and bext == 0):
                reply = QMessageBox.warning(None, 'Warning', 'Please select SLOT!')
                return 
            if not self.check_connect_slot(bsel, bext):
                reply = QMessageBox.warning(None, 'Warning', 'Please check selected SLOT is connected!')
                return
            pcount = int(self.lineEdit_erase.text())
            addrstr = self.lineEdit_address.text()
            if addrstr.startswith("0x"):
                addrstr = addrstr[2:]
            start_addr = int(addrstr, 16)
            print("--- Try to Erase APROM ---")   
            self.lib.Erase_APROM(pointer(self.io_handle_t), bsel, bext, pcount, start_addr)
            print("--- Erase APROM Command Send ---")
            reply = QMessageBox.warning(None, 'Progress', 'Erase APROM send.')
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def Write_Offline(self):
        self.text_browser.clear()
        if self.check_connect_board():
        
            if self.lineEdit_ap.text() == "" or not self.lineEdit_ap.text():
                reply = QMessageBox.warning(None, 'Warning', 'Please select APROM file!')
                return
                
            if self.lineEdit_spd.text() == "" or not self.lineEdit_spd.text():
                reply = QMessageBox.warning(None, 'Warning', 'Please select SPD file!')
                return
                
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.write_aprom_offline)
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')  

    def offline_select(self):
        t = not self.radioButton_offline.isChecked()
        self.checkBox_ap.setEnabled(t)
        self.checkBox_spd.setEnabled(t)
    
    def Write_Choice(self):
        self.text_browser.clear() 
        b_second = time.time()
        if self.check_connect_board(): 
            f_second = time.time()
            bsel = self.board_select()
            bext = self.board_ext_select()
            if bsel == 0 and bext == 0 and self.radioButton_online.isChecked():
                reply = QMessageBox.warning(None, 'Warning', 'Please select SLOT!')
                return
            if self.radioButton_online.isChecked():
                if self.checkBox_ap.isChecked() and self.checkBox_spd.isChecked():
                    if self.lineEdit_ap.text() == "" or not self.lineEdit_ap.text():
                        reply = QMessageBox.warning(None, 'Warning', 'Please select APROM file!')
                        return
                    if self.lineEdit_spd.text() == "" or not self.lineEdit_spd.text():
                        reply = QMessageBox.warning(None, 'Warning', 'Please select SPD file!')
                        return
                    if self.Ui_jump_ld():
                        self.Write_Online_All()
                elif self.checkBox_ap.isChecked():
                    if self.lineEdit_ap.text() == "" or not self.lineEdit_ap.text():
                        reply = QMessageBox.warning(None, 'Warning', 'Please select APROM file!')
                        return
                    if self.Ui_jump_ld():
                        self.Write_Online()
                elif self.checkBox_spd.isChecked():
                    if self.lineEdit_spd.text() == "" or not self.lineEdit_spd.text():
                        reply = QMessageBox.warning(None, 'Warning', 'Please select SPD file!')
                        return
                    self.Ui_jump_ap()
                    self.WriteSPD() 
                
            elif self.radioButton_offline.isChecked():
                self.Write_Offline()
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def Write_Online(self):
        self.text_browser.clear()
        if self.check_connect_board():    
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.write_aprom_online, next_worker_function = 'j')
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def Write_Online_All(self):
        self.text_browser.clear()
        if self.check_connect_board():  
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.write_aprom_online, next_worker_function = 'w')
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def ReadSPD_board(self):
        self.text_browser.clear()
        if self.check_connect_board():
               
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.read_spd_offline)
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')    
            
    def ReadSPD(self):
        self.text_browser.clear()
        if self.check_connect_board():
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.read_spd)
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def WriteSPD(self):
        self.text_browser.clear()
        if self.check_connect_board():
            bsel = self.board_select()      
            self.worker = Worker(self)
            self.setup_worker_thread(self.worker.write_spd_from_file, end = True)
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            
    def setup_worker_thread(self, worker_function, next_worker_function = None, end = None):
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(worker_function)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.update_progress_signal.connect(self.update_progress)
        self.worker.update_table_signal.connect(self.update_table)
        self.worker.change_table_signal.connect(self.change_spd_table)
        self.worker.error.connect(self.handle_error)
        self.worker.destroyed.connect(self.on_worker_deleted)
        
        self.set_all_button(False)
        self.worker.finished.connect(lambda: self.set_all_button(True))
        
        if next_worker_function == 'w':
            self.worker.finished.connect(self.jump_aprom_and_write_spd)
        elif next_worker_function == 'j':
            self.worker.finished.connect(self.jump_aprom)
    
        if end == True: 
            self.worker.finished.connect(self.Online_End)
            
        # Start the thread
        self.thread.start()
        
    def Online_End(self):
        reply = QMessageBox.warning(None, 'Warning', 'Online Programming Finish!')
        
    def jump_aprom_and_write_spd(self):
        if self.check_connect_board():
            bsel = self.board_select()
            bext = self.board_ext_select()
            boot_select = 0                
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext))
            print("--- Try to Jump Code ---")
            self.lib.Jump_Code(pointer(self.io_handle_t), bsel, bext, boot_select)
            print("--- Jump Code Send ---")   
            time.sleep(0.1)
            
            self.worker = Worker(self)   
            self.setup_worker_thread(self.worker.write_spd_from_file, end = True)  

    def jump_aprom(self):
        if self.check_connect_board():
            bsel = self.board_select()
            bext = self.board_ext_select()
            boot_select = 0                
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext))
            print("--- Try to Jump Code ---")   
            self.lib.Jump_Code(pointer(self.io_handle_t), bsel, bext, boot_select)
            print("--- Jump Code Send ---") 
            self.Online_End()
            
    def lock_radio(self):
        self.radioButton_slot_1.setEnabled(False)
        self.radioButton_slot_2.setEnabled(False)
        self.radioButton_slot_3.setEnabled(False)
        self.radioButton_slot_4.setEnabled(False)
        self.radioButton_slot_0.setEnabled(False)    
        
    def radio_spd(self):
        if self.check_connect_board(): 
            self.lock_radio()
            self.ReadSPD()
    
    def Ui_version(self):
        self.text_browser.clear()
        if self.check_connect_board():
            bsel = 0xF
            bext = 0x1
            slot_sum = 0
            Num2 = c_ubyte(0)
            Num2_ext = c_ubyte(0) 
            boot = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num2), byref(Num2_ext)) & 0xFFFFFFFFFF
            #print(hex(boot), Num2.value, Num2_ext.value)
            ID = 0xFF
            NumID = c_ubyte(0)
            NumID_ext = c_ubyte(0)
            label_t = ["Customer ID: ", "Chip ID: ", "LED ID: ", "Project ID: ", "FT ID: "]
            for i in range(1, 6): 
                if (i != 5):
                    vsel = 0x1 << (i - 1)
                    vext = 0
                else:
                    vsel = 0
                    vext = 1
                frame_slot = self.__dict__[f'Slot_{i%5}_2']
                label_slot = self.__dict__[f'label_slot_{i%5}']
                label_rom = self.__dict__[f'label_slot_{i%5}_rom']
                label_fw = self.__dict__[f'label_slot_{i%5}_fw']
                if ((Num2.value & bsel) and (bsel & vsel)) or ((Num2_ext.value & bext) and (bext & vext)):
                    b_text = "NANROM"
                    if (((boot >> (8 * (i - 1))) & 0xFF) == 0x1): 
                        b_text = "LDROM"
                        slot_sum += 0x1 << (i - 1)
                    elif (((boot >> (8 * (i - 1))) & 0xFF) == 0x0):
                        b_text = "APROM"
                        slot_sum += 0x1 << (i - 1)
                    
                    if (b_text == "LDROM"):
                        Num = c_ubyte(0)
                        Num_ext = c_ubyte(0)
                        version = self.lib.Get_Version(pointer(self.io_handle_t), vsel, vext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
                        v_num = ((version >> (8 * (i - 1))) & 0xFF)
                        v_text = hex(v_num)
                        frame_slot.setStyleSheet(".QFrame { border: 2px solid red; }")
                        label_slot.setText("Connected") 
                        label_slot.setStyleSheet("color: black;")
                        label_rom.setText("Boot: LDROM") 
                        label_rom.setStyleSheet("color: black;")
                        label_fw.setText("FW Version: " + v_text) 
                        label_fw.setStyleSheet("color: black;")
                        for j in range(0, 5):
                            label_slot_info = self.__dict__[f'label_slot_{i%5}_info_{j+1}']
                            label_slot_info.setText(label_t[j] + "NAN")
                            label_slot_info.setStyleSheet("color: gray;")
                    elif (b_text == "APROM"):
                        frame_slot.setStyleSheet(".QFrame { border: 2px solid red; }")
                        label_slot.setText("Connected")
                        label_slot.setStyleSheet("color: black;")
                        label_rom.setText("Boot: APROM")
                        label_rom.setStyleSheet("color: black;")
                        
                        FW = self.lib.Read_Reg(pointer(self.io_handle_t), vsel, vext, 2, byref(NumID), byref(NumID_ext)) & 0xFFFFFFFFFF
                        #print(hex(FW))
                        if (NumID.value & vsel) or (NumID_ext.value & vext):
                            label_fw.setText("FW Version: " + hex((FW >> (8 * (i - 1)))& 0xFF))
                            label_fw.setStyleSheet("color: black;")
                        else:
                            label_fw.setText("FW Version: NAN")
                            label_fw.setStyleSheet("color: gray;")
                            
                        for j in range(0, 5):    
                            ID = self.lib.Read_Reg(pointer(self.io_handle_t), vsel, vext, j + 21, byref(NumID), byref(NumID_ext)) & 0xFFFFFFFFFF
                            #print(hex(ID))
                            label_slot_info = self.__dict__[f'label_slot_{i%5}_info_{j+1}']
                            if (NumID.value & vsel) or (NumID_ext.value & vext):
                                label_slot_info.setText(label_t[j] + hex((ID >> (8 * (i - 1)))& 0xFF))
                                label_slot_info.setStyleSheet("color: black;")
                            else:
                                label_slot_info.setText(label_t[j] + "NAN")
                                label_slot_info.setStyleSheet("color: gray;")
                    else:
                        frame_slot.setStyleSheet(".QFrame { border: 2px solid gray; }")
                        label_slot.setText("Not Connected")
                        label_slot.setStyleSheet("color: gray;")
                        label_rom.setText("Boot: None")
                        label_rom.setStyleSheet("color: gray;")
                        label_fw.setText("FW Version: NAN")
                        label_fw.setStyleSheet("color: gray;")
                        for j in range(0, 5):    
                            label_slot_info = self.__dict__[f'label_slot_{i%5}_info_{j+1}']
                            label_slot_info.setText(label_t[j] + "NAN")
                elif (bsel & vsel) or (bext & vext):
                    frame_slot.setStyleSheet(".QFrame { border: 2px solid gray; }")
                    label_slot.setText("Not Connected")
                    label_slot.setStyleSheet("color: gray;")
                    label_rom.setText("Boot: None")
                    label_rom.setStyleSheet("color: gray;")
                    label_fw.setText("FW Version: NAN")
                    label_fw.setStyleSheet("color: gray;")
                    for j in range(0, 5):    
                        label_slot_info = self.__dict__[f'label_slot_{i%5}_info_{j+1}']
                        label_slot_info.setText(label_t[j] + "NAN")
                        label_slot_info.setStyleSheet("color: gray;")
                else:
                    continue
            
            self.a_state = slot_sum    
            self.update_slot_state(self.a_state, 0)
            print("--- Get SLOT information Finish ---")
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
        
    def Ui_jump_ap(self):
        self.text_browser.clear()
        if self.check_connect_board():
            bsel = self.board_select()
            bext = self.board_ext_select()
            if (bsel == 0 and bext == 0):
                reply = QMessageBox.warning(None, 'Warning', 'Please select SLOT!')
                return
            if not self.check_connect_slot(bsel, bext):
                reply = QMessageBox.warning(None, 'Warning', 'Please check selected SLOT is connected!')
                return
            boot_select = 0x0
                
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
            print("--- Try to Jump Code ---")   
            self.lib.Jump_Code(pointer(self.io_handle_t), bsel, bext, boot_select)
            print("--- Jump Code Send ---")  
            
            time.sleep(0.1)
            if not self.check_connect_boot(bsel, bext, 0x0):
                reply = QMessageBox.warning(None, 'Warning', 'NuDIMM-Gang ISP is only open for Nuvoton DIMM')
                return False
            return True
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            return False
            
    def Ui_jump_ld(self):
        self.text_browser.clear()
        if self.check_connect_board():
            bsel = self.board_select()
            bext = self.board_ext_select()
            if (bsel == 0 and bext == 0):
                reply = QMessageBox.warning(None, 'Warning', 'Please select SLOT!')
                return
            if not self.check_connect_slot(bsel, bext):
                reply = QMessageBox.warning(None, 'Warning', 'Please check selected SLOT is connected!')
                return
            boot_select = 0x1
            
            Num = c_ubyte(0)
            Num_ext = c_ubyte(0)
            boot = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
            print("--- Try to Jump Code ---") 
            self.lib.Jump_Code(pointer(self.io_handle_t), bsel, bext, boot_select)
            print("--- Jump Code Send ---")   
            
            time.sleep(0.25)
            if not self.check_connect_boot(bsel, bext, 0x1):
                reply = QMessageBox.warning(None, 'Warning', 'NuDIMM-Gang ISP is only open for Nuvoton DIMM')
                return False
            return True
        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            return False
        
    def iniBrowseAPROM(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter = "bin(*.bin)")
        if filename != "":
            self.lineEdit_ap.setText(filename)
            self.APROM_file = []
            self.read_APROM_file()
        else:
            self.label_file_size.setText("APROM File Size: 00000000 Bytes")
            self.label_file_checksum.setText("APROM File Checksum: 0xFFFF")
            
    def iniBrowseSPD(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter = "spd(*.spd)")
        if filename != "":
            self.lineEdit_spd.setText(filename)
            self.spd_table_f_value = [0xFF] * 1024
            self.read_SPD_file()   
                
    def iniBrowseSaveRead(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter = "bin(*.bin)")
        if filename != "":
            self.lineEdit_rd.setText(filename)
            self.read_file = []
            
    def read_SPD_file(self):
        filename = self.lineEdit_spd.text()
        try:
            file_size = os.path.getsize(filename)
            with open(filename, 'r') as f:  # Open file in read text mode
                content = f.read()
            # Split the content by lines, then split each line by spaces and filter out empty strings
            hex_values = [val for line in content.split('\n') for val in line.strip().split(' ') if val]
            # Convert the hex values back to integers and store them in spd_table_f_value
            self.spd_table_f_value = [int(val, 16) for val in hex_values]
        except Exception as e:
            self.spd_table_f_value = [0xFF] * 1024
        
    def read_APROM_file(self):
        filename = self.lineEdit_ap.text()
        try:
            f = open(filename, 'rb')            
            self.APROM_Checksum = 0
            self.APROM_crc32_Checksum = 0
            while True:
                x=f.read(1)
                if not x:
                    break
                temp=struct.unpack('B',x) 
                self.APROM_file.append(temp[0])
                self.APROM_Checksum=self.APROM_Checksum + temp[0]
            f.close()
            self.APROM_Checksum = self.APROM_Checksum & 0xFFFF
            self.APROM_size = len(self.APROM_file)
            import zlib
            f = open(filename, 'rb') 
            while True:
                s = f.read(65536)
                if not s:
                    break
                self.APROM_crc32_Checksum = zlib.crc32(s)
            f.close()
            self.APROM_crc32_Checksum = self.APROM_crc32_Checksum & 0xFFFFFFFF 
            self.label_file_size.setText("APROM File Size: " + str(self.APROM_size) + " Bytes")
            self.label_file_checksum.setText("APROM File Checksum: " + hex(self.APROM_Checksum))
        except Exception as e:
            print(f"An error occurred: {e}")
            print("APROM can not read or not exist!")
            self.APROM_size = 0
            self.APROM_Checksum = 0x0000
            self.APROM_crc32_Checksum = 0x00000000
            self.label_file_size.setText("APROM File Size: " + str(self.APROM_size) + " Bytes")
            self.label_file_checksum.setText("APROM File Checksum: " + hex(self.APROM_Checksum))  
        
    def show_Config(self):
        self.config_window_2 = Dialog_Ui_2(self.spd_table_w_value)
        self.config_window_2.show()
        
    def Ui_Config_Simple(self):
        self.config_window = Dialog_Ui_3(self.spd_table_w_value)
        self.config_window.setModal(True)
        self.config_window.data_updated.connect(self.update_main_data)
        self.config_window.show()
        
    def show_checker(self):
        self.checker_window = Dialog_Ui_4()
        self.checker_window.show()
        
    def update_main_data(self, config):
        self.spd_table_w_value = config
        self.change_spd_table()
        
    def verify_file(self, ret):
        for i in range(0, 5): 
            if (((ret >> (8 * i)) & 0xFF) == 0x1): 
                self.verify[i] = False
                
    def normalOutputWritten(self, text):
        self.text_browser.insertPlainText(text)
        self.text_browser.moveCursor(QTextCursor.End)
        
    def Save_Setting(self):
        filename = ""
        # Fix for crash in X on Ubuntu 14.04
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter = "config(*.cfg)")
        if (filename != "" and filename != None):
            self.conf.read(filename, encoding='utf-8')
            if not self.conf.has_section('File'):
                self.conf.add_section('File')
            self.conf.set('File', 'APROM File', self.lineEdit_ap.text())
            self.conf.set('File', 'SPD File', self.lineEdit_spd.text())
            
            if not self.conf.has_section('Setting'):
                self.conf.add_section('Setting')
            self.conf.set('Setting', 'SLOT', str(self.board_select()))
        
            self.conf.write(open(filename, 'w', encoding='utf-8'))
            
    def Load_Setting(self):
        filename = ""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter = "config(*.cfg)")
        if (filename != "" and filename != None):
            #print(filename)
            self.conf.read(filename, encoding='utf-8')
            self.lineEdit_ap.setText(self.conf.get('File', 'APROM File', fallback=''))
            self.lineEdit_spd.setText(self.conf.get('File', 'SPD File', fallback=''))
            if self.lineEdit_ap.text():
                self.APROM_file = []
                self.read_APROM_file()
            
            self.reverse_board_select(int(self.conf.get('Setting', 'SLOT', fallback='')))
                
    def Export_SPD_Information(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="spd(*.spd)")
        if filename:
            try:
                formatted_data = ""
                
                for i in range(0, len(self.spd_table_w_value), 16):
                    line = ' '.join(f"{val:02X}" for val in self.spd_table_w_value[i:i+16])
                    formatted_data += f" {line} \n"
                
                with open(filename, 'w') as f:  # Open file in write mode
                    f.write(formatted_data)
                    
            except Exception as e:
                QMessageBox.warning(None, 'Warning', f"An error occurred: {e}")
                print(f"An error occurred: {e}")
                
    def Import_SPD_Information(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter="spd(*.spd)")
        if filename:
            try:
                file_size = os.path.getsize(filename)
                
                with open(filename, 'r') as f:  # Open file in read text mode
                    content = f.read()
                    
                hex_values = [val for line in content.split('\n') for val in line.strip().split(' ') if val]

                self.spd_table_w_value = [int(val, 16) for val in hex_values]
                
                self.change_spd_table()
            except Exception as e:
                QMessageBox.warning(None, 'Warning', f"An error occurred: {e}")
                print(f"An error occurred: {e}")
            
    def update_progress(self, percent, text):
        self.label_progress_state.setText("Progress: " + text)
        self.progressBar.setValue(percent)
        
    def update_table(self, index, value):
        self.spd_table_value[index] = value & 0xFF
        self.spd_table_w_value[index] = value & 0xFF
        
    def item_info(self, item):
        index = 0 if self.radioButton_page_1.isChecked() else 1
        byte_index = index * 512 + item.row() * 16 + item.column()
        self.label_read_byte.setText("Byte 0x{:03X}".format(byte_index) + f" ({byte_index})")
    
    def set_spd_table(self, item):
        index = 0 if self.radioButton_page_1.isChecked() else 1
        intValue = int(item.text(), 16)
        byte_index = index * 512 + item.row() * 16 + item.column()
        self.spd_table_w_value[byte_index] = intValue & 0xFF
        if self.spd_table_w_value[byte_index] != self.spd_table_value[byte_index]:
            item.setForeground(QBrush(QColor('red')))
        else:
            item.setForeground(QBrush(QColor('black')))
        
    def change_spd_table(self):
        index = 0 if self.radioButton_page_1.isChecked() else 1
        for i in range(0, 512):
            value = f'0x{self.spd_table_w_value[index * 512 + i]:02X}'
            row, column  = divmod(i, 16)
            item = QtWidgets.QTableWidgetItem(value)
            self.Table_spd_2.setItem(row, column, item)
    
    def check_connect_board(self):
        self.connect_flag = self.lib.ISP_Connect(byref(self.io_handle_t), 40)
        return self.connect_flag
        
    def check_connect_slot(self, bsel, bext):
        Num = c_ubyte(0)
        Num_ext = c_ubyte(0)
        rst = True
        boot_res = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
        
        for i in range(0, 5):
            if (Num.value & (0x1 << i)) and (bsel & (0x1 << i)):
                b_num = (boot_res >> (8 * (i)) & 0xFF)
                if (b_num != 0x0 and b_num != 0x01):
                    rst = False
            elif (bsel & (0x1 << i)):
                rst = False
        
        return rst
        
    def check_connect_boot(self, bsel, bext, boot):
        # 0x1 : LDROM  0x0 : APROM
        Num = c_ubyte(0)
        Num_ext = c_ubyte(0)
        rst = True
        boot_res = self.lib.Get_Boot(pointer(self.io_handle_t), bsel, bext, byref(Num), byref(Num_ext)) & 0xFFFFFFFFFF
        
        for i in range(0, 4):
            if (Num.value & (0x1 << i)) and (bsel & (0x1 << i)):
                b_num = (boot_res >> (8 * (i)) & 0xFF)
                if (b_num != boot):
                    rst = False
            elif (bsel & (0x1 << i)):
                rst = False
        if (Num_ext.value & 0x1) and (bext & 0x1):
            b_num = (boot_res >> (8 * (4)) & 0xFF)
            if (b_num != boot):
                rst = False
        elif (bext & 0x1):
            rst = False
            
        return rst
        
    def set_all_button(self, state):
        self.btn_connect.setEnabled(state)
        self.btn_program.setEnabled(state)
        self.btn_slot.setEnabled(state)
        self.btn_ap.setEnabled(state)
        self.btn_spd.setEnabled(state)
        self.pushButton_read.setEnabled(state)
        self.pushButton_setting.setEnabled(state)
        self.pushButton_read_board.setEnabled(state)
        self.radioButton_online.setEnabled(state)
        self.radioButton_offline.setEnabled(state)
        
        if (state == True):
            self.update_slot_state(self.a_state, self.s_state)
            self.offline_select()
        else:
            self.checkBox_slot_1.setEnabled(False)
            self.checkBox_slot_2.setEnabled(False)
            self.checkBox_slot_3.setEnabled(False) 
            self.checkBox_slot_4.setEnabled(False)
            self.checkBox_slot_0.setEnabled(False)
            self.checkBox_slot_all.setEnabled(False) 
            self.radioButton_slot_1.setEnabled(False)
            self.radioButton_slot_2.setEnabled(False)
            self.radioButton_slot_3.setEnabled(False)
            self.radioButton_slot_4.setEnabled(False)
            self.radioButton_slot_0.setEnabled(False)
            self.checkBox_ap.setEnabled(False)
            self.checkBox_spd.setEnabled(False)
            
    def on_worker_deleted(self):
        self.worker = None   
        
    def handle_error(self, message):
        QMessageBox.warning(None, 'Error', message)
        self.set_all_button(True)
        
    def showVersion(self):
        reply = QtWidgets.QMessageBox.information(None ,'Version',' NuDIMM_Gang Version: 1.' + version_number + '\n')
    
    def showUM(self):         
        manual_path = os.path.join(".", "UM_NuDIMM-Gang.pdf")
        open_new(manual_path)
        
        self.text_browser.clear()
        if self.check_connect_board():
            bsel = self.board_select()
            bext = self.board_ext_select()
            if (bsel == 0 and bext == 0):
                reply = QMessageBox.warning(None, 'Warning', 'Please select SLOT!')
                return
            if not self.check_connect_slot(bsel, bext):
                reply = QMessageBox.warning(None, 'Warning', 'Please check selected SLOT is connected!')
                return
                
            NumID = c_ubyte(0)
            NumID_ext = c_ubyte(0)    
            self.lib.Write_Reg(pointer(self.io_handle_t), bsel, bext, 8, 76, byref(NumID), byref(NumID_ext))
            self.lib.Write_Reg(pointer(self.io_handle_t), bsel, bext, 8, 85, byref(NumID), byref(NumID_ext))
            time.sleep(5)
            
            self.Ui_jump_ld()
            time.sleep(0.1)
            if not self.check_connect_boot(bsel, bext, 0x0):
                reply = QMessageBox.warning(None, 'Warning', 'NuDIMM-Gang ISP is only open for Nuvoton DIMM')
                return False

        else:
            reply = QMessageBox.warning(None, 'Warning', 'Control Board Not Connect!')
            return False
            
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    import iconQrc
    if getattr(sys, 'frozen', False):
        APP_MODE = True
        icon_path = os.path.join(sys._MEIPASS, 'NuTool.ico')
    else:
        APP_MODE = False
        icon_path = './image/NuTool.ico'
    app.setWindowIcon(QIcon(icon_path))
    myapp = Main_Ui()
    myapp.show()
    sys.exit(app.exec_())