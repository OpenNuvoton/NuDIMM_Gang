from PyQt5.QtWidgets import QSpinBox, QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class TwoDigitHexSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(TwoDigitHexSpinBox, self).__init__(parent)
        self.setRange(0, 255)  # Set the range to 0-255

    def textFromValue(self, value):
        # Format as hexadecimal with leading zeros
        return "0x{:02X}".format(value)

class VersionLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(VersionLineEdit, self).__init__(parent)
        # Set up a validator to ensure only hexadecimal values are entered
        hexRegExp = QRegExp("[0-9A-Fa-f]{1}\\.[0-9A-Fa-f]{1}")
        self.setValidator(QRegExpValidator(hexRegExp, self))
        self.setText("1.0")  # Default value
        
    def setValue(self, value_1, value_2):
        # Set the value as a hexadecimal string
        self.setText("{:01X}".format(value_1) + "." + "{:01X}".format(value_2))

    def value(self):
        # Return the current value as two integer
        hex_values = self.text().split('.')
        # Convert each hexadecimal value to an integer
        value_1 = 0
        value_2 = 0
        try:
            value_1 = int(hex_values[0], 16)
        except:
            value_1 = 0
        try:
            value_2 = int(hex_values[1], 16)
        except:
            value_2 = 0
            
        return value_1, value_2

class HexLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(HexLineEdit, self).__init__(parent)
        # Set up a validator to ensure only hexadecimal values are entered
        hexRegExp = QRegExp("0x[0-9A-Fa-f]{1,4}")
        self.setValidator(QRegExpValidator(hexRegExp, self))
        self.setText("0x0000")  # Default value

    def setValue(self, value):
        # Set the value as a hexadecimal string
        self.setText("0x{:04X}".format(value))

    def value(self):
        # Return the current value as an integer
        return int(self.text(), 16)

class EightDigitHexLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(EightDigitHexLineEdit, self).__init__(parent)
        # Set up a validator to ensure only hexadecimal values are entered
        hexRegExp = QRegExp("0x[0-9A-Fa-f]{1,8}")
        self.setValidator(QRegExpValidator(hexRegExp, self))
        self.setText("0x00000000")  # Default value

    def setValue(self, value):
        # Set the value as a hexadecimal string
        self.setText("0x{:08X}".format(value))

    def value(self):
        # Return the current value as an integer
        return int(self.text(), 16)
        
