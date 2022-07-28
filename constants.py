from PyQt5 import QtGui, QtWidgets

NUM_TOPIC_ROWS=2
NUM_TOPIC_COLUMNS=2

BASIC_FONT_LARGE = QtGui.QFont('Arial', 28)
BASIC_FONT_MID = QtGui.QFont('Arial', 18)
BASIC_FONT_SMALL = QtGui.QFont('Arial', 12)

BACKGROUND_COLOR = "rgb(62, 110, 145)"
BACKGROUND_WHITE = "rgb(230,230,230)"
BACKGROUND_GREY = "rgb(100,100,100)"
BACKGROUND_LGREEN = "rgb(0,200,0)"
BACKGROUND_BLACK = "rgb(0,0,0)"
FONT_COLOR_LIGHT = "rgb(230, 230, 230)"
FONT_COLOR_DARK = "rgb(80, 80, 80)"

INTERFACE_BUTTON_UNSELECTED = f"color: rgb(230,230,230);background-color:{BACKGROUND_COLOR}; padding-left: 20px; border: 5px solid rgb(52, 100, 135);\nborder-radius: 30px;"
INTERFACE_BUTTON_SELECTED = f"background-color:rgb(200,50,100); padding-left: 20px; border: 5px solid rgb(0, 0, 0);\nborder-radius: 30px;"



def _set_size_policy():
    size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    size_policy.setHorizontalStretch(1)
    size_policy.setVerticalStretch(1)
    return size_policy

SIZE_POLICY = _set_size_policy()