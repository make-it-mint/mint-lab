from logging import root
from PyQt5 import QtWidgets, QtCore
from CustomButtons import LanguageButton

import sys, math


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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        for idx, language in enumerate(languages.keys()):
            row = math.floor(idx/num_cols)
            col = int(idx%num_cols)
            button = LanguageButton(parent=self)
            button.setSizePolicy(sizePolicy)
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