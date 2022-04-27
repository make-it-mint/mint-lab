#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Experiment import ExperimentTemplate
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, json
import RPi.GPIO as GPIO
import time
import threading
import random

class Experiment(ExperimentTemplate):

    def __init__(self, root_dir, language, screen_size, parent = None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size)
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        experiment_content = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        
        self.experiment_is_running = False
        self.header.setText(experiment_content["experiment"][self.language]["name"])
        self.fill_experiment_material(materials=experiment_content["material"][self.language])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_content["setup"]["images"])
        self.fill_experiment_info(text=experiment_content["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_content["information"]["file"]))
        self.fill_experiment(content=experiment_content["experiment"])


        self.show_fullscreen()


    def close(self):
        if self.experiment_is_running:
            QtWidgets.QMessageBox.about(self.MainWidget,"Achtung","Experiment stoppen, bevor das Fenster geschlossen werden kann")
        else:
            self.MainWidget.close() 

    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
             

        


    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.experiment_is_running = True

            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment()
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.run)
            self.running_experiment.distance.connect(self.update_ui)
            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.exit()



   


    def update_ui(self):
        pass



class Running_Experiment(QtCore.QObject):
    value_for_ui = QtCore.pyqtSignal(float)

    def run(self):
        try:
            while True:
                self.value_for_ui.emit(self.my_experiment())
        except (Exception, KeyboardInterrupt) as e:
            self.cleanup_pins()

    def cleanup_pins(self):
        GPIO.cleanup()
        pass


    def my_experiment(self):

        value = random.randint(2,40)
        
        return value



