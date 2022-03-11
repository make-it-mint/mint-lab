#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Experiment import ExperimentTemplate
import os
from PyQt6 import QtCore, QtGui, QtWidgets
import sys, os, json
#import RPi.GPIO as GPIO
import time
import threading
import random

class Experiment(ExperimentTemplate):

    def __init__(self, root_dir, language, screen_size, parent = None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size)
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        experiment_content = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        

        self.header.setText(experiment_content["experiment"][self.language]["name"])
        self.fill_experiment_material(materials=experiment_content["material"][self.language])
        self.fill_experiment_setup(image_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_content["setup"]["image"]))
        self.fill_experiment_info(text=experiment_content["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_content["information"]["file"]))
        self.fill_experiment(content=experiment_content["experiment"])


        self.show_fullscreen()


    def close(self):
        if self.experiment_is_running:
            QtWidgets.QMessageBox.about(self.MainWidget,"Achtung","Experiment stoppen, bevor das Fenster geschlossen werden kann")
        else:
            self.MainWidget.close() 

    

    def fill_experiment(self, content:dict):
        self.experiment_is_running = False
        self.experiment_layout = self.tabs["experiment"]["layout"]
        
        self.experiment_medium_speed(parent=self.experiment_layout, content=content)

        self.experiment_led_threshholds_and_distance(parent=self.experiment_layout, content=content)
        image = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/formula.png")
        formula = QtWidgets.QLabel()
        formula.setPixmap(image.scaledToWidth(formula.size().width()))

        self.experiment_layout.addWidget(formula,0,1)

        self.start_experiment = QtWidgets.QPushButton("START EXPERIMENT")
        self.start_experiment.clicked.connect(lambda:self.start_stop_experiment())
        
        self.experiment_layout.addWidget(self.start_experiment,1,1)

        self.experiment_layout.setRowStretch(0,2)
        self.experiment_layout.setRowStretch(1,4)
        self.experiment_layout.setRowStretch(2,3)
        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setColumnStretch(1,3)

        

        


    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.experiment_is_running = True
            self.start_experiment.setText("STOP EXPERIMENT")

            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment()
            self.running_experiment.speed_of_sound = self.check_selected_medium()
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.running_experiment.threshold_red = self.slider_red.value()
            self.running_experiment.threshold_blue = self.slider_blue.value()

            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.run)
            self.running_experiment.distance.connect(self.update_ui)

            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.exit()
            self.start_experiment.setText("START EXPERIMENT")



    def experiment_led_threshholds_and_distance(self, parent, content):
        self.interactive_icons_frame =QtWidgets.QFrame()
        self.interactive_icons_layout = QtWidgets.QGridLayout()
        self.interactive_icons_frame.setLayout(self.interactive_icons_layout)
        #Widgets for Blue LED
        self.slider_blue = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_blue.setMinimum(0)
        self.slider_blue.setMaximum(30)
        self.slider_blue.setValue(3)
        self.slider_blue.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_blue.setTickInterval(0.1)
        self.slider_blue.valueChanged.connect(self.blue_value_changed)

        self.label_blue = QtWidgets.QLabel(f"Blaue LED leuchtet ab einer Distanz von {self.slider_blue.value()} cm")
        self.label_blue.setFont(QtGui.QFont("Helvetica", 24, italic=False))
        self.label_blue_led = QtWidgets.QLabel()
        # self.label_blue_led.setSizePolicy(
        #         QSizePolicy.Expanding,
        #         QSizePolicy.Expanding,
        #     )
        self.label_blue_led.setStyleSheet(
                """
                background-color: transparent;
                """)

        self.interactive_icons_layout.addWidget(self.label_blue,0,0,1,2)
        self.interactive_icons_layout.addWidget(self.label_blue_led,1,0)
        self.interactive_icons_layout.addWidget(self.slider_blue,1,1)


        #Widgets for current distance
        self.current_distance = QtWidgets.QProgressBar()
        self.current_distance.setMaximum(30)
        self.current_distance.setMinimum(0)
        self.current_distance.setValue(0)
        self.current_distance.setTextVisible(False)
        # self.current_distance.setSizePolicy(
        #         QSizePolicy.Expanding,
        #         QSizePolicy.Expanding,
        #     )
        self.label_distance = QtWidgets.QLabel(f"Aktuelle Distanz: {self.current_distance.value()} cm")
        self.label_distance.setFont(QtGui.QFont("Helvetica", 24))
        self.interactive_icons_layout.addWidget(self.current_distance,3,1)
        self.interactive_icons_layout.addWidget(self.label_distance,2,0,1,2)

        #Widgets for Red LED
        self.slider_red = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_red.setMinimum(0)
        self.slider_red.setMaximum(30)
        self.slider_red.setValue(1)
        self.slider_red.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_red.setTickInterval(1)
        self.slider_red.valueChanged.connect(self.red_value_changed)
        
        self.label_red = QtWidgets.QLabel(f"Rote LED leuchtet ab einer Distanz von {self.slider_red.value()} cm")
        self.label_red.setFont(QtGui.QFont("Helvetica", 24))
        self.label_red_led = QtWidgets.QLabel()
        # self.label_red_led.setSizePolicy(
        #         QSizePolicy.Expanding,
        #         QSizePolicy.Expanding,
        #     )
        self.label_red_led.setStyleSheet(
                """
                background-color: transparent;
                """)

        self.interactive_icons_layout.addWidget(self.label_red,4,0,1,2)
        self.interactive_icons_layout.addWidget(self.label_red_led,5,0)
        self.interactive_icons_layout.addWidget(self.slider_red,5,1)

        self.interactive_icons_layout.setColumnStretch(0,1)
        self.interactive_icons_layout.setColumnStretch(1,20)
        self.interactive_icons_layout.setRowStretch(0,0)
        self.interactive_icons_layout.setRowStretch(1,1)
        self.interactive_icons_layout.setRowStretch(2,0)
        self.interactive_icons_layout.setRowStretch(3,1)
        self.interactive_icons_layout.setRowStretch(4,0)
        self.interactive_icons_layout.setRowStretch(5,1)

        parent.addWidget(self.interactive_icons_frame,2,0,1,2)


    def red_value_changed(self):
        self.label_red.setText(f"Rote LED leuchtet ab einer Distanz von {self.slider_red.value()} cm")
        try:
            self.running_experiment.threshold_red = self.slider_red.value()
        except:
            pass

    def blue_value_changed(self):
        self.label_blue.setText(f"Blaue LED leuchtet ab einer Distanz von {self.slider_blue.value()} cm")
        try:
            self.running_experiment.threshold_blue = self.slider_blue.value()
        except:
            pass


    def experiment_medium_speed(self, parent, content):
        self.medium_group=QtWidgets.QGroupBox(content[self.language]['medium'])
        self.medium_widgets = []
        medium_layout=QtWidgets.QVBoxLayout()
        for idx, (k, v) in enumerate(content[self.language]['speed'].items()):
            radio = QtWidgets.QRadioButton(f"{k}(~ {v} m/s)")
            radio.setFont(QtGui.QFont("Helvetica", 18))
            if idx == 0:
                radio.setChecked(True)
            medium_layout.addWidget(radio)
            self.medium_widgets.append(radio)

        self.custom_speed = QtWidgets.QLineEdit()
        #custom_speed.text()
        medium_layout.addWidget(self.custom_speed)

        self.medium_group.setLayout(medium_layout)

        parent.addWidget(self.medium_group,0,0,2,1)
 


    def check_selected_medium(self):

        speed = None

        for medium in self.medium_widgets:
            if medium.isChecked():
                text = medium.text()
                try:
                    speed = int(text.split()[1])

                except:
                    

                    try:
                        speed = int(self.custom_speed.text())

                    except ValueError:
                        QtWidgets.QMessageBox.about(self,"Error","Eigener Wert ist keine ganze Zahl (Integer)")
                        #print("Custom Value is not a Number")
                        speed = None
                
                break
        
        return speed

        


    def update_ui(self, distance):
        self.label_distance.setText(f"Aktuelle Distanz: {round(distance,2)} cm")
        bar = self.current_distance

        if distance <= self.slider_blue.value():
            self.label_blue_led.setStyleSheet(
                """
                background-color: blue;
                """)
        else:
            self.label_blue_led.setStyleSheet(
                """
                background-color: transparent;
                """)

        if distance <= self.slider_red.value():
            self.label_red_led.setStyleSheet(
                """
                background-color: red;
                """)
        else:
            self.label_red_led.setStyleSheet(
                """
                background-color: transparent;
                """)

        if distance < bar.maximum():
            bar.setValue(distance)
        elif distance >= bar.maximum():
            bar.setValue(int(bar.maximum()))



class Running_Experiment(QtCore.QObject):
    distance = QtCore.pyqtSignal(float)
    experiment_is_running = True
    speed_of_sound = None
    threshold_red = 0
    threshold_blue = 0

    def run(self):
        try:
            while self.experiment_is_running:
                if self.speed_of_sound is None:
                    break

                self.distance.emit(self.measure_distance())
                time.sleep(1)
            
            print("Measure stopped by Button Click")
            self.cleanup_pins()
            
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            print("Measurement stopped by User")
            self.cleanup_pins()

    def cleanup_pins(self):
        #GPIO.cleanup()
        pass


    def measure_distance(self):

        distance = random.randint(2,40)
        """
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24
        GPIO_LED_KURZ = 26
        GPIO_LED_LANG = 5

        
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO,GPIO.IN)
        GPIO.setup(GPIO_LED_KURZ, GPIO.OUT)
        GPIO.setup(GPIO_LED_LANG, GPIO.OUT)
        
        GPIO.output(GPIO_LED_KURZ, GPIO.LOW)
        GPIO.output(GPIO_LED_LANG,GPIO.LOW)
        
        GPIO.output(GPIO_TRIGGER,True)
        
        time.sleep(.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        StartTime = time.time()
        StopTime = time.time()
        
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
            
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
            
        
        TimeElapsed = StopTime - StartTime
        
        distance = (TimeElapsed * self.speed_of_sound*100)/2
        
        if distance <= self.threshold_red:
            GPIO.output(GPIO_LED_KURZ, GPIO.HIGH)
        if distance <= self.threshold_blue:
            GPIO.output(GPIO_LED_LANG,GPIO.HIGH)
            """
        return distance



