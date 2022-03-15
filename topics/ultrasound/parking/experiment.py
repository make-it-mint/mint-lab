from Experiment import ExperimentTemplate
import os
from PyQt6 import QtCore, QtGui, QtWidgets

class Experiment(ExperimentTemplate):

    def __init__(self, root_dir, language, screen_size, parent = None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size)
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(self.ROOT_DIR)

        self.show_fullscreen()
