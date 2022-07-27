from logging import root
from PyQt5 import QtWidgets, QtCore, QtGui
from serial.tools.list_ports import comports as list_comports

import sys, math


class SystemSelection(QtWidgets.QDialog):
    """
    This "window" is a QWidget. If it has no parent.
    """
    BASIC_FONT = QtGui.QFont('Arial', 28)

    def __init__(self, systems, root_dir, cur_selected_sytem, parent=None):
        super().__init__(parent)
        QBtn = QtWidgets.QDialogButtonBox.Ok
        self.parent = parent
        self.ROOT_DIR = root_dir
        self.Selected_System = cur_selected_sytem
        self.New_Selected_System = self.Selected_System.copy()
        self.comports = [comport.device for comport in list_comports()]
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.resize(600,400)
        self._set_Ui(systems)

        

    def _set_Ui(self, systems):
        self.layout = QtWidgets.QVBoxLayout()
        self.system_buttons = []
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        for system in systems.keys():
            if system == "arduino":
                continue
            button = QtWidgets.QRadioButton(systems[system]["name"])
            button.setFont(self.BASIC_FONT)
            button.setSizePolicy(sizePolicy)
            button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/{system}.png"))
            button.setIconSize(QtCore.QSize(50,50))
            button.toggled.connect(lambda do_it, arg=systems[system]["system_id"] :self._set_selected_system(arg))
            self.system_buttons.append(button)
            self.layout.addWidget(button)

        self._set_old_selected()
        comports_label = QtWidgets.QLabel("COM Ports")
        comports_label.setFont(self.BASIC_FONT)
        self.layout.addWidget(comports_label)
        self.comports_list_widget = QtWidgets.QListWidget()
        self.comports_list_widget.setStyleSheet(f"background-color:rgb(230,230,230)")
        self.comports_list_widget.setFont(self.BASIC_FONT)
        self.comports_list_widget.addItems(self.comports)
        self.comports_list_widget.clicked.connect(self._comport_selected)
        self.layout.addWidget(self.comports_list_widget)
        self.setLayout(self.layout)
        self.layout.addWidget(self.buttonBox)

    def _set_old_selected(self):
        self.system_buttons[self.Selected_System["system_id"]].setChecked(True)

    def _set_selected_system(self, new_system):
        self.New_Selected_System["system_id"]=new_system

    def _comport_selected(self, qmodelindex):
        self.New_Selected_System["comport"]=self.comports_list_widget.currentItem().text()
