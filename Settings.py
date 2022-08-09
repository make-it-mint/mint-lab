from curses import COLOR_RED
import os, json
from PyQt5 import QtCore, QtGui, QtWidgets
from software_data.constants import *


class SettingsInterface(QtWidgets.QDialog):
    """
    This "window" is a QWidget. If it has no parent.
    """

    def __init__(self, root_dir, settings, parent=None):
        super().__init__(parent)
        QBtn = QtWidgets.QDialogButtonBox.Ok
        self.parent = parent
        self.ROOT_DIR = root_dir
        self.settings = settings
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.resize(600,400)
        self._set_Ui()

        

    def _set_Ui(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        

        self.keyboard_toggle = QtWidgets.QPushButton()
        self.keyboard_toggle.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/keyboard.png"))
        self.keyboard_toggle.setIconSize(QtCore.QSize(int(self.size().width()*.6), int(self.size().height()*.6)))
        self.keyboard_toggle.setSizePolicy(SIZE_POLICY)
        if self.settings["has_keyboard"]:
            self.has_keyboard = True
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_LGREEN}; padding:0 40px 0 40px;")
        else:
            self.has_keyboard = False
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_RED}; padding:0 40px 0 40px;")
        self.keyboard_toggle.clicked.connect(self.toggle_keyboard)
        self.layout.addWidget(self.keyboard_toggle,0,0)
        

        
        self.layout.addWidget(self.buttonBox,1,0,1,2)


    def toggle_keyboard(self):
        if self.has_keyboard:
            self.has_keyboard = False
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_RED}; padding:0 40px 0 40px;")
        else:
            self.has_keyboard = True
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_LGREEN}; padding:0 40px 0 40px;")




