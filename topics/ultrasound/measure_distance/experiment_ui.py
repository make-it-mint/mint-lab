#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExperimentTemplate import UI_Template, Running_Experiment
from PyQt5 import QtCore, QtGui, QtWidgets
import os, json
from software_data.constants import *
from VirtualKeyboard import VKQLineEdit

class Experiment(UI_Template):

    def __init__(self, root_dir, language, screen_size, program_settings, parent = None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size, program_settings= program_settings)
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        if self.screen_size.width() <= 1024:
            self.SELECTED_FONT = BASIC_FONT_SMALL
            self.CUR_DISTANCE_FONT = QtGui.QFont('Arial', 32)
        else:
            self.SELECTED_FONT = BASIC_FONT_LARGE
            self.CUR_DISTANCE_FONT = QtGui.QFont('Arial', 48)

        experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.DEFAULT_VALUES={"SPEED_OF_SOUND":330,"RED":10,"BLUE":5}#MUST use double quotation marks
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=experiment_information["experiment"][self.language]["name"], hyperlink=experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=experiment_information["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_information["information"]["file"]))
        self.fill_experiment(content=experiment_information["experiment"])

    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.write_values_to_experiment_file()
            self.experiment_is_running = True
            self.start_experiment.setStyleSheet(f"color: {FONT_COLOR_LIGHT}; background-color: rgb(239,0,0); margin: 10px 20px 10px 20px; border-radius: 10px")
            self.start_experiment.setText(self.program_settings["stop_experiment"][self.language])

            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment(selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)

            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.start_experiment.setStyleSheet(f"color: {FONT_COLOR_DARK}; background-color: rgb(0,255,0); margin: 10px 20px 10px 20px; border-radius: 10px")
            self.running_experiment.experiment_is_running = self.experiment_is_running
            if self.selected_system["system_id"] == 0:
                self.running_experiment.experiment.stop()
            self.Experiment_Thread.exit()
            self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)

    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["SPEED_OF_SOUND"] = self.check_selected_medium()
        self.EXPERIMENT_VALUES["RED"] = self.slider_red.value()
        self.EXPERIMENT_VALUES["BLUE"] = self.slider_blue.value()
        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)



    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        
        self.experiment_medium_speed(parent=self.experiment_layout, content=content)

        self.experiment_led_threshholds_and_distance(parent=self.experiment_layout, content=content)
        image = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/formula.png")
        formula = QtWidgets.QLabel()
        formula.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        formula.setPixmap(image.scaled(int(self.screen_size.width()*.5), int(self.screen_size.height()*.25), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        self.experiment_layout.addWidget(formula,0,1)

        self.start_experiment = QtWidgets.QPushButton(self.program_settings["start_experiment"][self.language])
        self.start_experiment.clicked.connect(lambda:self.start_stop_experiment())
        
        self.experiment_layout.addWidget(self.start_experiment,1,1)

        self.experiment_layout.setRowStretch(0,2)
        self.experiment_layout.setRowStretch(1,4)
        self.experiment_layout.setRowStretch(2,3)
        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setColumnStretch(1,3)

        

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
        self.label_blue.setFont(self.SELECTED_FONT)
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
        self.label_distance.setFont(self.SELECTED_FONT)
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
        self.label_red.setFont(self.SELECTED_FONT)
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
            radio.setFont(self.SELECTED_FONT)
            if idx == 0:
                radio.setChecked(True)
            medium_layout.addWidget(radio)
            self.medium_widgets.append(radio)

        if not self.program_settings["has_keyboard"]:
            self.custom_speed = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.custom_speed = QtWidgets.QLineEdit()

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
                        speed = None
                
                break
        
        return speed

        


    def update_ui(self, value_for_ui):
        distance = 0.0
        try:
            value_pairs = value_for_ui.split(":")
            for pair in value_pairs:
                key, value = pair.split("=")
                if key == "d":
                    distance=float(value)
        except Exception as e:
            print(e)
            return

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
