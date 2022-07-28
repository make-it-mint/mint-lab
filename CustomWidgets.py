import os, json
from PyQt5 import QtCore, QtGui, QtWidgets
from serial.tools.list_ports import comports as list_comports
import math
from constants import *



class OverViewButton(QtWidgets.QToolButton):

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, screen_size, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)
        
        self.icon_button = QtWidgets.QToolButton()
        self.icon_button.setAutoRaise(True)
        self.icon_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setStyleSheet(f"background-color:rgb(255,255,255); margin:10px; border-radius:10px")

        if screen_size.width() <= 1024:
            font = BASIC_FONT_SMALL
            self.icon_button.setIconSize(QtCore.QSize(int(screen_size.width()*.25), int(screen_size.height()*.30)))
        else:
            font = BASIC_FONT_MID
            self.icon_button.setIconSize(QtCore.QSize(int(screen_size.width()*.20), int(screen_size.height()*.20)))

        self.text =QtWidgets.QLabel("")
        self.text.setFont(font)

        self.text.setStyleSheet("")
        self.text.setWordWrap(True)
        self.icon_button.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_button,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)

        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)

    def setButtonIcon(self, image_path=None):
        if image_path and os.path.exists(image_path):
            self.icon_button.setIcon(QtGui.QIcon(image_path))
        else:
            image_path = QtGui.QPixmap(f"{TopicButton.ROOT_DIR}/assets/system/default_invisible.png")
            self.icon_button.setIcon(QtGui.QIcon(image_path))

    def setButtonText(self, text=""):
        self.text.setText(text)

    def setActive(self, is_active:bool):
        if is_active:
            self.setStyleSheet(f"background-color:rgb(255,255,255); margin:10px; border-radius:10px")
            self.text.setStyleSheet("color:rgb(0,0,0)")
            self.icon_button.setStyleSheet("")
        else:
            self.setStyleSheet(f"")


class TopicButton(QtWidgets.QToolButton):

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, screen_size, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)
        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)
        if screen_size.width() <= 1024:
            font = BASIC_FONT_MID
        else:
            font = BASIC_FONT_MID

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"margin:10px; border-radius:10px")

        self.text =QtWidgets.QLabel()
        self.text.setFont(font)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text.setStyleSheet("color: rgb(230,230,230)")
        self.icon_label.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_label,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)
        self.screen_size = screen_size
        


    def setButtonIcon(self, image_path=None):
        if image_path and os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            self.icon_label.setPixmap(pixmap.scaled(int(self.screen_size.width()*.25), int(self.screen_size.height()*.25), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        else:
            pixmap = QtGui.QPixmap(f"{TopicButton.ROOT_DIR}/assets/system/default_invisible.png")
            self.icon_label.setPixmap(pixmap.scaled(int(self.screen_size.width()*.25), int(self.screen_size.height()*.25), QtCore.Qt.AspectRatioMode.KeepAspectRatio))



    def setButtonText(self, text=""):
        self.text.setText(text)

    def setActive(self, is_active:bool):
        if is_active:
            self.setStyleSheet("background-color:rgb(52, 100, 135);border:5px solid rgb(52, 100, 135); margin:10px; border-radius:30px")
            self.text.setStyleSheet("color: rgb(230,230,230)")
            self.icon_label.setStyleSheet("background-color:rgb(62, 110, 145);border:0px;border-radius:30px")
        else:
            self.setStyleSheet(f"")


class LanguageButton(QtWidgets.QToolButton):

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)
        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"margin:10px; border-radius:10px")
        

        self.text =QtWidgets.QLabel()
        self.text.setFont(BASIC_FONT_SMALL)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text.setStyleSheet("")
        self.icon_label.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_label,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)
        self.setStyleSheet("border:2px solid rgb(125,178,255); margin:10px; border-radius:30px")
        self.text.setStyleSheet("color: rgb(230,230,230); border:0px")
        self.icon_label.setStyleSheet("border:0px")
        


    def setButtonIcon(self, image_path=None):
        pixmap = QtGui.QPixmap(image_path)  
        self.icon_label.setPixmap(pixmap.scaled(120, 100))


    def setButtonText(self, text=""):
        self.text.setText(text)


class ScrollLabel(QtWidgets.QScrollArea):


    def __init__(self, screen_size):
        QtWidgets.QScrollArea.__init__(self)

        self.setWidgetResizable(True)
        content = QtWidgets.QWidget(self)
        self.setStyleSheet("background-color: rgb(52, 100, 135); border-radius: 10px")
        self.setWidget(content)
        if screen_size.width() <= 1024:
            font = BASIC_FONT_SMALL
        else:
            font = BASIC_FONT_MID

        layout = QtWidgets.QVBoxLayout(content)

        self.label = QtWidgets.QLabel(content)
        self.label.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: rgb(230, 230, 230)")
        self.label.setFont(font)
        layout.addWidget(self.label)


    def setText(self, text):
        self.label.setText(text)




class LanguageSelection(QtWidgets.QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, languages, root_dir, cur_language, parent=None):
        super().__init__(parent)
        QBtn = QtWidgets.QDialogButtonBox.Ok
        self.ROOT_DIR = root_dir
        self.languages = languages
        self.Selected_Language = cur_language
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.resize(600,400)
        self._set_Ui(languages)

        

    def _set_Ui(self, languages):
        self.layout = QtWidgets.QGridLayout()
        num_cols = 3
        self._Language_Buttons = []

        for idx, language in enumerate(languages.keys()):
            row = math.floor(idx/num_cols)
            col = int(idx%num_cols)
            button = LanguageButton(parent=self)
            button.setSizePolicy(SIZE_POLICY)
            button.setButtonText(languages[language]["name"])
            button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/languages/{languages[language]['icon']}")
            button.clicked.connect(lambda do_it, arg=language :self._set_new_language(arg))
            self._Language_Buttons.append(button)
            self.layout.addWidget(button,row, col)

        self.setLayout(self.layout)
        self.selected_language_label = QtWidgets.QLabel(self)
        self.selected_language_label.setText(self.languages[self.Selected_Language]["name"])
        self.layout.addWidget(self.selected_language_label, math.ceil(len(languages)/3) + 1, 0)
        self.layout.addWidget(self.buttonBox, math.ceil(len(languages)/3) + 1, 1)


    def _set_new_language(self, new_language):
        self.Selected_Language=new_language
        self.selected_language_label.setText(self.languages[self.Selected_Language]["name"])



class SystemSelection(QtWidgets.QDialog):
    """
    This "window" is a QWidget. If it has no parent.
    """

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
        for system in systems.keys():
            if system == "arduino":
                continue
            button = QtWidgets.QRadioButton(systems[system]["name"])
            button.setFont(BASIC_FONT_LARGE)
            button.setSizePolicy(SIZE_POLICY)
            button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/{system}.png"))
            button.setIconSize(QtCore.QSize(50,50))
            button.toggled.connect(lambda do_it, arg=systems[system]["system_id"] :self._set_selected_system(arg))
            self.system_buttons.append(button)
            self.layout.addWidget(button)

        self._set_old_selected()
        comports_label = QtWidgets.QLabel("COM Ports")
        comports_label.setFont(BASIC_FONT_MID)
        self.layout.addWidget(comports_label)
        self.comports_list_widget = QtWidgets.QListWidget()
        self.comports_list_widget.setStyleSheet(f"background-color:rgb(230,230,230)")
        self.comports_list_widget.setFont(BASIC_FONT_MID)
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


