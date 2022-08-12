#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExperimentTemplate import UI_Template, Running_Experiment
import os, ast, json
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from software_data.constants import *
from VirtualKeyboard import VKQLineEdit, VKQTextEdit


class Experiment(UI_Template):

    def __init__(self, root_dir, language, screen_size, program_settings, parent = None):
        super().__init__(root_dir=root_dir, language = language, parent = parent, screen_size = screen_size, program_settings= program_settings)
        self.EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        if self.screen_size.width() <= 1024:
            self.SELECTED_FONT = BASIC_FONT_MID
        else:
            self.SELECTED_FONT = BASIC_FONT_LARGE
        
        experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.DEFAULT_VALUES={"ACTION_TYPE":"custom_write","TEXT":""}#MUST use double quotation marks
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=experiment_information["experiment"][self.language]["name"], hyperlink=experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=experiment_information["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",experiment_information["information"]["file"]))
        self.fill_experiment(content=experiment_information["experiment"])

    

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


        self.rfid_state = QtWidgets.QPushButton()
        self.rfid_state.setFont(self.SELECTED_FONT)
        self.rfid_state.setText(content[self.language]['rfid_state']['idle'])
        self.rfid_state.setStyleSheet(f"background-color: {FONT_COLOR_DARK}; color:{FONT_COLOR_LIGHT}; border-radius:5px; padding 5px")
        self.rfid_state.setMinimumWidth(int(self.screen_size.width()*.8))
        self.experiment_layout.addWidget(self.rfid_state,3,0, QtCore.Qt.AlignCenter)
        self.rfid_state.clicked.connect(self.cancel_experiment)


        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setRowStretch(0,1)
        self.experiment_layout.setRowStretch(1,1)
        self.experiment_layout.setRowStretch(2,1)

    

    def custom_text_interface(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)


        if not self.program_settings["has_keyboard"]:
            self.custom_text_write = VKQTextEdit(name='value', mainWindowObj=self)
        else:
            self.custom_text_write = QtWidgets.QTextEdit()
        self.custom_text_write.setAlignment(QtCore.Qt.AlignJustify)
        self.custom_text_write.setFont(self.SELECTED_FONT)
        self.custom_text_write.setMinimumWidth(int(self.screen_size.width()*.3))
        self.custom_text_write.setPlaceholderText(f'{content[self.language]["custom_text"]["write_hint"]}')
        self.custom_text_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:{FONT_COLOR_LIGHT}; border-width:0px")
        layout.addWidget(self.custom_text_write, 0, 0, QtCore.Qt.AlignLeft)


      
        self.custom_text_read = QtWidgets.QTextEdit()
        self.custom_text_read.setAlignment(QtCore.Qt.AlignJustify)
        self.custom_text_read.setFont(self.SELECTED_FONT)
        self.custom_text_read.setReadOnly(True)
        self.custom_text_read.resize(int(self.screen_size.width()*.4),int(self.screen_size.height()*.3))
        self.custom_text_read.setPlaceholderText(f'{content[self.language]["custom_text"]["read_hint"]}')
        self.custom_text_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-radius:10px; border-width:0px")
        layout.addWidget(self.custom_text_read, 0, 3, QtCore.Qt.AlignCenter)


        self.custom_text_write_button = QtWidgets.QToolButton()
        self.custom_text_write_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.custom_text_write_button.setAutoRaise(True)
        layout.addWidget(self.custom_text_write_button,0,1)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['write_img']}"
        self.custom_text_write_button.setIcon(QtGui.QIcon(image_path))
        self.custom_text_write_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1)))
        self.custom_text_write_button.clicked.connect(lambda do_it, arg="custom_write" :self.start_stop_experiment(arg))
        self.custom_text_write_button.setStyleSheet(f"background-color:{BACKGROUND_LGREEN}; border-radius: 10px; padding:10px; border-width:0px")

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

        if not self.program_settings["has_keyboard"]:
            self.personal_first_write = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.personal_first_write = QtWidgets.QLineEdit()
        self.personal_first_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_first_write.setFont(self.SELECTED_FONT)
        self.personal_first_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_first_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        layout.addWidget(self.personal_first_write, 0, 0, QtCore.Qt.AlignLeft)

        if not self.program_settings["has_keyboard"]:
            self.personal_last_write = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.personal_last_write = QtWidgets.QLineEdit()
        self.personal_last_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_last_write.setFont(self.SELECTED_FONT)
        self.personal_last_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_last_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
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
        self.personal_image_read_button.clicked.connect(lambda do_it, arg="personal_read" :self.start_stop_experiment(arg))
        self.personal_image_read_button.setStyleSheet("background-color:rgb(255,255,0); border-radius: 10px; padding:10px; border-width:0px")

        ###############
        # READ CONTENT#
        ###############
        self.personal_image_read = QtWidgets.QLabel()
        layout.addWidget(self.personal_image_read,0,4,2,1,QtCore.Qt.AlignCenter)
        self.personal_image_read.setStyleSheet(f"border-width:0px")


        self.personal_first_read = QtWidgets.QLabel()
        self.personal_first_read.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_first_read.setFont(self.SELECTED_FONT)
        self.personal_first_read.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_first_read.setText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-width:0px")
        layout.addWidget(self.personal_first_read, 0, 5, QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)

        self.personal_last_read = QtWidgets.QLabel()
        self.personal_last_read.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_last_read.setFont(self.SELECTED_FONT)
        self.personal_last_read.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_last_read.setText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-width:0px")
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
        layout.addWidget(self.blue_led,0,0, QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.blue_led_is_selected = False
        self.blue_led.clicked.connect(self.check_blue_button)


        if not self.program_settings["has_keyboard"]:
            self.blue_led_freq = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.blue_led_freq = QtWidgets.QLineEdit()
        self.blue_led_freq.setFont(self.SELECTED_FONT)
        self.blue_led_freq.setMaximumWidth(int(self.screen_size.width()*.05))
        self.blue_led_freq.setAlignment(QtCore.Qt.AlignCenter)
        self.blue_led_freq.setPlaceholderText(f'{content["frequency"]}')
        self.blue_led_freq.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        self.blue_led_freq.setValidator(QtGui.QIntValidator())
        self.blue_led_freq.setMaxLength(3)
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
        layout.addWidget(self.red_led,0,1, QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
        self.red_led_is_selected = False
        self.red_led.clicked.connect(self.check_red_button)

        if not self.program_settings["has_keyboard"]:
            self.red_led_freq = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.red_led_freq = QtWidgets.QLineEdit()
        self.red_led_freq.setFont(self.SELECTED_FONT)
        self.red_led_freq.setMaximumWidth(int(self.screen_size.width()*.05))
        self.red_led_freq.setAlignment(QtCore.Qt.AlignCenter)
        self.red_led_freq.setPlaceholderText(f'{content["frequency"]}')
        self.red_led_freq.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:rgb(230,230,230); border-width:0px")
        self.red_led_freq.setValidator(QtGui.QIntValidator())
        self.red_led_freq.setMaxLength(3)
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




        layout.setRowStretch(0,2)
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


    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["ACTION_TYPE"]= self.action_type

        if self.action_type == "custom_write":
            self.EXPERIMENT_VALUES["TEXT"]= self.custom_text_write.toPlainText()
        elif self.action_type == "personal_write":
            self.EXPERIMENT_VALUES["TEXT"]= [self.personal_first_write.text(), self.personal_last_write.text(), self.selected_image]
        elif self.action_type == "led_write":
            self.EXPERIMENT_VALUES["TEXT"]= [self.red_led_is_selected, self.red_led_freq.text(), self.blue_led_is_selected, self.blue_led_freq.text()]
        else:
            self.EXPERIMENT_VALUES["TEXT"]=""

        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)

    def start_stop_experiment(self, action_type):
        self.action_type = action_type
        
        if self.experiment_is_running == False:
            self.write_values_to_experiment_file()
            self.experiment_is_running = True

            self.Experiment_Thread = QtCore.QThread(parent=self)
            self.running_experiment = Running_Experiment(selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)

            self.Experiment_Thread.start()

    
    def cancel_experiment(self):
        if self.experiment_is_running:
            self.running_experiment.experiment.stop()
            self.update_ui(value_for_ui="-1")
            time.sleep(1)
            self.update_ui(value_for_ui="0")

   


    def update_ui(self, value_for_ui):
        rfid_content=value_for_ui
        try:
            if rfid_content == "2":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['searching'])
                self.rfid_state.setStyleSheet(f"background-color: rgb(255,255,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
            elif rfid_content == "1":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['end'])
                self.rfid_state.setStyleSheet(f"background-color: rgb(0,255,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
            elif rfid_content == "-1":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['cancelled'])
                self.rfid_state.setStyleSheet(f"background-color: rgb(255,120,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
            elif rfid_content == "-2":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['error'])
                self.rfid_state.setStyleSheet(f"background-color: rgb(255,120,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
            elif rfid_content == "0":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['idle'])
                self.rfid_state.setStyleSheet(f"background-color: {FONT_COLOR_DARK}; color:{FONT_COLOR_LIGHT}; border-radius:5px; padding 5px")
                self.experiment_is_running = False
                self.Experiment_Thread.terminate()
            elif rfid_content == "3":
                self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['blinking'])
                self.rfid_state.setStyleSheet(f"background-color: rgb(0,255,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")

            else:
                if self.action_type == "custom_write" or self.action_type == "personal_write" or self.action_type == "led_write":
                    pass
                elif self.action_type == "custom_read":
                    self.custom_text_read.setText(rfid_content)
                elif self.action_type == "personal_read":
                    personal_data = ast.literal_eval(rfid_content)
                    self.personal_first_read.setText(personal_data[0])
                    self.personal_last_read.setText(personal_data[1])
                    pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/{self.experiment_content['experiment']['personal_images'][int(personal_data[2])]}")  
                    self.personal_image_read.setPixmap(pixmap.scaled(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(e)
                  



# class Running_Experiment(QtCore.QObject):
#     rfid_content = QtCore.pyqtSignal(str)


#     def __init__(self, action_type, text=""):
#         super().__init__()
#         self.action_type=action_type
#         self.text = text

#     def run(self):
#         try:
#             self.rfid_content.emit("2")
#             if self.action_type == "custom_write" or self.action_type == "personal_write" or self.action_type == "led_write":
#                 self.set_text()
#             elif self.action_type == "custom_read" or self.action_type == "personal_read":
#                 self.rfid_content.emit(self.get_text())
#             elif self.action_type == "led_read":
#                 #print(self.get_text())
#                 led_action = ast.literal_eval(self.get_text())
#                 print("LEDs: " + str(led_action))
#                 if not self.start_led(led_action=led_action):
#                     GPIO.cleanup()
#                     self.rfid_content.emit("-2")
#                     time.sleep(2)
#                     self.rfid_content.emit("0")
#                     return

#             self.rfid_content.emit("1")
#             time.sleep(2)
#             self.rfid_content.emit("0")
#         except (Exception, KeyboardInterrupt) as e:
#             print(e)
#             GPIO.cleanup()
#             self.rfid_content.emit("-1")
#             time.sleep(2)
#             self.rfid_content.emit("0")


#     def set_text(self):
#         rfid_reader = SimpleMFRC522()
#         try:
#             rfid_reader.write(f"{self.text}")
#         except:
#             return False
#         finally:
#             GPIO.cleanup()
        
#         return True

#     def get_text(self):
#         rfid_reader = SimpleMFRC522()
#         try:
            
#             idx, text = rfid_reader.read()
#         except:
#             pass
#         finally:
#             GPIO.cleanup()
        
#         return text

#     def start_led(self, led_action:list):
        
#         try:
#             led_red_on = bool(led_action[0])
#             if led_red_on:
#                 if not led_action[1] == "":
#                     led_red_freq = int(led_action[1])
#                 else:
#                     led_red_freq = 1
#             else:
#                 led_red_freq = 1


#             led_blue_on = bool(led_action[2])
#             if led_blue_on:
#                 if not led_action[3] == "":
#                     led_blue_freq = int(led_action[3])
#                 else:
#                     led_blue_freq = 1
#             else:
#                 led_blue_freq = 1


#             GPIO.setmode(GPIO.BCM)
#             BLUE_PIN = 16
#             GPIO.setup(BLUE_PIN, GPIO.OUT)
#             GPIO.output(BLUE_PIN, GPIO.LOW)
#             RED_PIN = 20
#             GPIO.setup(RED_PIN, GPIO.OUT)
#             GPIO.output(RED_PIN, GPIO.LOW)
#             pause_time = 1/(led_red_freq*led_blue_freq*2)
#             counter = 0
#             self.rfid_content.emit("3")
#             while True:
#                 if led_blue_on and counter % led_red_freq == 0:
#                     if GPIO.input(BLUE_PIN) == GPIO.LOW:
#                         GPIO.output(BLUE_PIN, GPIO.HIGH)
#                     else:
#                         GPIO.output(BLUE_PIN, GPIO.LOW)

#                 if led_red_on and counter % led_blue_freq == 0:
#                     if GPIO.input(RED_PIN) == GPIO.LOW:
#                         GPIO.output(RED_PIN, GPIO.HIGH)
#                     else:
#                         GPIO.output(RED_PIN, GPIO.LOW)

#                 counter += 1
#                 time.sleep(pause_time)

#         except Exception as e:
#             print(e)
#             return False
#         finally:
#             GPIO.cleanup()
        
#         return True



