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
        self.system_buttons = []
        

        
        self.layout.addWidget(self.buttonBox,0,0,1,2)



