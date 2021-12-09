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

        self.layout.addWidget(tabs_widget)
        print(self.tabs)
        self.fill_experiment_setup(content=experiment_content["setup"])
        self.fill_experiment_info(content=experiment_content["information"])


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
        



