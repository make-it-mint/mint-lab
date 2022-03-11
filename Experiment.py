import os, json
from PyQt6 import QtCore, QtGui, QtWidgets

class ExperimentTemplate(QtWidgets.QWidget):

    BASIC_FONT = QtGui.QFont('Arial', 22)
    BACKGROUND_COLOR = "rgb(62, 110, 145)"

    def __init__(self, root_dir, language, screen_size, parent=None):
        super().__init__(parent=parent)
        self.ROOT_DIR = root_dir
        self.screen_size = screen_size
        self.language = language
        content_json= json.load(open(os.path.join(self.ROOT_DIR,"content.json")))
        self.sys_content = content_json["system"]
        
        self.MainWidget=QtWidgets.QWidget()
        self.MainWidget.setStyleSheet(f"background-color:{ExperimentTemplate.BACKGROUND_COLOR}")
        self.MainLayout=QtWidgets.QGridLayout(self.MainWidget)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.close_experiment = QtWidgets.QPushButton()
        self.close_experiment.setSizePolicy(self.sizePolicy)
        self.close_experiment.setFlat(True)
        self.close_experiment.setObjectName("close_experiment")
        self.close_experiment.setStyleSheet(f"background-color:rgb(100,100,100);border-radius:{int(self.screen_size.height()*.024)}px")
        image_path = f"{self.ROOT_DIR}/assets/close_experiment.png"
        self.close_experiment.setIcon(QtGui.QIcon(image_path))
        self.close_experiment.setIconSize(QtCore.QSize(int(self.screen_size.width()*.05), int(self.screen_size.height()*.05)))
        self.close_experiment.clicked.connect(self.close)

        self.header =QtWidgets.QLabel("DUMMY")
        self.header.setFont(self.BASIC_FONT)

        self.MainLayout.addWidget(self.close_experiment,0,0,1,1)
        self.MainLayout.addWidget(self.header,0,1,1,1)

        self.tabs_widget = QtWidgets.QTabWidget()
        self.tabs_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)

        self.tabs={}
        for k,v in self.sys_content["experiment_tabs"][self.language].items():
            current_tab = QtWidgets.QFrame()
            current_layout = QtWidgets.QGridLayout(current_tab)
            self.tabs_widget.addTab(current_tab ,v)
            self.tabs.update({k:{"widget":current_tab,"layout":current_layout}})


        self.MainLayout.addWidget(self.tabs_widget,1,0,1,2)
        self.create_experiment_material_layout()


        self.MainWidget.resize(self.screen_size)
        self.MainLayout.setColumnStretch(0, 1)
        self.MainLayout.setColumnStretch(1, 19)
        self.MainLayout.setRowStretch(0, 1)
        self.MainLayout.setRowStretch(1, 17)


    def create_experiment_material_layout(self):
        tab_widget = self.tabs["material"]["widget"]
        layout = self.tabs["material"]["layout"]
        rows, cols = 3,5
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

        self.material_buttons=[]
        for button_idx in range(rows*cols):
            material_button = QtWidgets.QToolButton()
            material_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            material_button.setSizePolicy(self.sizePolicy)
            material_button.setAutoRaise(True)
            material_button.setEnabled(False)
            material_button.setObjectName(f"material_{button_idx}")
            material_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/default.png"))
            material_button.setStyleSheet(f"background-color:rgb(255,255,255); border: 2px solid black; margin:10px; padding-top: 20px; border-radius:10px")
            material_button.setIconSize(QtCore.QSize(int(self.screen_size.width()*.15), int(self.screen_size.height()*.20)))
            self.material_buttons.append(material_button)
            layout.addWidget(material_button, int(button_idx/cols),int(button_idx%cols))



    def fill_experiment_material(self, materials:list=[]):
        
        if len(materials) <= len(self.material_buttons):
            for idx, material_button in enumerate(self.material_buttons):
                try:
                    material_button.setIcon(QtGui.QIcon(f"{self.ROOT_DIR}/assets/parts/{materials[idx]['image']}"))
                    button_text=materials[idx]["text"]
                    if "source" in materials[idx].keys():
                        button_text += f"\n[{materials[idx]['source']}]"
                    material_button.setText(button_text)
                    material_button.setStyleSheet(f"background-color:rgb(255,255,255); border: 2px solid black; margin:10px; padding-top: 20px; border-radius:20px")
                    material_button.setEnabled(True)
                except IndexError as e:
                    material_button.setIcon(QtGui.QIcon())
                    material_button.setText("")
                    material_button.setEnabled(False)
                    material_button.setStyleSheet(f"")


            

    def fill_experiment_setup(self, image_path:str=None):
        tab_widget = self.tabs["setup"]["widget"]
        tab_widget.setStyleSheet(f"background-color:rgb(0,0,0)")
        layout = self.tabs["setup"]["layout"]
        layout.setColumnStretch(0,1)
        layout.setRowStretch(0,0)
        
        if not image_path:
            image_path=os.path.join(self.ROOT_DIR, "assets/default.png")
            print("No Path specified")


        
        
        setup = QtWidgets.QToolButton()
        setup.setSizePolicy(self.sizePolicy)
        setup.setAutoRaise(True)
        setup.setObjectName("setup_image")
        setup.setIcon(QtGui.QIcon(image_path))
        setup.setIconSize(QtCore.QSize(int(self.screen_size.width()*.97), int(self.screen_size.height()*.85)))
        layout.addWidget(setup, 0,0)

    def fill_experiment_info(self, text=[], file_path=None):
        if not file_path:
            file_path = f"{self.ROOT_DIR}/assets/default.png"

        tab_widget = self.tabs["information"]["widget"]
        layout = self.tabs["information"]["layout"]
        info_text = QtWidgets.QLabel()
        info_text.setWordWrap(True)
        info_text.setFont(self.BASIC_FONT)
        layout.addWidget(info_text, 0, 0)

        info = ""
        for idx, item in enumerate(text):
            info += item
            if idx < len(text)-1:
                info += f"\n\n"

        info_text.setText(info)

        movie_label = QtWidgets.QLabel()
        movie = QtGui.QMovie(file_path)
        movie_label.setMovie(movie)
        layout.addWidget(movie_label, 0, 1)
        movie.start()

    def fill_experiment(self, content=None):
        pass

    def close(self):
        pass


    def show_fullscreen(self):
        self.MainWidget.showFullScreen()