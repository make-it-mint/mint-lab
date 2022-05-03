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
        
        if self.screen_size.width() <= 1024:
            self.SELECTED_FONT = self.BASIC_FONT_MEDIUM
        else:
            self.SELECTED_FONT = self.BASIC_FONT_LARGE
        
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

        self.rfid_custom_text = QtWidgets.QFrame()
        self.custom_text_interface(parent_widget=self.rfid_custom_text, content=content)
        self.rfid_custom_text.setStyleSheet(f'border: 2px solid  rgb(52, 100, 135); border-radius: 10px')
        self.rfid_custom_text.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.experiment_layout.addWidget(self.rfid_custom_text, 0, 0)

        self.rfid_personal_data= QtWidgets.QFrame()
        self.custom_personal_data_interface(parent_widget=self.rfid_personal_data, content=content)
        self.rfid_personal_data.setStyleSheet(f'border: 2px solid  rgb(52, 100, 135); border-radius: 10px')
        self.rfid_personal_data.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.experiment_layout.addWidget(self.rfid_personal_data, 1, 0)

        self.rfid_leds= QtWidgets.QFrame()
        self.activate_leds_interface(parent_widget=self.rfid_leds, content=content)
        self.rfid_leds.setStyleSheet(f'border: 2px solid  rgb(52, 100, 135); border-radius: 10px')
        self.rfid_leds.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.experiment_layout.addWidget(self.rfid_leds, 2, 0)


        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setRowStretch(0,1)
        self.experiment_layout.setRowStretch(1,1)
        self.experiment_layout.setRowStretch(2,1)


    def custom_text_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        self.custom_text_write = QtWidgets.QTextEdit()
        self.custom_text_write.setAlignment(QtCore.Qt.AlignJustify)
        self.custom_text_write.setFont(self.SELECTED_FONT)
        self.custom_text_write.resize(int(self.screen_size.width()*.5),int(self.screen_size.height()*.3))
        self.custom_text_write.setPlaceholderText(f'{content[self.language]["custom_text"]["write_hint"]}')
        self.custom_text_write.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        layout.addWidget(self.custom_text_write, 0, 0, QtCore.Qt.AlignLeft)



        self.custom_text_read = QtWidgets.QTextEdit()
        self.custom_text_read.setAlignment(QtCore.Qt.AlignJustify)
        self.custom_text_read.setFont(self.SELECTED_FONT)
        self.custom_text_read.setReadOnly(True)
        self.custom_text_read.resize(int(self.screen_size.width()*.4),int(self.screen_size.height()*.3))
        self.custom_text_read.setPlaceholderText(f'{content[self.language]["custom_text"]["read_hint"]}')
        self.custom_text_read.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; border-radius:10px; border-width:0px")
        layout.addWidget(self.custom_text_read, 0, 3, QtCore.Qt.AlignCenter)


        self.custom_text_write_button = QtWidgets.QToolButton()
        self.custom_text_write_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.custom_text_write_button.setAutoRaise(True)
        layout.addWidget(self.custom_text_write_button,0,1)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['write_img']}"
        self.custom_text_write_button.setIcon(QtGui.QIcon(image_path))
        self.custom_text_write_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.custom_text_write_button.clicked.connect(lambda do_it, arg="custom_write" :self.start_stop_experiment(arg))
        self.custom_text_write_button.setStyleSheet("background-color:rgb(0,255,0); border-radius: 10px; padding:10px; border-width:0px")

        self.custom_text_read_button = QtWidgets.QToolButton()
        self.custom_text_read_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.custom_text_read_button.setAutoRaise(True)
        layout.addWidget(self.custom_text_read_button,0,2)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['read_img']}"
        self.custom_text_read_button.setIcon(QtGui.QIcon(image_path))
        self.custom_text_read_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.custom_text_read_button.clicked.connect(lambda do_it, arg="custom_read" :self.start_stop_experiment(arg))
        self.custom_text_read_button.setStyleSheet("background-color:rgb(255,255,0); border-radius: 10px; padding:10px; border-width:0px")
        

        layout.setColumnStretch(0,4)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,1)
        layout.setColumnStretch(3,4)


    def custom_personal_data_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        ################
        # WRITE CONTENT#
        ################
        self.selected_image = 0

        self.personal_first_write = QtWidgets.QLineEdit()
        self.personal_first_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_first_write.setFont(self.SELECTED_FONT)
        self.personal_first_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_first_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_write.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        layout.addWidget(self.personal_first_write, 0, 0, QtCore.Qt.AlignLeft)

        self.personal_last_write = QtWidgets.QLineEdit()
        self.personal_last_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_last_write.setFont(self.SELECTED_FONT)
        self.personal_last_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_last_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_write.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        layout.addWidget(self.personal_last_write, 1, 0, QtCore.Qt.AlignLeft)

        self.personal_image_write = QtWidgets.QToolButton()
        self.personal_image_write.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        layout.addWidget(self.personal_image_write,0,1,2,1)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['personal_images'][self.selected_image]}"
        self.personal_image_write.setIcon(QtGui.QIcon(image_path))
        self.personal_image_write.setStyleSheet(f"border-width:0px")
        self.personal_image_write.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.personal_image_write.clicked.connect(lambda do_it, arg=content :self.update_personal_image(arg))

        #############
        ## BUTTONS  #
        #############

        self.personal_image_write_button = QtWidgets.QToolButton()
        self.personal_image_write_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.personal_image_write_button.setAutoRaise(True)
        layout.addWidget(self.personal_image_write_button,0,2,2,1)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['write_img']}"
        self.personal_image_write_button.setIcon(QtGui.QIcon(image_path))
        self.personal_image_write_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.personal_image_write_button.clicked.connect(lambda do_it, arg="personal_write" :self.start_stop_experiment(arg))
        self.personal_image_write_button.setStyleSheet("background-color:rgb(0,255,0); border-radius: 10px; padding:10px; border-width:0px")

        self.personal_image_read_button = QtWidgets.QToolButton()
        self.personal_image_read_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.personal_image_read_button.setAutoRaise(True)
        layout.addWidget(self.personal_image_read_button,0,3,2,1)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['read_img']}"
        self.personal_image_read_button.setIcon(QtGui.QIcon(image_path))
        self.personal_image_read_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.personal_image_read_button.clicked.connect(lambda do_it, arg="custom_read" :self.start_stop_experiment(arg))
        self.personal_image_read_button.setStyleSheet("background-color:rgb(255,255,0); border-radius: 10px; padding:10px; border-width:0px")

        ###############
        # READ CONTENT#
        ###############
        self.personal_image_read = QtWidgets.QLabel()
        layout.addWidget(self.personal_image_read,0,4,2,1)
        self.personal_image_read.setStyleSheet(f"border-width:0px")


        self.personal_first_read = QtWidgets.QLabel()
        self.personal_first_read.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_first_read.setFont(self.SELECTED_FONT)
        self.personal_first_read.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_first_read.setText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_read.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; border-width:0px")
        layout.addWidget(self.personal_first_read, 0, 5, QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)

        self.personal_last_read = QtWidgets.QLabel()
        self.personal_last_read.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_last_read.setFont(self.SELECTED_FONT)
        self.personal_last_read.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_last_read.setText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_read.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; border-width:0px")
        layout.addWidget(self.personal_last_read, 1, 5, QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)

        

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)
        layout.setColumnStretch(0,8)
        layout.setColumnStretch(1,3)
        layout.setColumnStretch(2,3)
        layout.setColumnStretch(3,3)
        layout.setColumnStretch(4,5)
        layout.setColumnStretch(5,7)

    def update_personal_image(self, content):
        images = content["personal_images"]
        if self.selected_image == len(images)-1:
            self.selected_image = 0
        else:
            self.selected_image += 1

        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['personal_images'][self.selected_image]}"
        self.personal_image_write.setIcon(QtGui.QIcon(image_path))
        self.personal_image_write.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))


    def activate_leds_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        ############
        # BLUE LED #
        ############
        self.blue_led = QtWidgets.QToolButton()
        self.blue_led.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        image_path = f"{self.EXPERIMENT_DIR}/assets/blue.png"
        self.blue_led.setIcon(QtGui.QIcon(image_path))
        self.blue_led.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.blue_led.setStyleSheet(f"padding:4px")
        layout.addWidget(self.blue_led,0,0, QtCore.Qt.AlignCenter)
        self.blue_led_is_selected = False
        self.blue_led.clicked.connect(self.check_blue_button)

        self.blue_led_freq = QtWidgets.QLineEdit()
        self.blue_led_freq.setFont(self.SELECTED_FONT)
        self.blue_led_freq.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.blue_led_freq.setAlignment(QtCore.Qt.AlignCenter)
        self.blue_led_freq.setPlaceholderText(f'{content["frequency"]}')
        self.blue_led_freq.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        self.blue_led_freq.setValidator(QtGui.QDoubleValidator())
        self.blue_led_freq.setMaxLength(1)
        layout.addWidget(self.blue_led_freq, 1, 0, QtCore.Qt.AlignCenter)

        ############
        # RED  LED #
        ############
        self.red_led = QtWidgets.QToolButton()
        self.red_led.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        image_path = f"{self.EXPERIMENT_DIR}/assets/red.png"
        self.red_led.setIcon(QtGui.QIcon(image_path))
        self.red_led.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.red_led.setStyleSheet(f"padding:4px")
        layout.addWidget(self.red_led,0,1, QtCore.Qt.AlignCenter)
        self.red_led_is_selected = False
        self.red_led.clicked.connect(self.check_red_button)

        self.red_led_freq = QtWidgets.QLineEdit()
        self.red_led_freq.setFont(self.SELECTED_FONT)
        self.red_led_freq.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.red_led_freq.setAlignment(QtCore.Qt.AlignCenter)
        self.red_led_freq.setPlaceholderText(f'{content["frequency"]}')
        self.red_led_freq.setStyleSheet(f"color:{self.FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        self.red_led_freq.setValidator(QtGui.QDoubleValidator())
        self.red_led_freq.setMaxLength(1)
        layout.addWidget(self.red_led_freq, 1, 1, QtCore.Qt.AlignCenter)


        #############
        ## BUTTONS  #
        #############

        self.led_write_button = QtWidgets.QToolButton()
        self.led_write_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.led_write_button.setAutoRaise(True)
        layout.addWidget(self.led_write_button,0,2,2,1, QtCore.Qt.AlignCenter)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['write_img']}"
        self.led_write_button.setIcon(QtGui.QIcon(image_path))
        self.led_write_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.led_write_button.clicked.connect(lambda do_it, arg="led_write" :self.start_stop_experiment(arg))
        self.led_write_button.setStyleSheet("background-color:rgb(0,255,0); border-radius: 10px; padding:10px; border-width:0px")

        self.led_read_button = QtWidgets.QToolButton()
        self.led_read_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.led_read_button.setAutoRaise(True)
        layout.addWidget(self.led_read_button,0,3,2,1, QtCore.Qt.AlignLeft)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['read_img']}"
        self.led_read_button.setIcon(QtGui.QIcon(image_path))
        self.led_read_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.led_read_button.clicked.connect(lambda do_it, arg="led_read" :self.start_stop_experiment(arg))
        self.led_read_button.setStyleSheet("background-color:rgb(255,255,0); border-radius: 10px; padding:10px; border-width:0px")




        layout.setRowStretch(0,1)
        layout.setRowStretch(1,1)
        layout.setColumnStretch(0,2)
        layout.setColumnStretch(1,2)
        layout.setColumnStretch(2,4)
        layout.setColumnStretch(3,2)


    def check_blue_button(self):
        if self.blue_led_is_selected:
            self.blue_led.setStyleSheet(f"background-color: rgb(62, 110, 145); padding:4px")
            self.blue_led_is_selected = False
        else:
            self.blue_led.setStyleSheet(f"background-color: rgb(52, 100, 135); padding:4px")
            self.blue_led_is_selected = True

    def check_red_button(self):
        if self.red_led_is_selected:
            self.red_led.setStyleSheet(f"background-color: rgb(62, 110, 145); padding:4px")
            self.red_led_is_selected = False
        else:
            self.red_led.setStyleSheet(f"background-color: rgb(52, 100, 135); padding:4px")
            self.red_led_is_selected = True


    def start_stop_experiment(self, action_type):

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



