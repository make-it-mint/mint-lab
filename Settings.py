import os, json, git
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
        self.available_languages= self.settings["languages"]
        self.selected_language = self.settings["selected_language"]
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.resize(600,400)
        self._set_Ui()

        

    def _set_Ui(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)


        self.keyboard_toggle = QtWidgets.QPushButton()
        self.keyboard_toggle.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/keyboard.png"))
        self.keyboard_toggle.setIconSize(QtCore.QSize(int(self.size().width()*.3), int(self.size().height()*.3)))
        self.keyboard_toggle.setSizePolicy(SIZE_POLICY)
        if self.settings["has_keyboard"]:
            self.has_keyboard = True
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_LGREEN}; padding:0 40px 0 40px;")
        else:
            self.has_keyboard = False
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_RED}; padding:0 40px 0 40px;")
        self.keyboard_toggle.clicked.connect(self.toggle_keyboard)
        self.layout.addWidget(self.keyboard_toggle,0,0)


        self.language_selection = QtWidgets.QPushButton()
        self.language_selection.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/languages/{self.available_languages[self.selected_language]['icon']}.png"))
        self.language_selection.setIconSize(QtCore.QSize(int(self.size().width()*.3), int(self.size().height()*.3)))
        self.language_selection.setSizePolicy(SIZE_POLICY)
        self.language_selection.clicked.connect(self.select_language)
        self.layout.addWidget(self.language_selection,0,1)

        self.bt_update_software = QtWidgets.QToolButton()
        self.bt_update_software.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.bt_update_software.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/update.png"))
        self.bt_update_software.setText("VERSION X.X.X")
        self.bt_update_software.setFont(BASIC_FONT_MID)
        self.bt_update_software.setIconSize(QtCore.QSize(int(self.size().width()*.3), int(self.size().height()*.3)))
        self.bt_update_software.setSizePolicy(SIZE_POLICY)
        self.bt_update_software.clicked.connect(self.update_software)
        self.layout.addWidget(self.bt_update_software,1,0)

        

        
        self.layout.addWidget(self.buttonBox,2,0,1,2)

        self.layout.setRowStretch(0,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)


    def toggle_keyboard(self):
        if self.has_keyboard:
            self.has_keyboard = False
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_RED};")
        else:
            self.has_keyboard = True
            self.keyboard_toggle.setStyleSheet(f"background-color: {BACKGROUND_LGREEN};")


    def select_language(self):
        languages = list(self.available_languages.keys())

        if languages.index(self.selected_language) >= len(self.available_languages)-1:
            self.selected_language = languages[0]
        else:
            self.selected_language = languages[languages.index(self.selected_language)+1]
        
        self.language_selection.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/languages/{self.available_languages[self.selected_language]['icon']}.png"))


    def update_software(self):
        print("Hello")




