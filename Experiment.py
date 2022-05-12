import os, json, math
from turtle import screensize
from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import OverViewButton, ScrollLabel

class ExperimentTemplate(QtWidgets.QWidget):

    BASIC_FONT_LARGE = QtGui.QFont('Arial', 22)
    BASIC_FONT_MEDIUM = QtGui.QFont('Arial', 16)
    BASIC_FONT_SMALL = QtGui.QFont('Arial', 12)
    BACKGROUND_COLOR = "rgb(62, 110, 145)"
    FONT_COLOR_LIGHT = "rgb(230, 230, 230)"
    FONT_COLOR_DARK = "rgb(80, 80, 80)"

    def __init__(self, root_dir, language, screen_size, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.ROOT_DIR = root_dir
        self.screen_size = screen_size
        self.language = language
        content_json= json.load(open(os.path.join(self.ROOT_DIR,"content.json")))
        self.sys_content = content_json["system"]
        
        self.MainWidget=QtWidgets.QWidget()
        self.MainWidget.setStyleSheet(f"background-color:{ExperimentTemplate.BACKGROUND_COLOR}")
        self.MainLayout=QtWidgets.QGridLayout(self.MainWidget)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.show_fullscreen()
        self.close_experiment = QtWidgets.QPushButton()
        self.close_experiment.setSizePolicy(self.sizePolicy)
        self.close_experiment.setFlat(True)
        self.close_experiment.setObjectName("close_experiment")
        self.close_experiment.setStyleSheet(f"background-color:rgb(100,100,100);border-radius:{int(self.screen_size.height()*.024)}px")
        image_path = f"{self.ROOT_DIR}/assets/system/close_experiment.png"
        self.close_experiment.setIcon(QtGui.QIcon(image_path))
        self.close_experiment.setIconSize(QtCore.QSize(int(self.screen_size.width()*.05), int(self.screen_size.height()*.05)))
        self.close_experiment.clicked.connect(self.close)

        self.header =QtWidgets.QLabel()
        self.header.setFont(self.BASIC_FONT_LARGE)
        self.header.setStyleSheet(f"color: {self.FONT_COLOR_LIGHT}")
        self.MainLayout.addWidget(self.close_experiment,0,0,1,1)
        self.MainLayout.addWidget(self.header,0,1,1,1)

        self.tabs_widget = QtWidgets.QTabWidget()
        self.tabs_widget.setStyleSheet("color:rgb(230,230,230);")
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
        if self.screen_size.width() <= 1024:
            self._material_rows, self._material_cols = 2,4
            layout.setColumnStretch(0, 1)
            layout.setColumnStretch(1, 1)
            layout.setColumnStretch(2, 1)
            layout.setColumnStretch(3, 1)
            #layout.setColumnStretch(4, 1)
            layout.setRowStretch(0, 1)
            layout.setRowStretch(1, 1)
            #layout.setRowStretch(2, 1)

        else:
            self._material_rows, self._material_cols = 3,5
            layout.setColumnStretch(0, 1)
            layout.setColumnStretch(1, 1)
            layout.setColumnStretch(2, 1)
            layout.setColumnStretch(3, 1)
            layout.setColumnStretch(4, 1)
            layout.setRowStretch(0, 1)
            layout.setRowStretch(1, 1)
            layout.setRowStretch(2, 1)

        self.material_buttons=[]
        for button_idx in range(self._material_rows*self._material_cols):
            material_button = OverViewButton(parent=tab_widget, screen_size=self.screen_size)
            material_button.setSizePolicy(self.sizePolicy)
            material_button.setAutoRaise(True)
            material_button.setObjectName(f"material_{button_idx}")
            material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/system/default.png")
            material_button.setButtonText(text=f"Test")
            self.material_buttons.append(material_button)
            layout.addWidget(material_button, int(button_idx/self._material_cols),int(button_idx%self._material_cols))



    def fill_experiment_material(self, materials:list=[]):
        self.last_visible_material_idx = 0
        self.materials = materials
        self.material_page = 1
        if len(self.materials) <= len(self.material_buttons):
            for idx, material_button in enumerate(self.material_buttons):
                try:
                    material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/parts/{self.materials[idx]['image']}")
                    button_text=self.materials[idx]["text"]
                    if "source" in self.materials[idx].keys():
                        button_text += f" [{self.materials[idx]['source']}]"
                    material_button.setButtonText(button_text)
                    material_button.setActive(True)
                    material_button.setEnabled(True)
                except IndexError as e:
                    material_button.setButtonIcon()
                    material_button.setButtonText()
                    material_button.setEnabled(False)
                    material_button.setActive(False)

        else:
            for idx, material_button in enumerate(self.material_buttons):
                if idx == self._material_rows*self._material_cols - 1:
                    break
                self.last_visible_material_idx = idx
                try:
                    material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/parts/{self.materials[idx]['image']}")
                    button_text=self.materials[idx]["text"]
                    if "source" in self.materials[idx].keys():
                        button_text += f" [{self.materials[idx]['source']}]"
                    material_button.setButtonText(button_text)
                    material_button.setActive(True)
                    material_button.setEnabled(True)
                except IndexError as e:
                    material_button.setButtonIcon()
                    material_button.setButtonText()
                    material_button.setEnabled(False)
                    material_button.setActive(False)

            self.next_material_button = self.material_buttons[-1]
            self.next_material_button.setActive(True)
            self.next_material_button.setEnabled(True)
            self.next_material_button.setStyleSheet("background-color:rgb(0,205,0); margin:10px; border-radius:10px;")
            self.next_material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/system/next.png")
            self.next_material_button.setButtonText(f"{self.sys_content['bt_material_page'][self.language]} {self.material_page}/{int(math.ceil(len(self.materials)/(len(self.material_buttons)-1)))}")
            self.next_material_button.clicked.connect(self.update_material_page)
            self.next_material_button.text.setStyleSheet("color:rgb(230,230,230);")
            self.next_material_button.icon_button.clicked.connect(self.update_material_page)
            

    def update_material_page(self):
        if self.material_page + 1 <= int(math.ceil(len(self.materials)/(len(self.material_buttons)-1))):
            self.material_page += 1
        else:
            self.material_page = 1
            self.last_visible_material_idx = -1
        self.next_material_button.setButtonText(f"{self.sys_content['bt_material_page'][self.language]} {self.material_page}/{int(math.ceil(len(self.materials)/(len(self.material_buttons)-1)))}")
        
        for idx, material_button in enumerate(self.material_buttons):
            if idx == self._material_rows*self._material_cols - 1:
                break
            self.last_visible_material_idx += 1
            try:
                material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/parts/{self.materials[self.last_visible_material_idx]['image']}")
                button_text=self.materials[self.last_visible_material_idx]["text"]
                if "source" in self.materials[self.last_visible_material_idx].keys():
                    button_text += f" [{self.materials[self.last_visible_material_idx]['source']}]"
                material_button.setButtonText(button_text)
                material_button.setActive(True)
                material_button.setEnabled(True)
            except IndexError as e:
                material_button.setButtonIcon()
                material_button.setButtonText()
                material_button.setEnabled(False)
                material_button.setActive(False)

            

    def fill_experiment_setup(self, image_dir, image_path:list=None):
        self.setup_page = 0
        tab_widget = self.tabs["setup"]["widget"]
        tab_widget.setStyleSheet(f"background-color:rgb(0,0,0)")
        layout = self.tabs["setup"]["layout"]
        layout.setColumnStretch(0,1)
        layout.setRowStretch(0,9)
        layout.setRowStretch(1,1)
        self.setup_image_paths = [os.path.join(image_dir,image) for image in image_path]
        image_path=self.setup_image_paths[0]

        if not image_path:
            image_path=os.path.join(self.ROOT_DIR, "assets/system/default.png")
            print("No Path specified")

        self.setup_image = QtWidgets.QToolButton()
        self.setup_image.setSizePolicy(self.sizePolicy)
        self.setup_image.setAutoRaise(True)
        self.setup_image.setIcon(QtGui.QIcon(image_path))
        self.setup_image.setIconSize(QtCore.QSize(int(self.screen_size.width()*.95), int(self.screen_size.height()*.75)))
        layout.addWidget(self.setup_image, 0,0)

        self.change_setup_image_button = QtWidgets.QPushButton()
        self.change_setup_image_button.setFont(self.BASIC_FONT_MEDIUM)
        self.change_setup_image_button.setText(f'[fritzing] - {self.sys_content["experiment_setup"]["complete_page"][self.language]}')
        self.change_setup_image_button.setStyleSheet(f"background-color: {self.FONT_COLOR_DARK}; color:{self.FONT_COLOR_LIGHT}; border-radius:5px; padding 5px")
        self.change_setup_image_button.setMinimumWidth(int(self.screen_size.width()*.8))
        layout.addWidget(self.change_setup_image_button,1,0, QtCore.Qt.AlignCenter)
        self.change_setup_image_button.clicked.connect(self.update_setup_image)
        

    def update_setup_image(self):
        if self.setup_page == len(self.setup_image_paths) - 1:
            self.setup_page = 0
            self.change_setup_image_button.setText(f'[fritzing] - {self.sys_content["experiment_setup"]["complete_page"][self.language]}')
        else:
            self.setup_page += 1
            self.change_setup_image_button.setText(f'[fritzing] - {self.sys_content["experiment_setup"]["step_page"][self.language]}   {self.setup_page}/{len(self.setup_image_paths)}')
        image_path = self.setup_image_paths[self.setup_page]
        self.setup_image.setIcon(QtGui.QIcon(image_path))


        


        

    def fill_experiment_info(self, text=[], file_path=None):
        if not file_path:
            file_path = f"{self.ROOT_DIR}/assets/system/default.png"

        tab_widget = self.tabs["information"]["widget"]
        layout = self.tabs["information"]["layout"]
        info_text = ScrollLabel(screen_size=self.screen_size)
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

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)

    def fill_experiment(self, content=None):
        pass

    def close(self):
        pass


    def show_fullscreen(self):
        self.MainWidget.showFullScreen()