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

        
        self.setStyleSheet(
            """
            QFrame{
            border: 5px solid black;
            border-radius: 20px;
            }
            QLabel{
                border: 0px;
            }
            QToolButton{
                border-radius: 5px;
            }
            """)

        header =QLabel(experiment)
        header.setWordWrap(True)
        header.setFont(QFont("Helvetica", 32, QFont.Bold, italic=False))
        self.layout.addWidget(header,0,0,alignment=Qt.AlignCenter)

        button = QToolButton()
        image_path = f"{experiment_path}/logo.png"
        button.setIcon(QIcon(image_path))
        
        button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
        button.setIconSize(QSize(button.size().width(), button.size().height()-40))
        
        

        button.clicked.connect(self.start_experiment)
        self.layout.addWidget(button,1,0, alignment=Qt.AlignCenter)

        # desc =QLabel(description)
        # desc.setWordWrap(True)
        # desc.setFont(QFont("Helvetica", 22, QFont.Normal, italic=False))
        # self.layout.addWidget(desc,2,0,alignment=Qt.AlignCenter)
        

        self.layout.setColumnStretch(0,5)
        self.layout.setColumnStretch(1,1)
        self.layout.setRowStretch(0,0)
        self.layout.setRowStretch(1,0)
        self.layout.setRowStretch(2,1)


    def start_experiment(self):
        try:
            self.program_windows['experiment_list']['widget'].hide()
            self.program_windows['experiment']['widget'].show()
            spec = importlib.util.spec_from_file_location("module.name", f"{self._experiment_path}/experiment.py")
            experiment_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(experiment_module)
            experiment_module.Experiment(language = self._language, program_windows=self.program_windows)
        except Exception as e:
            #print(e)
            self.program_windows["experiment"]["widget"].hide()
            self.program_windows["experiment_list"]["widget"].show()
            QMessageBox.about(self,"Achtung","Keine Daten verfügbar")