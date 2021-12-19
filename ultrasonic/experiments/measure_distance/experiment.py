#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, json
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
#import RPi.GPIO as GPIO
import time
import threading
import random

class Experiment(QWidget):

    DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, language, program_windows):
        super().__init__()
        
        self.program_windows=program_windows
        parent_layout=self.program_windows['experiment']['layout']
        

        widget=QWidget()
        self.layout=QVBoxLayout()
        widget.setLayout(self.layout)

        parent_layout.addWidget(widget)

        self.language = language
        sys_content = json.load(open(f"sys_language.json"))[self.language]
        experiment_content = json.load(open(f"{self.DIRECTORY_PATH}/information.json"))

        header =QLabel(experiment_content["experiment"][self.language]["name"])
        self.layout.addWidget(header)
        
        
        tabs_widget = QTabWidget()
        tabs_widget.setTabPosition(QTabWidget.North)
        tabs_widget.setMovable(True)
        self.tabs={}
        for k,v in sys_content["experiment_tabs"].items():
            current_tab = QFrame()
            current_layout = QGridLayout(current_tab)
            tabs_widget.addTab(current_tab ,v)
            self.tabs.update({k:{"widget":current_tab,"layout":current_layout}})


        self.layout.addWidget(tabs_widget)

        self.fill_experiment_setup(content=experiment_content["setup"])
        self.fill_experiment_info(content=experiment_content["information"])
        self.fill_experiment(content=experiment_content["experiment"])


    def fill_experiment_setup(self, content:dict):
        layout = self.tabs["setup"]["layout"]

        material = ""
        for idx, item in enumerate(content[self.language]["material"]):
            material += item
            if idx < len(content[self.language]["material"])-1:
                material += f"\n"

        material_label = QLabel(material)
        layout.addWidget(material_label,0,0)


        
        img_path=os.path.join(self.DIRECTORY_PATH,content["image"])
        pic = QLabel()
        pic.setPixmap(QPixmap(img_path))
        
        pic.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
        )
        layout.addWidget(pic, 1,0)
        layout.setRowStretch(0,0)
        layout.setRowStretch(1,1)



    def fill_experiment_info(self, content:dict):

        layout = self.tabs["information"]["layout"]

        info = ""
        for idx, item in enumerate(content[self.language]):
            info += item
            if idx < len(content[self.language])-1:
                info += f"\n"

        material_label = QLabel(info)
        layout.addWidget(material_label, 0, 0)


        movie_label = QLabel()
        img_path=os.path.join(self.DIRECTORY_PATH,content["image"])
        movie = QMovie(img_path)
        movie_label.setMovie(movie)
        movie.start()
        
        
        movie_label.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
        )
        layout.addWidget(movie_label, 0, 1)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,0)
        

    def fill_experiment(self, content:dict):
        self.experiment_is_running = False
        self.experiment_layout = self.tabs["experiment"]["layout"]
        
        self.experiment_medium_speed(parent=self.experiment_layout, content=content)

        self.experiment_led_threshholds_and_distance(parent=self.experiment_layout, content=content)

        formula = QLabel("THIS IS WHERE THE FORMULA WILL GO")
        interactive_formula = QLabel("THIS IS WHERE THE INTERACTIVE FORMULA WILL GO")

        self.experiment_layout.addWidget(formula,0,2)
        self.experiment_layout.addWidget(interactive_formula,1,2)

        self.start_experiment = QPushButton("START EXPERIMENT")
        self.start_experiment.clicked.connect(lambda:self.start_stop_experiment())
        
        self.experiment_layout.addWidget(self.start_experiment,2,2)


        

        


    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.experiment_is_running = True
            self.start_experiment.setText("STOP EXPERIMENT")

            self.Experiment_Thread = QThread()
            self.running_experiment = Running_Experiment()
            self.running_experiment.speed_of_sound = self.check_selected_medium()
            self.running_experiment.experiment_is_running = self.experiment_is_running

            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.run)
            self.running_experiment.distance.connect(self.update_ui)

            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.terminate()
            self.start_experiment.setText("START EXPERIMENT")



    def experiment_led_threshholds_and_distance(self, parent, content):
        #Widgets for Blue LED
        self.slider_blue = QSlider(Qt.Horizontal)
        self.slider_blue.setMinimum(0)
        self.slider_blue.setMaximum(10)
        self.slider_blue.setValue(3)
        self.slider_blue.setTickPosition(QSlider.TicksBelow)
        self.slider_blue.setTickInterval(1)
        label_blue = QLabel("Blau")
        self.label_blue_distance = QLabel(f"{self.slider_blue.value()} cm")

        parent.addWidget(label_blue,3,0)
        parent.addWidget(self.label_blue_distance,3,1)
        parent.addWidget(self.slider_blue,3,2)


        #Widgets for current distane
        self.current_distance = QProgressBar()
        self.current_distance.setMaximum(100)
        self.current_distance.setMinimum(0)
        self.current_distance.setValue(20)
        self.current_distance.setTextVisible(False)
        self.label_distance = QLabel(f"Aktuelle Distanz:\n{self.current_distance.value()} cm")
        parent.addWidget(self.current_distance,4,2,1,2)
        parent.addWidget(self.label_distance,4,0,1,2)

        #Widgets for Red LED
        self.slider_red = QSlider(Qt.Horizontal)
        self.slider_red.setMinimum(0)
        self.slider_red.setMaximum(10)
        self.slider_red.setValue(1)
        self.slider_red.setTickPosition(QSlider.TicksBelow)
        self.slider_red.setTickInterval(1)
        label_red = QLabel("Rot")
        self.label_red_distance = QLabel(f"{self.slider_red.value()} cm")

        parent.addWidget(label_red,5,0)
        parent.addWidget(self.label_red_distance,5,1)
        parent.addWidget(self.slider_red,5,2)


    def experiment_medium_speed(self, parent, content):
        self.medium_group=QGroupBox(content[self.language]['medium'])
        self.medium_widgets = []
        medium_layout=QVBoxLayout()
        for idx, (k, v) in enumerate(content[self.language]['speed'].items()):
            radio = QRadioButton(f"{k}(~ {v} m/s)")
            if idx == 0:
                radio.setChecked(True)
            medium_layout.addWidget(radio)
            self.medium_widgets.append(radio)

        self.custom_speed = QLineEdit()
        #custom_speed.text()
        medium_layout.addWidget(self.custom_speed)

        self.medium_group.setLayout(medium_layout)

        parent.addWidget(self.medium_group,0,0,3,2)
 


    def check_selected_medium(self):

        speed = None

        for medium in self.medium_widgets:
            if medium.isChecked():
                text = medium.text()
                try:
                    speed = text.split()[1]

                except:
                    speed = self.custom_speed.text()

                try:
                    speed = int(speed)

                except ValueError:
                    print("Custom Value is not a Number")
                    speed = None
                
                break
        
        return speed

        


    def update_ui(self, distance):
        self.label_distance.setText(f"{round(distance,2)} cm")
        bar = self.current_distance

        if distance < bar.maximum():
            bar.setValue(distance)
        elif distance >= bar.maximum():
            bar.setValue(int(bar.maximum()))



