#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExperimentTemplate import UI_Template, Running_Experiment
from VirtualKeyboard import VKQLineEdit
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import os, json
import json
from software_data.constants import *


class Experiment(UI_Template):

    def __init__(self, root_dir, language, screen_size, parent = None, program_settings=None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size, program_settings = program_settings)
        
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.DEFAULT_VALUES={"FREQUENCY":2}#MUST use double quotation marks
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)

        self.set_experiment_header(experiment_name=experiment_information["experiment"][self.language]["name"], hyperlink=experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=experiment_information["information"][self.language], file_paths=[f"{self.EXPERIMENT_DIR}/assets/{item}" for item in experiment_information['information']['files'][self.language]])
        self.fill_experiment(content=experiment_information["experiment"])

    

    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        if not self.program_settings["has_keyboard"]:
            self.value_field = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.value_field = QtWidgets.QLineEdit()
        self.value_field.setMaxLength(10)
        self.value_field.setAlignment(QtCore.Qt.AlignCenter)
        self.value_field.setPlaceholderText(f'{self.EXPERIMENT_VALUES["FREQUENCY"]}')
        self.value_field.setValidator(QtGui.QIntValidator())
        self.experiment_layout.addWidget(self.value_field, 0, 0, QtCore.Qt.AlignLeft)

        self.start_experiment_button = QtWidgets.QToolButton()
        self.start_experiment_button.setAutoRaise(True)
        self.start_experiment_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.start_experiment_button.resize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2))
        self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/start_round.png"))
        self.start_experiment_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2)))
        self.start_experiment_button.setStyleSheet(f"border-radius: 1px")
        self.start_experiment_button.setSizePolicy(SIZE_POLICY_PREF)
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,1,1)

        
    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["FREQUENCY"] = self.value_field.text() if self.value_field.text() != "" else self.DEFAULT_VALUES["FREQUENCY"]
        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)


    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.write_values_to_experiment_file()
            self.experiment_is_running = True
            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment(experiment_button=self.start_experiment_button, selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)
            self.Experiment_Thread.start()
            self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/stop_round.png"))
            
        else:
            self.start_experiment_button.setEnabled(False)
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/start_round.png"))
            
            if self.selected_system["system_id"] == 0:
                self.running_experiment.experiment.stop()

            self.Experiment_Thread.exit()
            self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)
   


    def update_ui(self, value_for_ui):
        try:
            value_pairs = value_for_ui.split(":")
            for pair in value_pairs:
                key, value = pair.split("=")
                if key == "counter":
                    self.start_experiment_button.setText(value)
        except Exception as e:
            print(e)




        
        
            

        



