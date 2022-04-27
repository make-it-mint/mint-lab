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

        self.distance_visualization_frame = QtWidgets.QFrame()
        self.set_distance_visualization(parent_widget=self.distance_visualization_frame, content=content)
        self.experiment_layout.addWidget(self.distance_visualization_frame, 1, 0)

        self.car_distance_frame = QtWidgets.QFrame()
        self.set_car_distance_visualization(parent_widget=self.car_distance_frame, content=content)
        self.experiment_layout.addWidget(self.car_distance_frame, 2, 0)


        self.experiment_layout.setRowStretch(0,1)
        self.experiment_layout.setRowStretch(1,5)
        self.experiment_layout.setRowStretch(2,4)
        
             

    def set_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        #ROW 0 - Distances
        barrier_far_0 = QtWidgets.QLabel()
        barrier_far_0.setStyleSheet(
            """
            background-color: rgb(0,0,0);
            """)
        layout.addWidget(barrier_far_0, 0, 1)

        #ROW 1 - Progressbars
        self.distance_colour = QtWidgets.QLabel()
        self.distance_colour.setStyleSheet(
            """
            background-color: rgb(0,255,0);
            border-radius: 10px;
            margin-top: 40px;
            margin-bottom: 40px;
            """)
        layout.addWidget(self.distance_colour, 1, 0)

        barrier_far_1 = QtWidgets.QLabel()
        barrier_far_1.setStyleSheet(
                """
                background-color: rgb(0,0,0);
                """)
        layout.addWidget(barrier_far_1, 1, 1)

        self.progressbar_far = QtWidgets.QProgressBar()
        self.progressbar_far.setMinimum(0)
        self.progressbar_far.setMaximum(100)
        far_style = """
            QProgressBar{
                margin-top: 20px;
                margin-bottom: 20px;
            }

            QProgressBar::chunk {
                background-color: rgb(0,255,0);
            }"""
        self.progressbar_far.setStyleSheet(far_style)
        self.progressbar_far.setValue(50)
        self.progressbar_far.setTextVisible(False)
        self.progressbar_far.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )
        layout.addWidget(self.progressbar_far, 1, 2)
        #######################

        barrier_far_mid_1 = QtWidgets.QLabel()
        barrier_far_mid_1.setStyleSheet(
                """
                background-color: rgb(0,0,0);
                """)
        layout.addWidget(barrier_far_mid_1, 1, 3)

        self.progressbar_mid = QtWidgets.QProgressBar()
        self.progressbar_mid.setMinimum(0)
        self.progressbar_mid.setMaximum(100)
        mid_style = """
            QProgressBar{
                margin-top: 20px;
                margin-bottom: 20px;
            }

            QProgressBar::chunk {
                background-color: rgb(255,255,0);
                margin: 1px;
            }"""
        self.progressbar_mid.setStyleSheet(mid_style)
        self.progressbar_mid.setValue(50)
        self.progressbar_mid.setTextVisible(False)
        self.progressbar_mid.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )
        layout.addWidget(self.progressbar_mid, 1, 4)
        ##########################

        barrier_mid_near_1 = QtWidgets.QLabel()
        barrier_mid_near_1.setStyleSheet(
                """
                background-color: rgb(0,0,0);
                """)
        layout.addWidget(barrier_mid_near_1, 1, 5)

        self.progressbar_near = QtWidgets.QProgressBar()
        self.progressbar_near.setMinimum(0)
        self.progressbar_near.setMaximum(100)
        near_style = """
            QProgressBar{
                margin-top: 20px;
                margin-bottom: 20px;
            }

            QProgressBar::chunk {
                background-color: rgb(255,165,0);
            }"""
        self.progressbar_near.setStyleSheet(near_style)
        self.progressbar_near.setValue(50)
        self.progressbar_near.setTextVisible(False)
        self.progressbar_near.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )
        layout.addWidget(self.progressbar_near, 1, 6)
        #######################

        barrier_near_close_1 = QtWidgets.QLabel()
        barrier_near_close_1.setStyleSheet(
                """
                background-color: rgb(0,0,0);
                """)
        layout.addWidget(barrier_near_close_1, 1, 7)

        self.progressbar_close = QtWidgets.QProgressBar()
        self.progressbar_close.setMinimum(0)
        self.progressbar_close.setMaximum(100)
        close_style = """
            QProgressBar{
                margin-top: 20px;
                margin-bottom: 20px;
            }

            QProgressBar::chunk {
                background-color: rgb(255,0,0);
            }"""
        self.progressbar_close.setStyleSheet(close_style)
        self.progressbar_close.setValue(50)
        self.progressbar_close.setTextVisible(False)
        self.progressbar_close.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Preferred,
             )
        layout.addWidget(self.progressbar_close, 1, 8)
        #############################

        self.distance_stop = QtWidgets.QLabel()
        self.distance_stop.setStyleSheet(
            """
            background-color: rgb(255,0,0);
            border-radius: 10px;
            """)
        layout.addWidget(self.distance_stop, 1, 9)



        #ROW 2 - Beeping Frequencies

        #Layout Stretching
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,3)
        layout.setRowStretch(2,1)

        layout.setColumnStretch(0,4)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,30)
        layout.setColumnStretch(3,1)
        layout.setColumnStretch(4,26)
        layout.setColumnStretch(5,1)
        layout.setColumnStretch(6,22)
        layout.setColumnStretch(7,1)
        layout.setColumnStretch(8,18)
        layout.setColumnStretch(9,18)

    def set_car_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        layout = QtWidgets.QGridLayout()

    def start_stop_experiment(self):

        if not self.experiment_is_running:
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



