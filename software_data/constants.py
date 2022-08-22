from PyQt5 import QtGui, QtWidgets

NUM_TOPIC_ROWS=2
NUM_TOPIC_COLUMNS=2

BASIC_FONT_LARGE = QtGui.QFont('Arial', 28)
BASIC_FONT_MID = QtGui.QFont('Arial', 18)
BASIC_FONT_SMALL = QtGui.QFont('Arial', 12)

THRESHOLD_SCREEN_WIDTH = 1280

BACKGROUND_COLOR = "rgb(62, 110, 145)"
BACKGROUND_COLOR_DARK = "rgb(52, 100, 135)"
BACKGROUND_WHITE = "rgb(230,230,230)"
BACKGROUND_ORANGE = "rgb(255,165,0)"
BACKGROUND_YELLOW = "rgb(255,255,0)"
BACKGROUND_GREY = "rgb(100,100,100)"
BACKGROUND_RED = "rgb(255,0,0)"
BACKGROUND_DARK_GREY = "rgb(50,50,50)"
BACKGROUND_LGREEN = "rgb(0,200,0)"
BACKGROUND_BLACK = "rgb(0,0,0)"
FONT_COLOR_LIGHT = "rgb(230, 230, 230)"
FONT_COLOR_DARK = "rgb(80, 80, 80)"

INTERFACE_BUTTON_UNSELECTED = f"color: rgb(230,230,230);background-color:{BACKGROUND_COLOR_DARK};\nborder-radius: 30px;"
ITEMS_STYLE = f"color: rgb(230,230,230);background-color:{BACKGROUND_COLOR}; padding-left: 20px; border: 5px solid {BACKGROUND_COLOR_DARK};\nborder-radius: 30px;"
INTERFACE_BUTTON_SELECTED = f"background-color:rgb(200,50,100); padding-left: 20px; border: 5px solid rgb(0, 0, 0);\nborder-radius: 30px;"

BORDER_STYLESHEET_THIN = f'border: 2px solid  {BACKGROUND_COLOR_DARK}; border-radius: 10px'
BORDER_STYLESHEET_NONE = f'{BACKGROUND_COLOR_DARK}; border-radius: 0px'
KEYBOARD={
        "de":["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","Ä","Ö","Ü","ß",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".",":", "(", ")","{","}"],
        "en":["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".",":", "(", ")","{","}"]
    }

KEYBOARD_KEYS={
        "de":{
            "clear":"Löschen",
            "space":"Leerzeichen",
            "back":"Zurück",
            "enter":"Enter",
            "done":"Fertig"
        },
        "en":{
            "clear":"Clear",
            "space":"Space",
            "back":"Back",
            "enter":"Enter",
            "done":"Done"
        }
    }

def _set_size_policy(version):
    if version == 0:
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
    elif version == 1:
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
    elif version == 2:
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)

    return size_policy

SIZE_POLICY = _set_size_policy(version=0)
SIZE_POLICY_H = _set_size_policy(version=1)
SIZE_POLICY_PREF = _set_size_policy(version=2)