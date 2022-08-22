#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExperimentTemplate import UI_Template, Running_Experiment
from PyQt5 import QtCore, QtGui, QtWidgets
import os, json
from software_data.constants import *
from VirtualKeyboard import VKQLineEdit
from CustomWidgets import SliderProxyStyle

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

        self.experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.selected_button_idx = 0
        self.DEFAULT_VALUES={"SPEED_OF_SOUND":330,"RED":10,"BLUE":5}
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=self.experiment_information["experiment"][self.language]["name"], hyperlink=self.experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=self.experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=self.experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=self.experiment_information["information"][self.language], file_paths=[f"{self.EXPERIMENT_DIR}/assets/{item}" for item in self.experiment_information['information']['files'][self.language]])
        self.fill_experiment(content=self.experiment_information["experiment"])

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

    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["SPEED_OF_SOUND"] = list(self.speeds[self.selected_button_idx].values())[0]
        self.EXPERIMENT_VALUES["RED"] = self.red_slider.value()
        self.EXPERIMENT_VALUES["BLUE"] = self.blue_slider.value()
        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)



    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        self.experiment_layout.setRowStretch(0,1)
        self.experiment_layout.setRowStretch(1,4)
        self.experiment_layout.setColumnStretch(0,4)
        self.experiment_layout.setColumnStretch(1,1)

        self.speeds_frame = QtWidgets.QFrame()
        self.speeds_frame.setSizePolicy(SIZE_POLICY)
        self.speeds_frame.setStyleSheet(BORDER_STYLESHEET_THIN)
        self.speeds_interface(parent_widget=self.speeds_frame, content=content)
        self.experiment_layout.addWidget(self.speeds_frame,0,0,1,2)

        self.experiment_frame = QtWidgets.QFrame()
        self.experiment_frame.setSizePolicy(SIZE_POLICY)
        self.experiment_frame.setStyleSheet(f"border-radius: 0px")
        self.experiment_interface(parent_widget=self.experiment_frame, content=content)
        self.experiment_layout.addWidget(self.experiment_frame,1,0,1,1)
    

        self.start_experiment_button = QtWidgets.QToolButton()
        self.start_experiment_button.setAutoRaise(True)
        self.start_experiment_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.start_experiment_button.resize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2))
        self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/start_round.png"))
        self.start_experiment_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2)))
        self.start_experiment_button.setStyleSheet(f"border-radius: 0px")
        self.start_experiment_button.setSizePolicy(SIZE_POLICY_PREF)
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,1,1, QtCore.Qt.AlignCenter)
    

        



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




    def speeds_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)
        self.speed_buttons=[]
        self.speed_texts=[]
        self.speeds=[]
        
        for idx, (medium,speed) in enumerate(content[self.language]['speed'].items()):

            button = QtWidgets.QPushButton()
            image_path = f"{self.EXPERIMENT_DIR}/assets/{medium}.png"
            button.setIcon(QtGui.QIcon(image_path))
            button.setStyleSheet(f"border-width:0px; border-radius:20px")
            button.setSizePolicy(SIZE_POLICY)
            button.setIconSize(QtCore.QSize(int(parent_widget.size().width()*.15), int(parent_widget.size().height()*.4)))
            button.clicked.connect(lambda do_it, arg=idx :self.select_medium(arg))
            layout.addWidget(button,0,idx,QtCore.Qt.AlignCenter)

            if medium == "other":
                if not self.program_settings["has_keyboard"]:
                    text = VKQLineEdit(name='value', mainWindowObj=self)
                else:
                    text = QtWidgets.QLineEdit()
                text.setAlignment(QtCore.Qt.AlignJustify)
                text.setFont(BASIC_FONT_LARGE)
                text.setValidator(QtGui.QIntValidator())
                text.setSizePolicy(SIZE_POLICY)
                text.setPlaceholderText(f'm/s')
                text.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:{BACKGROUND_WHITE}; border-width:0px")
                
            else:
                text = QtWidgets.QLabel(f"{speed} m/s")
                text.setFont(BASIC_FONT_LARGE)
                text.setStyleSheet(f"color:{FONT_COLOR_LIGHT}; border-width:0px")
                text.setSizePolicy(SIZE_POLICY)
            
            layout.addWidget(text,1,idx,QtCore.Qt.AlignCenter)


            self.speed_buttons.append(button)
            self.speed_texts.append(text)
            self.speeds.append({medium:speed})

            layout.setColumnStretch(idx,1)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)

        self.select_medium(self.selected_button_idx)

    def select_medium(self, button_idx):
        self.selected_button_idx=button_idx
        for idx, medium_button in enumerate(self.speed_buttons):
            if idx == button_idx:
                medium_button.setStyleSheet(f"background-color:{BACKGROUND_COLOR_DARK};border-width:0px; border-radius:20px")
            else:
                medium_button.setStyleSheet(f"background-color:{BACKGROUND_COLOR};border-width:0px; border-radius:20px")
        #print(list(self.speeds[button_idx].values())[0])
        

    def experiment_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        layout.setRowStretch(0,8)
        layout.setRowStretch(1,1)
        layout.setRowStretch(2,1)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,1)

        
        self.red_slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
        slider_handle_style = SliderProxyStyle(self.red_slider.style())
        self.red_slider.setSizePolicy(SIZE_POLICY)
        self.red_slider.setStyleSheet("QSlider::handle:vertical {background-color: red; border:2px solid black;border-radius:20px}")
        self.red_slider.setStyle(slider_handle_style)
        self.red_slider.valueChanged.connect(self.slider_red_changed)
        layout.addWidget(self.red_slider,0,0)

        self.led_red = QtWidgets.QToolButton()
        self.led_red.setAutoRaise(True)
        self.led_red.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.led_red.setIcon(QtGui.QIcon(f"{self.EXPERIMENT_DIR}/assets/led_red.png"))
        self.led_red.setIconSize(QtCore.QSize(int(parent_widget.size().width()*.1), int(parent_widget.size().width()*.1)))
        self.led_red.setStyleSheet(f"border-radius: 0px")
        self.led_red.setSizePolicy(SIZE_POLICY)
        self.led_red.setEnabled(False)
        layout.addWidget(self.led_red,1,0, QtCore.Qt.AlignCenter)

        self.threshold_red = QtWidgets.QLabel(f"0 cm")
        self.threshold_red.setSizePolicy(SIZE_POLICY_PREF)
        self.threshold_red.setFont(BASIC_FONT_LARGE)
        self.threshold_red.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_red.setStyleSheet(f"color:{FONT_COLOR_LIGHT}")
        layout.addWidget(self.threshold_red,2,0, QtCore.Qt.AlignCenter)




        self.blue_slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.blue_slider.setSizePolicy(SIZE_POLICY_PREF)
        self.blue_slider.setStyleSheet("QSlider::handle:vertical {background-color: blue; border:2px solid black;border-radius:20px}")
        self.blue_slider.setStyle(slider_handle_style)
        self.blue_slider.valueChanged.connect(self.slider_blue_changed)
        layout.addWidget(self.blue_slider,0,2)

        self.led_blue = QtWidgets.QToolButton()
        self.led_blue.setAutoRaise(True)
        self.led_blue.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.led_blue.setIcon(QtGui.QIcon(f"{self.EXPERIMENT_DIR}/assets/led_blue.png"))
        self.led_blue.setIconSize(QtCore.QSize(int(parent_widget.size().width()*.1), int(parent_widget.size().width()*.1)))
        self.led_blue.setStyleSheet(f"border-radius: 0px")
        self.led_blue.setSizePolicy(SIZE_POLICY_PREF)
        self.led_blue.setEnabled(False)
        layout.addWidget(self.led_blue,1,2, QtCore.Qt.AlignCenter)

        self.threshold_blue = QtWidgets.QLabel(f"0 cm")
        self.threshold_blue.setSizePolicy(SIZE_POLICY_PREF)
        self.threshold_blue.setFont(BASIC_FONT_LARGE)
        self.threshold_blue.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_blue.setStyleSheet(f"color:{FONT_COLOR_LIGHT}")
        layout.addWidget(self.threshold_blue,2,2, QtCore.Qt.AlignCenter)


        self.current_distance = QtWidgets.QLabel(f"{self.experiment_information['experiment'][self.language]['distance']}\n0")
        self.current_distance.setSizePolicy(SIZE_POLICY_PREF)
        self.current_distance.setFont(BASIC_FONT_LARGE)
        self.current_distance.setAlignment(QtCore.Qt.AlignCenter)
        self.current_distance.setStyleSheet(f"color:{FONT_COLOR_LIGHT}")
        layout.addWidget(self.current_distance,1,1,2,1, QtCore.Qt.AlignCenter)

        self.current_distance_bar = QtWidgets.QProgressBar()
        self.current_distance_bar.setOrientation(QtCore.Qt.Vertical)
        self.current_distance_bar.setSizePolicy(SIZE_POLICY_H)
        self.current_distance_bar.setTextVisible(False)
        self.current_distance_bar.setStyleSheet(f"QProgressBar::chunk{{background-color: {BACKGROUND_LGREEN};}}")
        self.current_distance_bar.setRange(0,100)
        self.current_distance_bar.setFixedWidth(120)
        self.current_distance_bar.setValue(0)
        layout.addWidget(self.current_distance_bar,0,1, QtCore.Qt.AlignHCenter)



    def slider_red_changed(self):
        self.threshold_red.setText(f"{self.red_slider.value()} cm")

    def slider_blue_changed(self):
        self.threshold_blue.setText(f"{self.blue_slider.value()} cm")


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

        self.current_distance.setText(f"{self.experiment_information['experiment'][self.language]['distance']}\n{round(distance,2)}")
        bar = self.current_distance_bar

        self.led_blue.setEnabled(True) if distance <= self.blue_slider.value() else self.led_blue.setEnabled(False)
        self.led_red.setEnabled(True) if distance <= self.red_slider.value() else self.led_red.setEnabled(False)

        if distance < bar.maximum():
            bar.setValue(distance)
        elif distance >= bar.maximum():
            bar.setValue(int(bar.maximum()))
