import os, json
from PyQt5 import QtCore, QtGui, QtWidgets

class OverViewButton(QtWidgets.QToolButton):

    BASIC_FONT = QtGui.QFont('Arial', 18)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, screen_size, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)

        self.icon_button = QtWidgets.QToolButton()
        self.icon_button.setAutoRaise(True)
        self.icon_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setStyleSheet(f"background-color:rgb(255,255,255); margin:10px; border-radius:10px")
        self.icon_button.setIconSize(QtCore.QSize(int(screen_size.width()*.15), int(screen_size.height()*.20)))

        self.text =QtWidgets.QLabel("DUMMY")
        self.text.setFont(self.BASIC_FONT)

        self.text.setStyleSheet("")
        self.icon_button.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_button,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)

        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)


    def setButtonIcon(self, image_path=None):
        self.icon_button.setIcon(QtGui.QIcon(image_path))

    def setButtonText(self, text=""):
        self.text.setText(text)

    def setActive(self, is_active:bool):
        if is_active:
            self.setStyleSheet(f"background-color:rgb(255,255,255); margin:10px; border-radius:10px")
            self.text.setStyleSheet("")
            self.icon_button.setStyleSheet("")
        else:
            self.setStyleSheet(f"")


class TopicButton(QtWidgets.QToolButton):

    BASIC_FONT = QtGui.QFont('Arial', 18)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent_size, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)
        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"margin:10px; border-radius:10px")

        self.text =QtWidgets.QLabel("DUMMY")
        self.text.setFont(self.BASIC_FONT)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text.setStyleSheet("")
        self.icon_label.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_label,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)
        self.parent_size = parent_size
        


    def setButtonIcon(self, image_path=None):
        if image_path:
            pixmap = QtGui.QPixmap(image_path)  
            self.icon_label.setPixmap(pixmap.scaled(int(self.parent_size.width()*.75), int(self.parent_size.height()*.75), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        else:
            pixmap = QtGui.QPixmap(image_path)  
            self.icon_label.setPixmap(pixmap)


    def setButtonText(self, text=""):
        self.text.setText(text)

    def setActive(self, is_active:bool):
        if is_active:
            self.setStyleSheet("border:2px solid rgb(125,178,255); margin:10px; border-radius:30px")
            self.text.setStyleSheet("border:0px")
            self.icon_label.setStyleSheet("border:0px")
        else:
            self.setStyleSheet(f"")


class LanguageButton(QtWidgets.QToolButton):

    BASIC_FONT = QtGui.QFont('Arial', 18)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.MainLayout = QtWidgets.QGridLayout(self)
        self.MainLayout.setRowStretch(0, 5)
        self.MainLayout.setRowStretch(1, 1)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"margin:10px; border-radius:10px")
        

        self.text =QtWidgets.QLabel("DUMMY")
        self.text.setFont(self.BASIC_FONT)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text.setStyleSheet("")
        self.icon_label.setStyleSheet("")

        self.MainLayout.addWidget(self.icon_label,0,0,1,1)
        self.MainLayout.addWidget(self.text,1,0,1,1)
        self.setStyleSheet("border:2px solid rgb(125,178,255); margin:10px; border-radius:30px")
        self.text.setStyleSheet("border:0px")
        self.icon_label.setStyleSheet("border:0px")
        


    def setButtonIcon(self, image_path=None):
        pixmap = QtGui.QPixmap(image_path)  
        self.icon_label.setPixmap(pixmap.scaled(150, 100))


    def setButtonText(self, text=""):
        self.text.setText(text)


class ScrollLabel(QtWidgets.QScrollArea):

    BASIC_FONT = QtGui.QFont('Arial', 18)

    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)
        content = QtWidgets.QWidget(self)
        self.setStyleSheet("background-color: rgb(52, 100, 135); border-radius: 10px")
        self.setWidget(content)

        layout = QtWidgets.QVBoxLayout(content)

        self.label = QtWidgets.QLabel(content)
        self.label.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: rgb(230, 230, 230)")
        self.label.setFont(self.BASIC_FONT)
        layout.addWidget(self.label)


    def setText(self, text):
        self.label.setText(text)