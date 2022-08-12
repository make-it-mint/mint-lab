from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
import sys
from software_data.constants import *
import math
 
class VKQLineEdit(QLineEdit):
    def __init__(self, parent=None, name=None, mainWindowObj=None, validator=None):
        super(VKQLineEdit, self).__init__(parent)
        self.name = name
        self.mainWindowObj = mainWindowObj
        self.setFocusPolicy(Qt.ClickFocus)
        if validator == "int":
            self.setValidator(QIntValidator())

 
    def focusInEvent(self, e):
        self.mainWindowObj.keyboard.currentTextBox = self
        self.mainWindowObj.keyboard.text_box.setText(self.text())
        self.mainWindowObj.keyboard.show()
 
        super(VKQLineEdit, self).focusInEvent(e)
 
    def mousePressEvent(self, e):

        super(VKQLineEdit, self).mousePressEvent(e)


class VKQTextEdit(QTextEdit):
    def __init__(self, parent=None, name=None, mainWindowObj=None, validator=None):
        super(VKQTextEdit, self).__init__(parent)
        self.name = name
        self.mainWindowObj = mainWindowObj
        self.setFocusPolicy(Qt.ClickFocus)
        if validator == "int":
            self.setValidator(QIntValidator())

 
    def focusInEvent(self, e):
        self.mainWindowObj.keyboard.currentTextBox = self
        self.mainWindowObj.keyboard.text_box.setText(self.toPlainText())
        self.mainWindowObj.keyboard.show()
 
        super(VKQTextEdit, self).focusInEvent(e)
 
    def mousePressEvent(self, e):

        super(VKQTextEdit, self).mousePressEvent(e)
        
 
 
 
class Keyboard(QWidget):
    def __init__(self, screen_size, language, parent=None):
        super(Keyboard, self).__init__(parent)
        self.currentTextBox = None
        self.setStyleSheet(f"background-color:{BACKGROUND_DARK_GREY}; color:{FONT_COLOR_LIGHT}")
        self.screen_size = screen_size
        self.language = language
        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.buttonClicked)
 
        self.initUI()
 
    def initUI(self):
        layout = QGridLayout()
 

        self.setAutoFillBackground(True)
        self.text_box = QTextEdit()
        self.text_box.setFont(BASIC_FONT_LARGE)
        
        
 
        names = KEYBOARD[self.language]
        rows = 5 if self.screen_size.width()<1024 else 4
        cols = int(math.ceil(len(names)/rows))
        layout.addWidget(self.text_box, 0, 0, 1, cols)
 
        positions = [(i + 1, j) for i in range(rows) for j in range(cols)]
 
        for position, name in zip(positions, names):
 
            if name == '':
                continue
            button = QPushButton(name)
            button.setFont(BASIC_FONT_LARGE)
            button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
            button.setFixedHeight(80)
            button.setFixedWidth(90)
 
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            layout.addWidget(button, *position)
 
        # Cancel button
        # cancel_button = QPushButton('Cancel')
        # cancel_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        # cancel_button.setFont(BASIC_FONT_LARGE)
        # cancel_button.KEY_CHAR = Qt.Key_Cancel
        # layout.addWidget(cancel_button, 5, 0, 1, 2)
        # cancel_button.clicked.connect(self.signalMapper.map)
        # self.signalMapper.setMapping(cancel_button, cancel_button.KEY_CHAR)
        # #cancel_button.setFixedWidth(60)
 
        # Cancel button
        clear_button = QPushButton(KEYBOARD_KEYS[self.language]["clear"])
        clear_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        clear_button.setFont(BASIC_FONT_LARGE)
        clear_button.KEY_CHAR = Qt.Key_Clear
        layout.addWidget(clear_button, 5, 0, 1, 2)
        clear_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(clear_button, clear_button.KEY_CHAR)
        #clear_button.setFixedWidth(60)
 
        # Space button
        space_button = QPushButton(KEYBOARD_KEYS[self.language]["space"])
        space_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        space_button.setFont(BASIC_FONT_LARGE)
        space_button.KEY_CHAR = Qt.Key_Space
        layout.addWidget(space_button, 5, 2, 1, 3)
        space_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
        #space_button.setFixedWidth(85)
 
 
        # Back button
        back_button = QPushButton(KEYBOARD_KEYS[self.language]["back"])
        back_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        back_button.setFont(BASIC_FONT_LARGE)
        back_button.KEY_CHAR = Qt.Key_Backspace
        layout.addWidget(back_button, 5, 5, 1, 2)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        #back_button.setFixedWidth(60)
 
 
 
        # Enter button
        enter_button = QPushButton(KEYBOARD_KEYS[self.language]["enter"])
        enter_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        enter_button.setFont(BASIC_FONT_LARGE)
        enter_button.KEY_CHAR = Qt.Key_Enter
        layout.addWidget(enter_button, 5, 7, 1, 2)
        enter_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(enter_button, enter_button.KEY_CHAR)
        #enter_button.setFixedWidth(60)
 
        # Done button
        done_button = QPushButton(KEYBOARD_KEYS[self.language]["done"])
        done_button.setStyleSheet(f"color:{FONT_COLOR_LIGHT};")
        done_button.setFont(BASIC_FONT_LARGE)
        done_button.KEY_CHAR = Qt.Key_Home
        layout.addWidget(done_button, 5, 9, 1, 2)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        #done_button.setFixedWidth(60)
 
        self.setGeometry(int(self.screen_size.width()*.05), int(self.screen_size.height()*.2), int(self.screen_size.width()*.9), int(self.screen_size.height()*.7))
        self.setLayout(layout)
 
    def buttonClicked(self, char_ord):
 
        txt = self.text_box.toPlainText()
 
        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]
        elif char_ord == Qt.Key_Enter:
            txt += chr(10)
        elif char_ord == Qt.Key_Home:
            self.currentTextBox.setText(txt)
            self.text_box.setText("")
            self.hide()
            return
        elif char_ord == Qt.Key_Clear:
            txt = ""
        elif char_ord == Qt.Key_Space:
            txt += ' '
        else:
            txt += chr(char_ord)
 
        self.text_box.setText(txt)
 
 