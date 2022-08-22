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
        if self.screen_size.width() <= THRESHOLD_SCREEN_WIDTH:
            self.SELECTED_FONT = BASIC_FONT_SMALL
            self.CUR_DISTANCE_FONT = QtGui.QFont('Arial', 32)
        else:
            self.SELECTED_FONT = BASIC_FONT_LARGE
            self.CUR_DISTANCE_FONT = QtGui.QFont('Arial', 48)

        experiment_information = json.load(open(os.path.join(self.EXPERIMENT_DIR,"experiment_information.json")))
        self.DEFAULT_VALUES={"SPEED_OF_SOUND":330,"FAR":20,"MID":14,"NEAR":8,"CLOSE":4,"FAR_HZ":1,"MID_HZ":2,"NEAR_HZ":4,"CLOSE_HZ":8}
        self.EXPERIMENT_VALUES=self.DEFAULT_VALUES.copy()

        self.set_experiment_header(experiment_name=experiment_information["experiment"][self.language]["name"], hyperlink=experiment_information["experiment"][self.language]["link"])
        self.fill_experiment_material(materials=experiment_information["material"][self.language][str(self.selected_system["system_id"])])
        self.fill_experiment_setup(image_dir=os.path.join(self.EXPERIMENT_DIR,"assets"),image_path=experiment_information["setup"][str(self.selected_system["system_id"])])
        self.fill_experiment_info(text=experiment_information["information"][self.language], file_paths=[f"{self.EXPERIMENT_DIR}/assets/{item}" for item in experiment_information['information']['files'][self.language]])
        self.fill_experiment(content=experiment_information["experiment"])


   

    def fill_experiment(self, content:dict):
        self.experiment_layout = self.tabs["experiment"]["layout"]
        # self.experiment_layout.setColumnStretch(0,1)
        # self.experiment_layout.setColumnStretch(1,1) 
        self.experiment_layout.setRowStretch(0,1)
        self.experiment_layout.setRowStretch(1,2)
        self.experiment_layout.setRowStretch(2,1)

        self.distance_visualization_frame = QtWidgets.QFrame()
        self.set_distance_visualization(parent_widget=self.distance_visualization_frame, content=content)
        self.distance_visualization_frame.setSizePolicy(SIZE_POLICY)
        self.experiment_layout.addWidget(self.distance_visualization_frame, 0, 0)
        
        self.default_distance_text = f"{content[self.language]['default_distance']}"
        self.distance_display = QtWidgets.QLabel(self.default_distance_text)
        self.distance_display.setAlignment(QtCore.Qt.AlignCenter)
        self.distance_display.setFont(self.CUR_DISTANCE_FONT)
        self.distance_display.setStyleSheet(f"color: {FONT_COLOR_LIGHT}")
        self.experiment_layout.addWidget(self.distance_display,2,0)


        self.start_experiment_button = QtWidgets.QToolButton()
        self.start_experiment_button.setAutoRaise(True)
        self.start_experiment_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.start_experiment_button.resize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2))
        self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/start_rec.png"))
        self.start_experiment_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.8), int(self.screen_size.height()*.2)))
        self.start_experiment_button.setStyleSheet(f"border-radius: 1px")
        self.start_experiment_button.setSizePolicy(SIZE_POLICY)
        self.start_experiment_button.clicked.connect(self.start_stop_experiment)
        self.experiment_layout.addWidget(self.start_experiment_button,3,0)

        self.car_distance_frame = QtWidgets.QFrame()
        self.set_car_distance_visualization(parent_widget=self.car_distance_frame, content=content)
        self.car_distance_frame.setSizePolicy(SIZE_POLICY)
        self.experiment_layout.addWidget(self.car_distance_frame, 1, 0)

        
        
             

    def set_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(layout)

        thresholds = ["FAR","MID","NEAR","CLOSE"]
        threshold_colours = [BACKGROUND_LGREEN, BACKGROUND_YELLOW,BACKGROUND_ORANGE,BACKGROUND_RED]
        self.bounds = []
        self.beeps = []
        for column, threshold in enumerate(thresholds):

            if not self.program_settings["has_keyboard"]:
                bound = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
            else:
                bound = QtWidgets.QLineEdit()
            bound.setMaxLength(10)
            bound.setAlignment(QtCore.Qt.AlignCenter)
            bound.setFont(self.SELECTED_FONT)
            bound.setPlaceholderText(f'{self.DEFAULT_VALUES[threshold]} cm')
            bound.setStyleSheet(f"background-color:{threshold_colours[column]} ; color:{FONT_COLOR_DARK}; border-radius: 5px;")
            bound.setValidator(QtGui.QIntValidator())
            self.bounds.append(bound)
            layout.addWidget(bound, 0, column+1, QtCore.Qt.AlignLeft)

            if not self.program_settings["has_keyboard"]:
                beeps = VKQLineEdit(name='value', mainWindowObj=self, validator="int")
            else:
                beeps = QtWidgets.QLineEdit()
            beeps.setMaxLength(10)
            beeps.setAlignment(QtCore.Qt.AlignCenter)
            beeps.setFont(self.SELECTED_FONT)
            selected_key=f"{threshold}_HZ"
            beeps.setPlaceholderText(f'{self.DEFAULT_VALUES[selected_key]} Hz')
            beeps.setStyleSheet(f"background-color:{threshold_colours[column]} ;color:{FONT_COLOR_DARK};  border-radius: 5px;")
            beeps.setValidator(QtGui.QIntValidator())
            self.beeps.append(beeps)
            layout.addWidget(beeps, 2, column+1, QtCore.Qt.AlignLeft)


        


        self.progressbar_distance = QtWidgets.QProgressBar()
        self.progressbar_distance.setMinimum(0)
        self.progressbar_distance.setMaximum(1000)
        self.progressbar_distance.setValue(0)
        self.progressbar_distance.setTextVisible(False)
        self.progressbar_distance.setSizePolicy(SIZE_POLICY)
        layout.addWidget(self.progressbar_distance, 1, 1,1,4)

        self.distance_stop = QtWidgets.QToolButton()
        self.distance_stop.setAutoRaise(True)
        self.distance_stop.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.distance_stop.resize(int(self.screen_size.width()*.2), int(self.screen_size.width()*.2))
        self.distance_stop.setIcon(QtGui.QIcon(f"{self.EXPERIMENT_DIR}/assets/go.png"))
        self.distance_stop.setIconSize(QtCore.QSize(int(self.screen_size.width()*.2), int(self.screen_size.height()*.2)))
        self.distance_stop.setStyleSheet(f"border-radius: 1px")
        self.distance_stop.setSizePolicy(SIZE_POLICY)
        layout.addWidget(self.distance_stop, 0, 5,3,1)   


        #Layout Stretching
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,3)
        layout.setRowStretch(2,1)

        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,1)
        layout.setColumnStretch(3,1)
        layout.setColumnStretch(4,1)
        layout.setColumnStretch(5,1)


    def update_progressbar(self, pb):
        far, far_colour = self.EXPERIMENT_VALUES["FAR"],BACKGROUND_LGREEN
        mid, mid_colour = self.EXPERIMENT_VALUES["MID"], BACKGROUND_YELLOW
        near, near_colour = self.EXPERIMENT_VALUES["NEAR"], BACKGROUND_ORANGE
        close, close_colour = self.EXPERIMENT_VALUES["CLOSE"], BACKGROUND_RED
        
        distance_value = self.distance/far
    

        if distance_value > 1:
            pb.setValue(0)
            return
        elif distance_value <= 1 and distance_value > mid/far:
            start_colour, stop_colour = far_colour, mid_colour

        elif distance_value <= mid/far and distance_value > near/far:
            start_colour, stop_colour = far_colour, mid_colour

        elif distance_value <= near/far and distance_value > close/far:
            start_colour, stop_colour = mid_colour, near_colour

        elif distance_value <= close/far and distance_value >= 0:
            start_colour, stop_colour = near_colour, close_colour

        else:
            return

        pb.setStyleSheet('QProgressBar::chunk {' +
                        'background-color: qlineargradient(spread:pad, x1:'+ str(0) + ', y1:0, x2:' + str(distance_value) + ', y2:0, ' + 
                        'stop: 0.5 ' + start_colour + ','
                        ' stop: 1 ' + stop_colour +
                        '); width: -1px; margin: -1px;}')
        pb.setValue((1-distance_value)*1000)

        icon = QtGui.QIcon(f"{self.EXPERIMENT_DIR}/assets/go.png") if self.distance >= close else QtGui.QIcon(f"{self.EXPERIMENT_DIR}/assets/stop.png")
        self.distance_stop.setIcon(QtGui.QIcon(icon))


           
    def set_car_distance_visualization(self, parent_widget:QtWidgets, content:dict):
        self.cars_layout = QtWidgets.QGridLayout()
        parent_widget.setLayout(self.cars_layout)
        self.moving_weight, self.space_weight, self.static_weight=1,4,1

        self.cars_layout.setColumnStretch(0,self.moving_weight)
        self.cars_layout.setColumnStretch(1,self.space_weight)
        self.cars_layout.setColumnStretch(2,self.static_weight)


        movable_object = QtWidgets.QLabel()
        movable_object.setSizePolicy(SIZE_POLICY)
        movable_object.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car.png")  
        movable_object.setPixmap(pixmap.scaled(int(self.screen_size.width()*.2),int(self.screen_size.height()*.2), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.cars_layout.addWidget(movable_object,0,0)


        static_object = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f"{self.EXPERIMENT_DIR}/assets/car_static.png")
        static_object.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        static_object.setPixmap(pixmap.scaled(int(self.screen_size.width()*.2),int(self.screen_size.height()*.2), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        static_object.setSizePolicy(SIZE_POLICY)

        self.cars_layout.addWidget(static_object,0,2)


    def update_object_distance(self, distance):
        moving_weight, space_weight, static_weight = 1,4,1#DEFAULT VALUES

        if distance > self.EXPERIMENT_VALUES["FAR"]:
            self.moving_weight=moving_weight
            self.space_weight=space_weight
            self.static_weight=static_weight
        else:
            factor = distance/self.EXPERIMENT_VALUES["FAR"]*100
            self.space_weight = int((space_weight+moving_weight)*factor)
            self.moving_weight = int((space_weight+moving_weight)*(100-factor))
            self.static_weight = int((self.moving_weight+self.space_weight)/6)


        self.cars_layout.setColumnStretch(0, self.moving_weight)
        self.cars_layout.setColumnStretch(1, self.space_weight)
        self.cars_layout.setColumnStretch(2, self.static_weight)

    def write_values_to_experiment_file(self):
        self.EXPERIMENT_VALUES["FAR"] = self.bounds[0].text() if self.bounds[0].text() != "" else self.DEFAULT_VALUES["FAR"]
        self.EXPERIMENT_VALUES["MID"] = self.bounds[1].text() if self.bounds[1].text() != "" else self.DEFAULT_VALUES["MID"]
        self.EXPERIMENT_VALUES["NEAR"] = self.bounds[2].text() if self.bounds[2].text() != "" else self.DEFAULT_VALUES["NEAR"] 
        self.EXPERIMENT_VALUES["CLOSE"] = self.bounds[3].text() if self.bounds[3].text() != "" else self.DEFAULT_VALUES["CLOSE"]

        self.EXPERIMENT_VALUES["FAR_HZ"] = self.beeps[0].text() if self.beeps[0].text() != "" else self.DEFAULT_VALUES["FAR_HZ"]
        self.EXPERIMENT_VALUES["MID_HZ"] = self.beeps[1].text() if self.beeps[1].text() != "" else self.DEFAULT_VALUES["MID_HZ"]
        self.EXPERIMENT_VALUES["NEAR_HZ"] = self.beeps[2].text() if self.beeps[2].text() != "" else self.DEFAULT_VALUES["NEAR_HZ"] 
        self.EXPERIMENT_VALUES["CLOSE_HZ"] = self.beeps[3].text() if self.beeps[3].text() != "" else self.DEFAULT_VALUES["CLOSE_HZ"]
        self.set_values(new_values = self.EXPERIMENT_VALUES, dir = self.EXPERIMENT_DIR)

    def start_stop_experiment(self):

        if self.experiment_is_running == False:
            self.write_values_to_experiment_file()
            self.experiment_is_running = True
            self.distance = self.EXPERIMENT_VALUES["FAR"]+1
            self.Experiment_Thread = QtCore.QThread()
            self.running_experiment = Running_Experiment(experiment_button=self.start_experiment_button, selected_system=self.selected_system, dir = self.EXPERIMENT_DIR, serial_read_freq_hz=10)            
            self.running_experiment.moveToThread(self.Experiment_Thread)
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.Experiment_Thread.started.connect(self.running_experiment.start_experiment)
            self.running_experiment.value_for_ui.connect(self.update_ui)
            self.Experiment_Thread.start()
            self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/stop_rec.png"))
            #self.update_object_distance(1)
            
        else:
            self.start_experiment_button.setEnabled(False)
            self.experiment_is_running = False
            self.running_experiment.experiment_is_running = self.experiment_is_running
            self.start_experiment_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/system/start_rec.png"))
            
            if self.selected_system["system_id"] == 0:
                self.running_experiment.experiment.stop()

            self.Experiment_Thread.exit()

            self.set_values(new_values = self.DEFAULT_VALUES, dir = self.EXPERIMENT_DIR)


   


    def update_ui(self, value_for_ui):
        #print(value_for_ui)
        try:
            value_pairs = value_for_ui.split(":")
            for pair in value_pairs:
                key, value = pair.split("=")
                if key == "d":
                    self.distance=float(value)
        except Exception as e:
            print(e)
            return
        self.distance_display.setText(f"{round(self.distance,2)} cm\n{self.default_distance_text}")
        self.update_progressbar(pb= self.progressbar_distance)
        self.update_object_distance(self.distance)