class Running_Experiment(QObject):
    distance = pyqtSignal(float)
    experiment_is_running = True
    speed_of_sound = None

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
        # GPIO.setmode(GPIO.BCM)
        # GPIO_TRIGGER = 18
        # GPIO_ECHO = 24
        # GPIO_LED_KURZ = 26
        # GPIO_LED_LANG = 5

        
        # GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        # GPIO.setup(GPIO_ECHO,GPIO.IN)
        # GPIO.setup(GPIO_LED_KURZ, GPIO.OUT)
        # GPIO.setup(GPIO_LED_LANG, GPIO.OUT)
        
        # GPIO.output(GPIO_LED_KURZ, GPIO.LOW)
        # GPIO.output(GPIO_LED_LANG,GPIO.LOW)
        
        # GPIO.output(GPIO_TRIGGER,True)
        
        # time.sleep(.00001)
        # GPIO.output(GPIO_TRIGGER, False)
        
        # StartTime = time.time()
        # StopTime = time.time()
        
        # while GPIO.input(GPIO_ECHO) == 0:
        #     StartTime = time.time()
            
        # while GPIO.input(GPIO_ECHO) == 1:
        #     StopTime = time.time()
            
        
        # TimeElapsed = StopTime - StartTime
        
        # distance = (TimeElapsed * self.speed_of_sound*100)/2
        
        # if distance < self.slider_red.value():
        #     GPIO.output(GPIO_LED_KURZ, GPIO.HIGH)
        # elif distance > self.slider_blue.value():
        #     GPIO.output(GPIO_LED_LANG,GPIO.HIGH)
            
        return distance