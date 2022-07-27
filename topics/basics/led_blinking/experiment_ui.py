#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio.base_subprocess import ReadSubprocessPipeProto
from concurrent.futures import thread
from Experiment import ExperimentTemplate
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, json
import time
import multiprocessing
import subprocess
import json
import serial

class Experiment(ExperimentTemplate):

    def __init__(self, root_dir, language, screen_size, parent = None, selected_system=None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size, selected_system = selected_system)
        
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        experiment_content = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        
        self.experiment_is_running = False
        self.header.setText(experiment_content["experiment"][self.language]["name"])
        self.fill_experiment_material(materials=experiment_content["material"][self.language])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_content["setup"]["images"])
        self.fill_experiment_info(text=experiment_content["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_content["information"]["file"]))
        self.fill_experiment(content=experiment_content["experiment"])




    def close(self):
        if self.experiment_is_running:
            QtWidgets.QMessageBox.about(self.MainWidget,"Achtung","Experiment stoppen, bevor das Fenster geschlossen werden kann")
        else:
            self.MainWidget.close() 

    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        self.start_experiment_button = QtWidgets.QPushButton(self.sys_content["start_experiment"][self.language])
        self.start_experiment_button.setStyleSheet(f"color: {self.FONT_COLOR_DARK}; background-color: rgb(0,255,0); margin: 10px 20px 10px 20px; border-radius: 10px")
        self.start_experiment_button.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,1,1)

        


    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.experiment_is_running = True

            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment(selected_system=self.selected_system, dir = self.EXPERIMENT_DIR)
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)
            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            if self.selected_system["system_id"] == 0:
                self.running_experiment.experiment.stop()
            self.Experiment_Thread.exit()
   


    def update_ui(self, value_for_ui):
        try:
            value_pairs = value_for_ui.split(":")
            for pair in value_pairs:
                key, value = pair.split("=")
                if key == "counter":
                    self.start_experiment_button.setText(pair)
        except Exception as e:
            print(e)
        pass



class Running_Experiment(QtCore.QObject):
    value_for_ui = QtCore.pyqtSignal(str)
    experiment_is_running = True

    def __init__(self, selected_system, dir):
        super().__init__()
        self.selected_system = selected_system
        self.dir = dir
        

    def start_experiment(self):
        if self.selected_system["system_id"] == 0:
            from topics.basics.led_blinking.experiment_code.rpi import Experiment as rpi_experiment
            self.experiment = rpi_experiment(self.experiment_is_running, self.value_for_ui)
            self.experiment.run()        
                
        elif self.selected_system["system_id"] == 1:
            experiment = multiprocessing.Process(target=self.run_picopi)
            try:
                experiment.start()
                time.sleep(1)
                ser = serial.Serial(port=self.selected_system["comport"],baudrate=9600)
                ser.flushInput()
                while self.experiment_is_running:
                    self.value_for_ui.emit(ser.readline().decode("utf-8"))
                    time.sleep(.01)
                experiment.terminate()
                os.system(f'ampy --port {self.selected_system["comport"]} reset')
            except Exception or KeyboardInterrupt as e:
                print(e)
                experiment.terminate()
                os.system(f'ampy --port {self.selected_system["comport"]} reset')

    def run_picopi(self):
        os.system(f'ampy --port {self.selected_system["comport"]} run {self.dir[self.dir.rfind("mint-lab/")+9:]}/experiment_code/picopi.py')

        
        
            

        



