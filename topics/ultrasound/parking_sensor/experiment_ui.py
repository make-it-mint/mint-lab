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
        self.DEFAULT_VALUES={"SPEED_OF_SOUND":330,"FAR":20,"MID":14,"NEAR":8,"CLOSE":4,"FAR_HZ":1,"MID_HZ":2,"NEAR_HZ":4,"CLOSE_HZ":8}#MUST use double quotation marks
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=experiment_information["experiment"][self.language]["name"], hyperlink=experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=experiment_information["information"][self.language], file_paths=[f"{self.EXPERIMENT_DIR}/assets/{item}" for item in experiment_information['information']['files'][self.language]])
        self.fill_experiment(content=experiment_information["experiment"])


   

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        self.experiment_layout.setColumnStretch(0,1)
        self.experiment_layout.setColumnStretch(1,1) 
        self.experiment_layout.setRowStretch(0,3)
        self.experiment_layout.setRowStretch(1,3)
        self.experiment_layout.setRowStretch(2,4)

        self.distance_visualization_frame = QtWidgets.QFrame()
        self.set_distance_visualization(parent_widget=self.distance_visualization_frame, content=content)
        self.distance_visualization_frame.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.experiment_layout.addWidget(self.distance_visualization_frame, 0, 0, 1, 2)
        

        self.distance_display = QtWidgets.QLabel(content[self.language]["default_distance"])
        self.distance_display.setAlignment(QtCore.Qt.AlignCenter)
        self.distance_display.setFont(self.CUR_DISTANCE_FONT)
        self.distance_display.setStyleSheet(f"color: {FONT_COLOR_LIGHT}")
        self.experiment_layout.addWidget(self.distance_display,1,0)

        self.start_experiment_button = QtWidgets.QPushButton(self.program_settings["start_experiment"][self.language])
        self.start_experiment_button.setFont(self.CUR_DISTANCE_FONT)
        self.start_experiment_button.setStyleSheet(f"color: {FONT_COLOR_DARK}; background-color: rgb(0,255,0); margin: 10px 20px 10px 20px; border-radius: 10px")
        self.start_experiment_button.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,1,1)

        self.car_distance_frame = QtWidgets.QFrame()
        self.set_car_distance_visualization(parent_widget=self.car_distance_frame, content=content)
        self.car_distance_frame.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred
             )
        self.experiment_layout.addWidget(self.car_distance_frame, 2, 0, 1, 2)

        
        
             

    def set_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        ###################
        #ROW 0 - Distances#
        ###################
        if not self.program_settings["has_keyboard"]:
            self.bound_far = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.bound_far = QtWidgets.QLineEdit()
        self.bound_far.setMaxLength(10)
        self.bound_far.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_far.setFont(self.SELECTED_FONT)
        self.bound_far.setPlaceholderText(f'{content[self.language]["colour_legend"]["far"]}: 20 cm')
        self.bound_far.setStyleSheet("background-color: rgb(0,255,0); border-radius: 5px;")
        self.bound_far.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.bound_far, 0, 2, QtCore.Qt.AlignLeft)

        #################
        if not self.program_settings["has_keyboard"]:
            self.bound_far_mid = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.bound_far_mid = QtWidgets.QLineEdit()
        self.bound_far_mid.setMaxLength(10)
        self.bound_far_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_far_mid.setFont(self.SELECTED_FONT)
        self.bound_far_mid.setPlaceholderText(f'{content[self.language]["colour_legend"]["mid"]}: 14 cm')
        self.bound_far_mid.setStyleSheet("background-color: rgb(255,255,0); border-radius: 5px;")
        self.bound_far_mid.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.bound_far_mid, 0, 4, QtCore.Qt.AlignLeft)



        #################
        if not self.program_settings["has_keyboard"]:
            self.bound_mid_near = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.bound_mid_near = QtWidgets.QLineEdit()
        self.bound_mid_near.setMaxLength(10)
        self.bound_mid_near.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_mid_near.setFont(self.SELECTED_FONT)
        self.bound_mid_near.setPlaceholderText(f'{content[self.language]["colour_legend"]["near"]}: 8 cm')
        self.bound_mid_near.setStyleSheet("background-color: rgb(255,165,0); border-radius: 5px;")
        self.bound_mid_near.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.bound_mid_near, 0, 6, QtCore.Qt.AlignLeft)

        #################
        if not self.program_settings["has_keyboard"]:
            self.bound_near_close = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.bound_near_close = QtWidgets.QLineEdit()
        self.bound_near_close.setMaxLength(10)
        self.bound_near_close.setAlignment(QtCore.Qt.AlignCenter)
        self.bound_near_close.setFont(self.SELECTED_FONT)
        self.bound_near_close.setPlaceholderText(f'{content[self.language]["colour_legend"]["close"]}: 4 cm')
        self.bound_near_close.setStyleSheet("background-color: rgb(255,48,48); border-radius: 5px;")
        self.bound_near_close.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.bound_near_close, 0, 8, QtCore.Qt.AlignLeft)


        ######################
        #ROW 1 - Progressbar #
        ######################
        self.distance_colour = QtWidgets.QLabel()
        self.distance_colour.setStyleSheet(
            """
            background-color: rgb(0,255,0);
            border-radius: 10px;
            margin: 10px 10px 10px 10px;
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
        self.distance_stop.setPixmap(pixmap.scaled(200,100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        # self.distance_stop.setStyleSheet(
        #     """
        #     background-color: rgb(255,0,0);
        #     border-radius: 10px;
        #     """)
        layout.addWidget(self.distance_stop, 1, 10)     


        #############################
        #ROW 2 - Beeping Frequencies#
        #############################
        if not self.program_settings["has_keyboard"]:
            self.beep_far = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.beep_far = QtWidgets.QLineEdit()
        self.beep_far.setMaxLength(10)
        self.beep_far.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_far.setFont(self.SELECTED_FONT)
        self.beep_far.setPlaceholderText(f'{content[self.language]["colour_legend"]["far"]}: 1 Hz')
        self.beep_far.setStyleSheet("background-color: rgb(0,255,0); border-radius: 5px;")
        self.beep_far.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.beep_far, 2, 2, QtCore.Qt.AlignLeft)


        #################
        if not self.program_settings["has_keyboard"]:
            self.beep_far_mid = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.beep_far_mid = QtWidgets.QLineEdit()
        self.beep_far_mid.setMaxLength(10)
        self.beep_far_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_far_mid.setFont(self.SELECTED_FONT)
        self.beep_far_mid.setPlaceholderText(f'{content[self.language]["colour_legend"]["mid"]}: 2 Hz')
        self.beep_far_mid.setStyleSheet("background-color: rgb(255,255,0); border-radius: 5px;")
        self.beep_far_mid.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.beep_far_mid, 2, 4, QtCore.Qt.AlignLeft)

        #################
        if not self.program_settings["has_keyboard"]:
            self.beep_mid_near = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.beep_mid_near = QtWidgets.QLineEdit()
        self.beep_mid_near.setMaxLength(10)
        self.beep_mid_near.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_mid_near.setFont(self.SELECTED_FONT)
        self.beep_mid_near.setPlaceholderText(f'{content[self.language]["colour_legend"]["near"]}: 4 Hz')
        self.beep_mid_near.setStyleSheet("background-color: rgb(255,165,0); border-radius: 5px;")
        self.beep_mid_near.setValidator(QtGui.QIntValidator())
        layout.addWidget(self.beep_mid_near, 2, 6, QtCore.Qt.AlignLeft)


        #################
        if not self.program_settings["has_keyboard"]:
            self.beep_near_close = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
        else:
            self.beep_near_close = QtWidgets.QLineEdit()
        self.beep_near_close.setMaxLength(10)
        self.beep_near_close.setAlignment(QtCore.Qt.AlignCenter)
        self.beep_near_close.setFont(self.SELECTED_FONT)
        self.beep_near_close.setPlaceholderText(f'{content[self.language]["colour_legend"]["close"]}: 8 Hz')
        self.beep_near_close.setStyleSheet("background-color: rgb(255,48,48); border-radius: 5px;")
        self.beep_near_close.setValidator(QtGui.QIntValidator())
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
            margin: 10px 10px 10px 10px;
            """)
        elif distance_value <= mid/far and distance_value > near/far:
            start_colour, stop_colour = far_colour, mid_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {mid_colour};
            border-radius: 10px;
            margin: 10px 10px 10px 10px;
            """)
        elif distance_value <= near/far and distance_value > close/far:
            start_colour, stop_colour = mid_colour, near_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {near_colour};
            border-radius: 10px;
            margin: 10px 10px 10px 10px;
            """)
        elif distance_value <= close/far and distance_value >= 0:
            start_colour, stop_colour = near_colour, close_colour
            self.distance_colour.setStyleSheet(
            f"""
            background-color: {close_colour};
            border-radius: 10px;
            margin: 10px 10px 10px 10px;
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
        self.distance_stop.setPixmap(pixmap.scaled(int(self.screen_size.width()*.2),int(self.screen_size.height()*.2), QtCore.Qt.AspectRatioMode.KeepAspectRatio))


           
    def set_car_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        self.max_distance = 964
        self.default_movable_object_weight = 41
        self.complete_layout_weight = 1185
        self.movable_object_layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(self.movable_object_layout )

        movable_object = QtWidgets.QLabel()
        movable_object.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred,
             )
        movable_object.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car.png")  
        movable_object.setPixmap(pixmap.scaled(int(self.screen_size.width()*.2),int(self.screen_size.height()*.2), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.movable_object_layout.addWidget(movable_object,0,0)

        space = QtWidgets.QLabel()
        space.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred,
             )

        self.movable_object_layout.addWidget(space,0,1)


        static_object = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car_static.png")
        static_object.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        static_object.setPixmap(pixmap.scaled(int(self.screen_size.width()*.2),int(self.screen_size.height()*.2), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        static_object.setSizePolicy(
                 QtWidgets.QSizePolicy.Policy.Preferred,
                 QtWidgets.QSizePolicy.Policy.Preferred,
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

    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["FAR"] = self.bound_far.text() if self.bound_far.text() != "" else self.DEFAULT_VALUES["FAR"]
        self.EXPERIMENT_VALUES["MID"] = self.bound_far_mid.text() if self.bound_far_mid.text() != "" else self.DEFAULT_VALUES["MID"]
        self.EXPERIMENT_VALUES["NEAR"] = self.bound_mid_near.text() if self.bound_mid_near.text() != "" else self.DEFAULT_VALUES["NEAR"] 
        self.EXPERIMENT_VALUES["CLOSE"] = self.bound_near_close.text() if self.bound_near_close.text() != "" else self.DEFAULT_VALUES["CLOSE"]

        self.EXPERIMENT_VALUES["FAR_HZ"] = self.beep_far.text() if self.beep_far.text() != "" else self.DEFAULT_VALUES["FAR_HZ"]
        self.EXPERIMENT_VALUES["MID_HZ"] = self.beep_far_mid.text() if self.beep_far_mid.text() != "" else self.DEFAULT_VALUES["MID_HZ"]
        self.EXPERIMENT_VALUES["NEAR_HZ"] = self.beep_mid_near.text() if self.beep_mid_near.text() != "" else self.DEFAULT_VALUES["NEAR_HZ"] 
        self.EXPERIMENT_VALUES["CLOSE_NZ"] = self.beep_near_close.text() if self.beep_near_close.text() != "" else self.DEFAULT_VALUES["CLOSE_HZ"]
        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)

    def start_stop_experiment(self):

        if not self.experiment_is_running:

            self.write_values_to_experiment_file()
            self.experiment_is_running = True
            self.start_experiment_button.setStyleSheet(f"color: {FONT_COLOR_LIGHT}; background-color: rgb(239,0,0); margin: 10px 20px 10px 20px; border-radius: 10px")
            self.start_experiment_button.setText(self.program_settings["stop_experiment"][self.language])
            self.Experiment_Thread = QtCore.QThread()
            

            self.running_experiment = Running_Experiment(selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)
            self.Experiment_Thread.start()
            
        else:
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            if self.selected_system["system_id"] == 0:
                self.running_experiment.experiment.stop()
            self.Experiment_Thread.exit()
            self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)


   


    def update_ui(self, value_for_ui):
        distance = value_for_ui
        self.distance_display.setText(f"{distance:3.3f} cm")
        self.update_progressbar(pb= self.progressbar_distance, distance=distance)
        self.update_object_distance(distance)





