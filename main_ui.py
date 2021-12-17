#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 16:33:00 2021


@author: felix
"""

import sys
import os
import math
import git
import json
import experiment_list_item as item
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 



class MainApp(QMainWindow):
    
    DEF_FONT = 'Helvetica 18'
    FONT_B = 'Helvetica 18 bold'
    FONT_L = 'Helvetica 32'
    REPO_PATH = os.path.dirname(os.path.abspath(__file__))
    
    
    
    def __init__(self, parent = None, name = 'main', columns = 3, language = 'de'):
        super().__init__(parent)
        self._widgets = {}
        self._language = language
        self._sys_content = json.load(open(f"{self.REPO_PATH}/sys_language.json"))[self._language]
        self._name = name
        self._projects = json.load(open(f"{self.REPO_PATH}/projects.json"))
        self._main_menu = self._setup_root()
        self._num_col = columns
        
        self.create_main_ui()
        self._create_menubar()

    
    def _create_menubar(self):
        menu_bar = self.menuBar()
        self.setMenuBar(menu_bar)
        file_menu = QMenu("&File", self)
        file_menu.addAction("Beenden", self.exit_app)
        menu_bar.addMenu(file_menu)

        update_menu = QMenu("&Update", self)
        update_menu.addAction("Update Repo", self._update_repo)
        update_menu.addAction("Update Betriebssystem",self.update_os)
        menu_bar.addMenu(update_menu)

    def exit_app(self):
        self.close()
        print("Beenden")


    def update_os(self):
        print("Update OS")

    
    def _setup_root(self):
        self.centralWidget = QFrame()
        self.setCentralWidget(self.centralWidget)
        #self._experiment_list_root_view = QGridLayout(self.centralWidget).
        self.central_layout = QGridLayout(self.centralWidget)


        #Root View For Experiment List
        self.experiment_list_frame = QFrame()
        self._experiment_list_layout = QGridLayout(self.experiment_list_frame)
        self.central_layout.addWidget(self.experiment_list_frame,0,0)


        #Root View For Main Menu
        self.menu_frame = QFrame()
        self._menu_layout = QGridLayout(self.menu_frame)
        self.central_layout.addWidget(self.menu_frame,0,1)

        #Root View For Experiment
        self.experiment_frame = QFrame()
        self._experiment_layout = QGridLayout(self.experiment_frame)
        self.central_layout.addWidget(self.experiment_frame,0,2)

        self.experiment_list_frame.hide()
        self.experiment_frame.hide()
        
        self.setWindowTitle('Basic Grid Layout')
        self.showFullScreen()
        self._widgets.update({
            'windows':{
                'central':{'widget':self.centralWidget,'layout':self.central_layout},
                 'menu':{'widget':self.menu_frame, 'layout':self._menu_layout},
                 'experiment_list':{'widget':self.experiment_list_frame, 'layout':self._experiment_list_layout},
                 'experiment':{'widget':self.experiment_frame, 'layout':self._experiment_layout}
                 }
        })
        
    def create_main_ui(self):

        for idx, project in enumerate(self._projects.keys()):
            row = math.floor(idx/self._num_col)*2
            col = int(idx % self._num_col)

            label = QLabel(self._projects[project]['name'][self._language])
            label.setFont(QFont("Helvetica", 24, QFont.Normal, italic=False))

            button = QToolButton()
            #button.setToolButtonStyle(Qt.ToolButtonIconOnly)

            image_path = f"{self.REPO_PATH}/{project}/project_logo.png"
            button.setIcon(QIcon(image_path))
            
            button.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Expanding,
            )
            button.setIconSize(QSize(button.size().width()-100, button.size().height()-40))
            button.setStyleSheet(
                f"""
                background-color: {self._projects[project]['colour']};
                border-radius: 20px;
                """)
            button.clicked.connect(lambda checked, arg= project: self._open_experiment_list(arg))

            self._menu_layout.addWidget(label, row, col, alignment=Qt.AlignCenter)
            self._menu_layout.addWidget(button, row+1, col)
            self._widgets.update({'button':{project: {'name':button, 'img': image_path}}})
            #self._menu_layout.setRowStretch(row,1)
        

    
    
    def _update_repo(self, tag_idx=-1):
        #old_tag
        repo = git.Repo(self.REPO_PATH)
        current_tag = repo.git.describe('--tags')
        repo.git.checkout('main')
        repo.remotes.origin.pull()
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        selected_tag = tags[tag_idx]
        if not current_tag==str(selected_tag):
            print(f"Changed from Version: {current_tag} to new Version: {selected_tag}")
            repo.git.checkout(str(selected_tag))
        else:
            print(f"Already checked out Version: {selected_tag}")    
        
    def _open_experiment_list(self, experiment_type):
        #try:
        self.menu_frame.hide()
        self.experiment_list_frame.show()
        self.show_experiment_list(path=f"{self.REPO_PATH}/{experiment_type}")
        # except Exception as e:
        #     print(e)
        #     #messagebox.showinfo("Achtung","Keine Daten verfügbar")
        #     return

        
    def show_experiment_list(self, path):
        self.current_list_frame = QFrame()
        self.current_list_layout = QGridLayout(self.current_list_frame)
        self._experiment_list_layout.addWidget(self.current_list_frame,0,0)

        experiments = json.load(open(f"{path}/experiments.json"))["experiments"]
        num_rows = 0
        num_columns = 3
        for idx, experiment in enumerate(experiments):
            num_rows += 1
            row = int(math.floor(idx/num_columns))
            column = int(idx % num_columns)
            experiment_name = experiment[self._language]["name"]
            experiment_description = experiment[self._language]["description"]
            experiment_path = f"{path}/{experiment['path']}"

            experiment = item.ExperimentOverview(
                experiment = experiment_name,
                description=experiment_description,
                experiment_path=experiment_path,
                language=self._language,
                windows=self._widgets['windows'],
                )

            self.current_list_layout.addWidget(experiment, row, column)

        for row in range(num_rows + 1):
            if row < num_rows:
                self.current_list_layout.setRowStretch(row,0)
            else:
                self.current_list_layout.setRowStretch(row,1)

        for column in range(num_columns):
            self.current_list_layout.setColumnStretch(column,1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = MainApp(language='de')
    windowExample.show()
    sys.exit(app.exec_())
                             