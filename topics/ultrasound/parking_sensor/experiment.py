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
        self.header.setStyleSheet(f"color: {self.FONT_COLOR_LIGHT}")
        self.fill_experiment_material(materials=experiment_content["material"][self.language])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_content["setup"]["images"])
        self.fill_experiment_info(text=experiment_content["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_content["information"]["file"]))
        self.fill_experiment(content=experiment_content["experiment"][self.language])


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
        self.experiment_layout.addWidget(self.distance_visualization_frame, 0, 0, 1, 2)

        self.distance_display = QtWidgets.QLabel(content["default_distance"])
        self.distance_display.setAlignment(QtCore.Qt.AlignCenter)
        self.distance_display.setFont(QtGui.QFont('Arial', 70))
        self.distance_display.setStyleSheet(f"color: {self.FONT_COLOR_LIGHT}")
        self.experiment_layout.addWidget(self.distance_display,1,0)

        self.start_experiment_button = QtWidgets.QPushButton("START EXPERIMENT")
        self.start_experiment_button.setFont(QtGui.QFont('Arial', 48))
        self.start_experiment_button.setStyleSheet(f"color: {self.FONT_COLOR_DARK}; background-color: rgb(0,255,0); margin: 50px 200px 50px 200px; border-radius: 50px")
        self.start_experiment_button.setCheckable(True)
        self.start_experiment_button.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding
             )
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,1,1)

        self.car_distance_frame = QtWidgets.QFrame()
        self.set_car_distance_visualization(parent_widget=self.car_distance_frame, content=content)
        self.experiment_layout.addWidget(self.car_distance_frame, 2, 0, 1, 2)

        
        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setColumnStretch(1,1) 
        self.experiment_layout.setRowStretch(0,3)
        self.experiment_layout.setRowStretch(1,3)
        self.experiment_layout.setRowStretch(2,4)
             

    def set_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        ###################
        #ROW 0 - Distances#
        ###################
        self.bound_far = QtWidgets.QLineEdit()
        self.bound_far.setMaxLength(10)
        self.bound_far.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_far.setFont(self.BASIC_FONT)
        self.bound_far.setPlaceholderText(f'{content["colour_legend"]["far"]}: 20 cm')
        self.bound_far.setStyleSheet("background-color: rgb(0,255,0); border-radius: 15px;")
        self.bound_far.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.bound_far, 0, 2, QtCore.Qt.AlignLeft)

        #################

        self.bound_far_mid = QtWidgets.QLineEdit()
        self.bound_far_mid.setMaxLength(10)
        self.bound_far_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_far_mid.setFont(self.BASIC_FONT)
        self.bound_far_mid.setPlaceholderText(f'{content["colour_legend"]["mid"]}: 14 cm')
        self.bound_far_mid.setStyleSheet("background-color: rgb(255,255,0); border-radius: 15px;")
        self.bound_far_mid.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.bound_far_mid, 0, 4, QtCore.Qt.AlignLeft)



        #################

        self.bound_mid_near = QtWidgets.QLineEdit()
        self.bound_mid_near.setMaxLength(10)
        self.bound_mid_near.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_mid_near.setFont(self.BASIC_FONT)
        self.bound_mid_near.setPlaceholderText(f'{content["colour_legend"]["near"]}: 8 cm')
        self.bound_mid_near.setStyleSheet("background-color: rgb(255,165,0); border-radius: 15px;")
        self.bound_mid_near.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.bound_mid_near, 0, 6, QtCore.Qt.AlignLeft)

        #################

        self.bound_near_close = QtWidgets.QLineEdit()
        self.bound_near_close.setMaxLength(10)
        self.bound_near_close.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_near_close.setFont(self.BASIC_FONT)
        self.bound_near_close.setPlaceholderText(f'{content["colour_legend"]["close"]}: 4 cm')
        self.bound_near_close.setStyleSheet("background-color: rgb(255,48,48); border-radius: 15px;")
        self.bound_near_close.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.bound_near_close, 0, 8, QtCore.Qt.AlignLeft)


        ######################
        #ROW 1 - Progressbar #
        ######################
        self.distance_colour = QtWidgets.QLabel()
        self.distance_colour.setStyleSheet(
            """
            background-color: rgb(0,255,0);
            border-radius: 10px;
            margin: 100px 10px 100px 10px;
            """)
        layout.addWidget(self.distance_colour, 1, 0)

        barrier_far_1 = QtWidgets.QLabel()
        barrier_far_1.setStyleSheet("background-color: rgb(0,0,0);")

        layout.addWidget(barrier_far_1, 1, 1)

        self.progressbar_distance = QtWidgets.QProgressBar()
        self.progressbar_distance.setMinimum(0)
        self.progressbar_distance.setMaximum(1000)
        self.progressbar_distance.setValue(0)
        self.progressbar_distance.setTextVisible(False)
        self.progressbar_distance.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred,
             )
        layout.addWidget(self.progressbar_distance, 1, 2,1,7)
        #############################
        barrier_final_1 = QtWidgets.QLabel()
        barrier_final_1.setStyleSheet("background-color: rgb(0,0,0);")
        layout.addWidget(barrier_final_1, 1, 9)

        self.distance_stop = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/go.png")
        self.distance_stop.setAlignment(QtCore.Qt.AlignCenter)
        self.distance_stop.setPixmap(pixmap.scaled(int(parent_widget.size().width()), int(parent_widget.size().height()*.7), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        # self.distance_stop.setStyleSheet(
        #     """
        #     background-color: rgb(255,0,0);
        #     border-radius: 10px;
        #     """)
        layout.addWidget(self.distance_stop, 1, 10)     


        #############################
        #ROW 2 - Beeping Frequencies#
        #############################

        self.beep_far = QtWidgets.QLineEdit()
        self.beep_far.setMaxLength(10)
        self.beep_far.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_far.setFont(self.BASIC_FONT)
        self.beep_far.setPlaceholderText(f'{content["colour_legend"]["far"]}: 0.5 Hz')
        self.beep_far.setStyleSheet("background-color: rgb(0,255,0); border-radius: 15px;")
        self.beep_far.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.beep_far, 2, 2, QtCore.Qt.AlignLeft)


        #################

        self.beep_far_mid = QtWidgets.QLineEdit()
        self.beep_far_mid.setMaxLength(10)
        self.beep_far_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_far_mid.setFont(self.BASIC_FONT)
        self.beep_far_mid.setPlaceholderText(f'{content["colour_legend"]["mid"]}: 1 Hz')
        self.beep_far_mid.setStyleSheet("background-color: rgb(255,255,0); border-radius: 15px;")
        self.beep_far_mid.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.beep_far_mid, 2, 4, QtCore.Qt.AlignLeft)

        #################


        self.beep_mid_near = QtWidgets.QLineEdit()
        self.beep_mid_near.setMaxLength(10)
        self.beep_mid_near.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_mid_near.setFont(self.BASIC_FONT)
        self.beep_mid_near.setPlaceholderText(f'{content["colour_legend"]["near"]}: 2 Hz')
        self.beep_mid_near.setStyleSheet("background-color: rgb(255,165,0); border-radius: 15px;")
        self.beep_mid_near.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.beep_mid_near, 2, 6, QtCore.Qt.AlignLeft)


        #################


        self.beep_near_close = QtWidgets.QLineEdit()
        self.beep_near_close.setMaxLength(10)
        self.beep_near_close.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_near_close.setFont(self.BASIC_FONT)
        self.beep_near_close.setPlaceholderText(f'{content["colour_legend"]["close"]}: 4 Hz')
        self.beep_near_close.setStyleSheet("background-color: rgb(255,48,48); border-radius: 15px;")
        self.beep_near_close.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.beep_near_close, 2, 8, QtCore.Qt.AlignLeft)


        #Layout Stretching
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,3)
        layout.setRowStretch(2,1)

        layout.setColumnStretch(0,40)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,300)
        layout.setColumnStretch(3,1)
        layout.setColumnStretch(4,260)
        layout.setColumnStretch(5,1)
        layout.setColumnStretch(6,220)
        layout.setColumnStretch(7,1)
        layout.setColumnStretch(8,180)
        layout.setColumnStretch(9,1)
        layout.setColumnStretch(10,180)

    def update_progressbar(self, pb, distance:float, far:float= 20, mid:float=14, near:float=8, close:float =4):
        self.far = far
        far_colour = 'rgba(0, 255, 0, 255)'
        mid_colour = 'rgba(255, 255, 0, 255)'
        near_colour = 'rgba(255, 165, 0, 255)'
        close_colour = 'rgba(255, 48, 48, 255)'
         
        distance_value = distance/far
    

        if distance_value > 1:
            pb.setValue(0)
            return
        elif distance_value <= 1 and distance_value > mid/far:
            start_colour, stop_colour = far_colour, mid_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {far_colour};
            border-radius: 10px;
            margin: 100px 10px 100px 10px;
            """)
        elif distance_value <= mid/far and distance_value > near/far:
            start_colour, stop_colour = far_colour, mid_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {mid_colour};
            border-radius: 10px;
            margin: 100px 10px 100px 10px;
            """)
        elif distance_value <= near/far and distance_value > close/far:
            start_colour, stop_colour = mid_colour, near_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {near_colour};
            border-radius: 10px;
            margin: 100px 10px 100px 10px;
            """)
        elif distance_value <= close/far and distance_value >= 0:
            start_colour, stop_colour = near_colour, close_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {close_colour};
            border-radius: 10px;
            margin: 100px 10px 100px 10px;
            """)
        else:
            return

        pb.setStyleSheet('QProgressBar::chunk {' +
                        'background-color: qlineargradient(spread:pad, x1:'+ str(0) + ', y1:0, x2:' + str(distance_value) + ', y2:0, ' + 
                        'stop: 0.5 ' + start_colour + ','
                        ' stop: 1 ' + stop_colour +
                        '); width: -1px; margin: -1px;}')
        pb.setValue((1-distance_value)*1000)

        if distance >= close:
            pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/go.png")
        else:
            pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/stop.png")
        self.distance_stop.setPixmap(pixmap.scaled(int(self.distance_display.size().width()), int(self.distance_display.size().height()), QtCore.Qt.AspectRatioMode.KeepAspectRatio))


           
    def set_car_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        self.max_distance = 964
        self.default_movable_object_weight = 41
        self.complete_layout_weight = 1185
        self.movable_object_layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(self.movable_object_layout )

        movable_object = QtWidgets.QLabel()
        #movable_object.setStyleSheet("background-color: rgb(0,0,0)")
        movable_object.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )
        movable_object.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car.png")  
        movable_object.setPixmap(pixmap.scaled(int(parent_widget.size().width()), int(parent_widget.size().height()), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.movable_object_layout.addWidget(movable_object,0,0)


        space = QtWidgets.QLabel()
        #space.setStyleSheet("background-color: rgb(255,0,0)")
        space.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )

        self.movable_object_layout.addWidget(space,0,1)


        static_object = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car_static.png")
        static_object.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        static_object.setPixmap(pixmap.scaled(int(parent_widget.size().width()), int(parent_widget.size().height()), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        static_object.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Expanding,
                 QtWidgets.QSizePolicy.Policy.Expanding,
             )

        self.movable_object_layout.addWidget(static_object,0,2)

        self.movable_object_layout.setColumnStretch(0,41)
        self.movable_object_layout.setColumnStretch(1,964)
        self.movable_object_layout.setColumnStretch(2,180)

    def update_object_distance(self, distance):

        if distance < self.far:
            new_space_weight = int(self.max_distance*(distance/self.far))
            new_movable_weight = self.default_movable_object_weight + self.max_distance - new_space_weight
        else:
            new_movable_weight = self.default_movable_object_weight
            new_space_weight = self.max_distance 

        self.movable_object_layout.setColumnStretch(0, new_movable_weight)
        self.movable_object_layout.setColumnStretch(1, new_space_weight)



    def start_stop_experiment(self):

        if not self.experiment_is_running:
            self.experiment_is_running = True
            self.start_experiment_button.setStyleSheet(f"color: {self.FONT_COLOR_LIGHT}; background-color: rgb(139,0,0); margin: 50px 200px 50px 200px; border-radius: 50px")
            self.start_experiment_button.setText("STOP EXPERIMENT")
            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment()
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.run)
            self.running_experiment.distance.connect(self.update_ui)
            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.start_experiment_button.setStyleSheet(f"color: {self.FONT_COLOR_DARK}; background-color: rgb(0,255,0); margin: 50px 200px 50px 200px; border-radius: 50px")
            self.start_experiment_button.setText("START EXPERIMENT")
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.exit()



   


    def update_ui(self, distance):
        self.distance_display.setText(f"{distance} cm")
        self.update_progressbar(pb= self.progressbar_distance, distance=distance)
        self.update_object_distance(distance)



class Running_Experiment(QtCore.QObject):
    distance = QtCore.pyqtSignal(float)
    experiment_is_running = True

    def run(self):
        try:
            while self.experiment_is_running:
                self.distance.emit(self.my_experiment())
                time.sleep(1)
        except (Exception, KeyboardInterrupt) as e:
            self.cleanup_pins()

    def cleanup_pins(self):
        GPIO.cleanup()
        pass


    def my_experiment(self):

        value = random.uniform(0,22)
        
        
        return value



