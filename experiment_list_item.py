#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 16:33:00 2021


@author: felix
"""

import sys
import os
import math
import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import importlib.util










class ExperimentOverview(QFrame):

    def __init__(self, experiment, description, experiment_path, language, windows):
        super().__init__()
        self.program_windows = windows
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self._experiment_path = experiment_path
        self._language = language

        self.layout.addWidget(QLabel(experiment),0,0)

        button = QToolButton()
        image_path = f"{experiment_path}/logo.png"
        button.setIcon(QIcon(image_path))
        
        button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
        button.setIconSize(QSize(button.size().width()-100, button.size().height()-40))
        button.setStyleSheet(
            f"""
            border-radius: 20px;
            """)

        button.clicked.connect(self.start_experiment)
        self.layout.addWidget(button,1,0)


        self.layout.addWidget(QLabel(description),2,0)

        button = QPushButton("Start Experiment")
        

        self.layout.setColumnStretch(0,5)
        self.layout.setColumnStretch(1,1)
        self.layout.setRowStretch(0,0)
        self.layout.setRowStretch(1,0)
        self.layout.setRowStretch(2,1)


    def start_experiment(self):
        self.program_windows['experiment_list']['widget'].hide()
        self.program_windows['experiment']['widget'].show()
        spec = importlib.util.spec_from_file_location("module.name", f"{self._experiment_path}/experiment.py")
        experiment_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(experiment_module)
        experiment_module.Experiment(language = self._language, program_windows=self.program_windows)