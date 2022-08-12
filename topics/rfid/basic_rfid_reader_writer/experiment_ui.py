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
        
        self.experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.DEFAULT_VALUES={"EXPERIMENT":"TEXT","ACTION":"WRITE","CONTENT":""}#MUST use double quotation marks
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=self.experiment_information["experiment"][self.language]["name"], hyperlink=self.experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=self.experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=self.experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=self.experiment_information["information"][self.language], file_path=os.path.join(self.EXPERIMENT_DIR,"assets",self.experiment_information["information"]["file"]))
        self.fill_experiment(content=self.experiment_information["experiment"])

    

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setColumnStretch(1,1)
        self.experiment_layout.setColumnStretch(2,1)
        self.experiment_layout.setRowStretch(0,2)
        self.experiment_layout.setRowStretch(1,8)

        self.activate_text_bt = QtWidgets.QPushButton()
        self.activate_text_bt.setStyleSheet(f"background-color:{BACKGROUND_LGREEN}")
        self.activate_text_bt.setSizePolicy(SIZE_POLICY)
        self.activate_text_bt.clicked.connect(self.activate_experiment_text)
        self.experiment_layout.addWidget(self.activate_text_bt,0,0)

        self.rfid_custom_text = QtWidgets.QFrame()
        self.custom_text_interface(parent_widget=self.rfid_custom_text, content=content)
        self.rfid_custom_text.setStyleSheet(BORDER_STYLESHEET_THIN)
        self.rfid_custom_text.setSizePolicy(SIZE_POLICY)
        self.experiment_layout.addWidget(self.rfid_custom_text, 1, 0, 2, 1)

        self.activate_person_bt = QtWidgets.QPushButton()
        self.activate_person_bt.setStyleSheet(f"background-color:{BACKGROUND_RED}")
        self.activate_person_bt.setSizePolicy(SIZE_POLICY)
        self.activate_person_bt.clicked.connect(self.activate_experiment_person)
        self.experiment_layout.addWidget(self.activate_person_bt,0,1)

        self.rfid_personal_data= QtWidgets.QFrame()
        self.custom_personal_data_interface(parent_widget=self.rfid_personal_data, content=content)
        self.rfid_personal_data.setStyleSheet(BORDER_STYLESHEET_THIN)
        self.rfid_personal_data.setSizePolicy(SIZE_POLICY)
        self.experiment_layout.addWidget(self.rfid_personal_data, 1, 1, 2, 1)


        self.rfid_state_bt = QtWidgets.QToolButton()
        self.rfid_state_bt.setAutoRaise(True)
        self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_COLOR}")
        self.rfid_state_bt.setSizePolicy(SIZE_POLICY)
        self.rfid_state_bt.clicked.connect(self.cancel_experiment)
        self.rfid_state_bt.setEnabled(False)
        self.experiment_layout.addWidget(self.rfid_state_bt,0,2)


        self.experiment_buttons= QtWidgets.QFrame()
        self.set_experiment_buttons(parent_widget=self.experiment_buttons, content=content)
        self.experiment_buttons.setStyleSheet("border-radius: 0px")
        self.experiment_buttons.setSizePolicy(SIZE_POLICY)
        self.experiment_layout.addWidget(self.experiment_buttons, 1, 2, 2, 1)


    def activate_experiment_text(self):
        self.activate_text_bt.setStyleSheet(f"background-color:{BACKGROUND_LGREEN};")
        self.activate_person_bt.setStyleSheet(f"background-color:{BACKGROUND_RED};")
        self.EXPERIMENT_VALUES["EXPERIMENT"] = "TEXT"

    def activate_experiment_person(self):
        self.activate_text_bt.setStyleSheet(f"background-color:{BACKGROUND_RED};")
        self.activate_person_bt.setStyleSheet(f"background-color:{BACKGROUND_LGREEN};")
        self.EXPERIMENT_VALUES["EXPERIMENT"] = "PERSON"



    

    def custom_text_interface(self, parent_widget, content):
        pass
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)


        if not self.program_settings["has_keyboard"]:
            self.custom_text_write = VKQTextEdit(name='value', mainWindowObj=self)
        else:
            self.custom_text_write = QtWidgets.QTextEdit()
        self.custom_text_write.setFont(self.SELECTED_FONT)
        self.custom_text_write.setSizePolicy(SIZE_POLICY)
        self.custom_text_write.setPlaceholderText(f'{content[self.language]["custom_text"]["write_hint"]}')
        self.custom_text_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:{FONT_COLOR_LIGHT}; border-width:0px")
        layout.addWidget(self.custom_text_write,0,0)

        separator = QtWidgets.QLabel("-------------------")
        separator.setFont(self.SELECTED_FONT)
        separator.setStyleSheet(f"color:{FONT_COLOR_LIGHT}; border-width:0px")
        layout.addWidget(separator,1,0,QtCore.Qt.AlignCenter)



      
        self.custom_text_read = QtWidgets.QTextEdit()
        self.custom_text_read.setFont(self.SELECTED_FONT)
        self.custom_text_read.setReadOnly(True)
        self.custom_text_read.setSizePolicy(SIZE_POLICY_H)
        self.custom_text_read.resize(QtCore.QSize(int(parent_widget.size().width()*.9),int(parent_widget.size().height()*.4)))
        self.custom_text_read.setPlaceholderText(f'{content[self.language]["custom_text"]["read_hint"]}')
        self.custom_text_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-radius:10px; border-width:0px")
        layout.addWidget(self.custom_text_read,2,0,QtCore.Qt.AlignCenter)

        layout.setRowStretch(0,1)
        layout.setRowStretch(2,1)
        


    def custom_personal_data_interface(self, parent_widget, content):
        pass
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        # ################
        # # WRITE CONTENT#
        # ################
        self.selected_image = 0

        if not self.program_settings["has_keyboard"]:
            self.personal_first_write = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.personal_first_write = QtWidgets.QLineEdit()
        self.personal_first_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_first_write.setFont(self.SELECTED_FONT)
        self.personal_first_write.setSizePolicy(SIZE_POLICY)
        #self.personal_first_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_first_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:{BACKGROUND_WHITE}; border-width:0px")
        layout.addWidget(self.personal_first_write,0,0)


        if not self.program_settings["has_keyboard"]:
            self.personal_last_write = VKQLineEdit(name='value', mainWindowObj=self)
        else:
            self.personal_last_write = QtWidgets.QLineEdit()
        self.personal_last_write.setAlignment(QtCore.Qt.AlignJustify)
        self.personal_last_write.setFont(self.SELECTED_FONT)
        self.personal_last_write.setSizePolicy(SIZE_POLICY)
        #self.personal_last_write.resize(int(self.screen_size.width()*.2),int(self.screen_size.height()*.3))
        self.personal_last_write.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_write.setStyleSheet(f"color:{FONT_COLOR_DARK}; background-color:{BACKGROUND_WHITE}; border-width:0px")
        layout.addWidget(self.personal_last_write,0,1)

        self.personal_image_write = QtWidgets.QToolButton()
        self.personal_image_write.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['personal_images'][self.selected_image]}"
        self.personal_image_write.setIcon(QtGui.QIcon(image_path))
        self.personal_image_write.setStyleSheet(f"border-width:0px")
        self.personal_last_write.setSizePolicy(SIZE_POLICY)
        self.personal_image_write.setIconSize(QtCore.QSize(int(self.screen_size.width()*.15), int(self.screen_size.height()*.15)))
        self.personal_image_write.clicked.connect(lambda do_it, arg=content :self.update_personal_image(arg))
        layout.addWidget(self.personal_image_write,1,0,1,2,QtCore.Qt.AlignCenter)

        separator = QtWidgets.QLabel("-------------------")
        separator.setFont(self.SELECTED_FONT)
        separator.setStyleSheet(f"color:{FONT_COLOR_LIGHT};border-width:0px")
        layout.addWidget(separator,2,0,1,2,QtCore.Qt.AlignCenter)

  

        # ###############
        # # READ CONTENT#
        # ###############
        self.personal_image_read = QtWidgets.QLabel()
        self.personal_image_read.setStyleSheet(f"border-width:0px")
        #pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/{content['personal_images'][self.selected_image]}")  
        #self.personal_image_read.setPixmap(pixmap.scaled(int(self.screen_size.width()*.15), int(self.screen_size.height()*.15), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self.personal_image_read,4,0,1,2,QtCore.Qt.AlignCenter)
        


        self.personal_first_read = QtWidgets.QTextEdit()
        self.personal_first_read.setFont(self.SELECTED_FONT)
        self.personal_first_read.setReadOnly(True)
        self.personal_first_read.setSizePolicy(SIZE_POLICY)
        self.personal_first_read.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["first_name"]}')
        self.personal_first_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-radius:10px; border-width:0px")
        layout.addWidget(self.personal_first_read,3,0,QtCore.Qt.AlignCenter)

        self.personal_last_read = QtWidgets.QTextEdit()
        self.personal_last_read.setFont(self.SELECTED_FONT)
        self.personal_last_read.setReadOnly(True)
        self.personal_last_read.setSizePolicy(SIZE_POLICY)
        self.personal_last_read.setPlaceholderText(f'{content[self.language]["custom_personal_data"]["last_name"]}')
        self.personal_last_read.setStyleSheet(f"color:{FONT_COLOR_DARK}; border-radius:10px; border-width:0px")
        layout.addWidget(self.personal_last_read,3,1,QtCore.Qt.AlignCenter)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,4)
        layout.setRowStretch(3,1)
        layout.setRowStretch(4,4)


    def update_personal_image(self, content):
        images = content["personal_images"]
        if self.selected_image == len(images)-1:
            self.selected_image = 0
        else:
            self.selected_image += 1

        image_path = f"{self.EXPERIMENT_DIR}/assets/{content['personal_images'][self.selected_image]}"
        self.personal_image_write.setIcon(QtGui.QIcon(image_path))
        self.personal_image_write.setIconSize(QtCore.QSize(int(self.screen_size.width()*.15), int(self.screen_size.height()*.15)))


    def set_experiment_buttons(self, parent_widget, content):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)


        self.write_rfid = QtWidgets.QToolButton()
        self.write_rfid.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        image_path = f"{self.EXPERIMENT_DIR}/assets/write.png"
        self.write_rfid.setIcon(QtGui.QIcon(image_path))
        self.write_rfid.setStyleSheet(f"border-width:0px")
        self.write_rfid.setSizePolicy(SIZE_POLICY)
        self.write_rfid.setIconSize(QtCore.QSize(int(parent_widget.size().width()*.8), int(parent_widget.size().height()*.4)))
        self.write_rfid.clicked.connect(lambda do_it, arg="WRITE" :self.start_stop_experiment(arg))
        layout.addWidget(self.write_rfid,0,0,QtCore.Qt.AlignCenter)


        separator = QtWidgets.QLabel("-------------------")
        separator.setFont(self.SELECTED_FONT)
        separator.setStyleSheet(f"color:{FONT_COLOR_LIGHT}; border-width:0px")
        layout.addWidget(separator,1,0,QtCore.Qt.AlignCenter)


        self.read_rfid = QtWidgets.QToolButton()
        self.read_rfid.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        image_path = f"{self.EXPERIMENT_DIR}/assets/read.png"
        self.read_rfid.setIcon(QtGui.QIcon(image_path))
        self.read_rfid.setStyleSheet(f"border-width:0px")
        self.read_rfid.setSizePolicy(SIZE_POLICY)
        self.read_rfid.setIconSize(QtCore.QSize(int(parent_widget.size().width()*.8), int(parent_widget.size().height()*.4)))
        self.read_rfid.clicked.connect(lambda do_it, arg="READ" :self.start_stop_experiment(arg))
        layout.addWidget(self.read_rfid,2,0,QtCore.Qt.AlignCenter)

        layout.setRowStretch(0,1)
        layout.setRowStretch(2,1)
       



    def write_values_to_experiment_file(self, action_type):
        #action_type: "WRITE", "READ"
        self.EXPERIMENT_VALUES["ACTION"]=action_type 

        if self.EXPERIMENT_VALUES["EXPERIMENT"] == "TEXT":
            self.EXPERIMENT_VALUES["CONTENT"]= self.custom_text_write.toPlainText()
        elif self.EXPERIMENT_VALUES["EXPERIMENT"] == "PERSON":
            self.EXPERIMENT_VALUES["CONTENT"]= [self.personal_first_write.text(), self.personal_last_write.text(), self.selected_image]
        else:
            self.EXPERIMENT_VALUES["CONTENT"]=""

        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)



    def start_stop_experiment(self, action_type):        
        if self.experiment_is_running == False:
            self.write_values_to_experiment_file(action_type)
            self.experiment_is_running = True

            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment(selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)
            self.Experiment_Thread.start()
            self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_LGREEN}")
            self.rfid_state_bt.setEnabled(True)

    
    def cancel_experiment(self):
        if self.experiment_is_running:
            self.experiment_is_running = False
            self.running_experiment.experiment.rfid_reader.READER.Close_MFRC522()
            del self.running_experiment.experiment
            self.update_ui(value_for_ui="state=-1")
            time.sleep(.5)
            self.update_ui(value_for_ui="state=0")
            self.rfid_state_bt.setEnabled(False)

   


    def update_ui(self, value_for_ui:str):
        try:
            if value_for_ui.startswith("state="):
                rfid_content = value_for_ui[6:]
            else:
                rfid_content = value_for_ui

            if rfid_content == "2":
                self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_LGREEN}")
                #self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['searching'])
                #self.rfid_state.setStyleSheet(f"background-color: rgb(255,255,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
                pass
            elif rfid_content == "1":
                self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_BLACK}")
                # self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['end'])
                # self.rfid_state.setStyleSheet(f"background-color: rgb(0,255,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
                pass
            elif rfid_content == "-1":
                self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_DARK_GREY}")
                # self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['cancelled'])
                # self.rfid_state.setStyleSheet(f"background-color: rgb(255,120,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
                pass
            elif rfid_content == "-2":
                self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_RED}")
                # self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['error'])
                # self.rfid_state.setStyleSheet(f"background-color: rgb(255,120,0); color:{FONT_COLOR_DARK}; border-radius:5px; padding 5px")
                pass
            elif rfid_content == "0":
                self.rfid_state_bt.setStyleSheet(f"background-color:{BACKGROUND_COLOR}")
                # self.rfid_state.setText(self.experiment_content["experiment"][self.language]['rfid_state']['idle'])
                # self.rfid_state.setStyleSheet(f"background-color: {FONT_COLOR_DARK}; color:{FONT_COLOR_LIGHT}; border-radius:5px; padding 5px")
                #self.running_experiment.experiment.stop()
                self.experiment_is_running = False
                self.Experiment_Thread.quit()
                self.rfid_state_bt.setEnabled(False)
                self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)



            else:
                if self.EXPERIMENT_VALUES["ACTION"]=="WRITE":
                    pass
                elif self.EXPERIMENT_VALUES["ACTION"]=="READ"and self.EXPERIMENT_VALUES["EXPERIMENT"]=="TEXT":
                    self.custom_text_read.setText(rfid_content)
                elif self.EXPERIMENT_VALUES["ACTION"]=="READ"and self.EXPERIMENT_VALUES["EXPERIMENT"]=="PERSON":
                    personal_data = ast.literal_eval(rfid_content)
                    self.personal_first_read.setText(personal_data[0])
                    self.personal_last_read.setText(personal_data[1])
                    pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/{self.experiment_information['experiment']['personal_images'][int(personal_data[2])]}")  
                    self.personal_image_read.setPixmap(pixmap.scaled(int(self.screen_size.width()*.1), int(self.screen_size.height()*.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(e)
            #self.running_experiment.experiment.stop()
            self.experiment_is_running = False
            self.Experiment_Thread.quit()
            self.rfid_state_bt.setEnabled(False)
            self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)



                  
