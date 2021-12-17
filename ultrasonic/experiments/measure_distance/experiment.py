#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, json
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 


class Experiment(QFrame):

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
            print(v)

        self.layout.addWidget(tabs_widget)
        print(self.tabs)
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
        layout = self.tabs["experiment"]["layout"]
        
        medium_group=QGroupBox(content[self.language]['medium'])
        medium_layout=QVBoxLayout()
        for idx, (k, v) in enumerate(content[self.language]['speed'].items()):
            radio = QRadioButton(f"{k}(~{v} m/s")
            if idx == 0:
                radio.setChecked(True)
            medium_layout.addWidget(radio)

        custom_speed = QLineEdit()
        #custom_speed.text()
        medium_layout.addWidget(custom_speed)

        medium_group.setLayout(medium_layout)

        layout.addWidget(medium_group,0,0,3,2)


        formula = QLabel("THIS IS WHERE THE FORMULA WILL GO")
        interactive_formula = QLabel("THIS IS WHERE THE INTERACTIVE FORMULA WILL GO")

        layout.addWidget(formula,0,2)
        layout.addWidget(interactive_formula,1,2)

        start_experiment = QPushButton("START EXPERIMENT")
        layout.addWidget(start_experiment,2,2)


        #Widgets for Blue LED
        slider_blue = QSlider(Qt.Horizontal)
        slider_blue.setMinimum(0)
        slider_blue.setMaximum(10)
        slider_blue.setValue(3)
        slider_blue.setTickPosition(QSlider.TicksBelow)
        slider_blue.setTickInterval(1)
        label_blue = QLabel("Blau")
        label_blue_distance = QLabel(f"{slider_blue.value()} cm")

        layout.addWidget(label_blue,3,0)
        layout.addWidget(label_blue_distance,3,1)
        layout.addWidget(slider_blue,3,2)


        #Widgets for current distane
        current_distance = QProgressBar()
        current_distance.setMaximum(100)
        current_distance.setMinimum(0)
        current_distance.setValue(20)
        label_distance = QLabel(f"Aktuelle Distanz:\n{current_distance.value()} cm")
        layout.addWidget(current_distance,4,2,1,2)
        layout.addWidget(label_distance,4,0,1,2)

        #Widgets for Red LED
        slider_red = QSlider(Qt.Horizontal)
        slider_red.setMinimum(0)
        slider_red.setMaximum(10)
        slider_red.setValue(1)
        slider_red.setTickPosition(QSlider.TicksBelow)
        slider_red.setTickInterval(1)
        label_red = QLabel("Rot")
        label_red_distance = QLabel(f"{slider_red.value()} cm")

        layout.addWidget(label_red,5,0)
        layout.addWidget(label_red_distance,5,1)
        layout.addWidget(slider_red,5,2)



