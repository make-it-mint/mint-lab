#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, json
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import RPi.GPIO as GPIO
import time
import threading
import random

class Experiment(QWidget):

    DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, language, program_windows, path):
        super().__init__()
        
        root_directory_path=path
        self.program_windows=program_windows
        parent_layout=self.program_windows['experiment']['layout']
        

        self.widget=QWidget()
        self.layout=QGridLayout()
        self.widget.setLayout(self.layout)

        parent_layout.addWidget(self.widget)

        self.language = language
        sys_content = json.load(open(f"{root_directory_path}/sys_language.json"))[self.language]
        experiment_content = json.load(open(f"{self.DIRECTORY_PATH}/information.json"))

        back_button=QPushButton(" X ")
        back_button.setFont(QFont("Helvetica", 30, QFont.Bold, italic=False))
        back_button.clicked.connect(self._return_to_experiment_list)
        back_button.setStyleSheet(
                """
                QPushButton {
                background-color: red;
                border: 2px solid black;
                border-radius: 25px;
                }
                """)
        self.layout.addWidget(back_button,0,0)

        header =QLabel(experiment_content["experiment"][self.language]["name"])
        header.setFont(QFont("Helvetica", 30, QFont.Bold, italic=False))
        self.layout.addWidget(header,0,1)

        self.layout.setColumnStretch(0,0)
        self.layout.setColumnStretch(1,1)
        
        self.tabs_widget = QTabWidget()
        self.tabs_widget.setTabPosition(QTabWidget.North)
        #self.tabs_widget.setMovable(True)
        
        self.tabs={}
        for k,v in sys_content["experiment_tabs"].items():
            current_tab = QFrame()
            current_layout = QGridLayout(current_tab)
            self.tabs_widget.addTab(current_tab ,v)
            self.tabs.update({k:{"widget":current_tab,"layout":current_layout}})


        self.layout.addWidget(self.tabs_widget,1,0,1,2)

        self.fill_experiment_material(content=experiment_content["setup"])
        self.fill_experiment_setup(content=experiment_content["setup"])
        self.fill_experiment_info(content=experiment_content["information"])
        self.fill_experiment(content=experiment_content["experiment"])


    def _return_to_experiment_list(self):
        if self.experiment_is_running:
            QMessageBox.about(self,"Achtung","Experiment stoppen, bevor das Fenster geschlossen werden kann")
        else:
            self.program_windows["experiment"]["widget"].hide()
            self.program_windows["experiment_list"]["widget"].show()
            self.widget.deleteLater()



    def fill_experiment_material(self, content:dict):
        layout = self.tabs["material"]["layout"]

        material = ""
        for idx, item in enumerate(content[self.language]["material"]):
            material += item
            if idx < len(content[self.language]["material"])-1:
                material += f"\n"

        material_label = QLabel(material)
        material_label.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))
        layout.addWidget(material_label,0,0)



    def fill_experiment_setup(self, content:dict):
        layout = self.tabs["setup"]["layout"]
        layout.setColumnStretch(0,1)
        layout.setRowStretch(0,0)
        
        img_path=os.path.join(self.DIRECTORY_PATH,content["image"])

        image = QPixmap(img_path)
        label = QLabel()
        label.setPixmap(image.scaledToWidth(int(self.tabs_widget.size().width()*2)))
        

        layout.addWidget(label, 0,0,alignment=Qt.AlignCenter)

        



    def fill_experiment_info(self, content:dict):

        layout = self.tabs["information"]["layout"]

        info = ""
        for idx, item in enumerate(content[self.language]):
            info += item
            if idx < len(content[self.language])-1:
                info += f"\n\n"

        material_label = QLabel(info)
        material_label.setWordWrap(True)
        material_label.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))
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
        image = QPixmap(f"{self.DIRECTORY_PATH}/formula.png")
        formula = QLabel()
        formula.setPixmap(image.scaledToWidth(formula.size().width()))

        self.experiment_layout.addWidget(formula,0,1,alignment=Qt.AlignCenter)

        self.start_experiment = QPushButton("START EXPERIMENT")
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

            self.Experiment_Thread = QThread()
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
        self.interactive_icons_frame =QFrame()
        self.interactive_icons_layout = QGridLayout()
        self.interactive_icons_frame.setLayout(self.interactive_icons_layout)
        #Widgets for Blue LED
        self.slider_blue = QSlider(Qt.Horizontal)
        self.slider_blue.setMinimum(0)
        self.slider_blue.setMaximum(30)
        self.slider_blue.setValue(3)
        self.slider_blue.setTickPosition(QSlider.TicksBelow)
        self.slider_blue.setTickInterval(0.1)
        self.slider_blue.valueChanged.connect(self.blue_value_changed)

        self.label_blue = QLabel(f"Blaue LED leuchtet ab einer Distanz von {self.slider_blue.value()} cm")
        self.label_blue.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))
        self.label_blue_led = QLabel()
        self.label_blue_led.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
            )
        self.label_blue_led.setStyleSheet(
                """
                background-color: transparent;
                """)

        self.interactive_icons_layout.addWidget(self.label_blue,0,0,1,2)
        self.interactive_icons_layout.addWidget(self.label_blue_led,1,0)
        self.interactive_icons_layout.addWidget(self.slider_blue,1,1)


        #Widgets for current distance
        self.current_distance = QProgressBar()
        self.current_distance.setMaximum(30)
        self.current_distance.setMinimum(0)
        self.current_distance.setValue(0)
        self.current_distance.setTextVisible(False)
        self.current_distance.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
            )
        self.label_distance = QLabel(f"Aktuelle Distanz: {self.current_distance.value()} cm")
        self.label_distance.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))
        self.interactive_icons_layout.addWidget(self.current_distance,3,1)
        self.interactive_icons_layout.addWidget(self.label_distance,2,0,1,2)

        #Widgets for Red LED
        self.slider_red = QSlider(Qt.Horizontal)
        self.slider_red.setMinimum(0)
        self.slider_red.setMaximum(30)
        self.slider_red.setValue(1)
        self.slider_red.setTickPosition(QSlider.TicksBelow)
        self.slider_red.setTickInterval(1)
        self.slider_red.valueChanged.connect(self.red_value_changed)
        
        self.label_red = QLabel(f"Rote LED leuchtet ab einer Distanz von {self.slider_red.value()} cm")
        self.label_red.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))
        self.label_red_led = QLabel()
        self.label_red_led.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
            )
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
        self.medium_group=QGroupBox(content[self.language]['medium'])
        self.medium_widgets = []
        medium_layout=QVBoxLayout()
        for idx, (k, v) in enumerate(content[self.language]['speed'].items()):
            radio = QRadioButton(f"{k}(~ {v} m/s)")
            radio.setFont(QFont("Helvetica", 18, QFont.Normal, italic=False))
            if idx == 0:
                radio.setChecked(True)
            medium_layout.addWidget(radio)
            self.medium_widgets.append(radio)

        self.custom_speed = QLineEdit()
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
                        QMessageBox.about(self,"Error","Eigener Wert ist keine ganze Zahl (Integer)")
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



class Running_Experiment(QObject):
    distance = pyqtSignal(float)
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
        GPIO.cleanup()
        pass


    def measure_distance(self):

        #distance = random.randint(2,40)
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
            
        return distance