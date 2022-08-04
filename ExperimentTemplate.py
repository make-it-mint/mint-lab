import os, time, math, multiprocessing, serial
from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import OverViewButton, ScrollLabel
from VirtualKeyboard import Keyboard
import importlib.util
from software_data.constants import *

class UI_Template(QtWidgets.QWidget):

    

    def __init__(self, root_dir, language, screen_size, parent=None, program_settings=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.experiment_is_running = False
        self.program_settings = program_settings

        self.selected_system = self.program_settings["selected_system"]
        self.ROOT_DIR = root_dir
        self.screen_size = screen_size
        self.language = language
        
        self.MainWidget=QtWidgets.QWidget()
        self.MainWidget.setStyleSheet(f"background-color:{BACKGROUND_COLOR}; color:{FONT_COLOR_LIGHT};")
        self.MainLayout=QtWidgets.QGridLayout(self.MainWidget)

        self.show_fullscreen()
        

        self._set_header_widgets()
        self._set_experiment_tab_widgets()


        
        self._create_experiment_material_layout()


        self.MainWidget.resize(self.screen_size)

        if not self.program_settings["has_keyboard"]:
            self.initiate_keyboard()

        self.MainLayout.setColumnStretch(0, 1)
        self.MainLayout.setColumnStretch(1, 17)
        self.MainLayout.setRowStretch(0, 1)
        self.MainLayout.setRowStretch(1, 17)

    def initiate_keyboard(self):
        self.keyboard = Keyboard(language = self.language, screen_size = self.screen_size, parent=self.MainWidget)

    def _set_experiment_tab_widgets(self):
        self.tabs_widget = QtWidgets.QTabWidget()
        self.tabs_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)

        self.tabs={}
        for k,v in self.program_settings["experiment_tabs"][self.language].items():
            current_tab = QtWidgets.QFrame()
            current_layout = QtWidgets.QGridLayout(current_tab)
            self.tabs_widget.addTab(current_tab ,v)
            self.tabs.update({k:{"widget":current_tab,"layout":current_layout}})


        self.MainLayout.addWidget(self.tabs_widget,1,0,1,3)

    def _set_header_widgets(self):
        image_path = f"{self.ROOT_DIR}/assets/system/close_experiment.png"
        self.close_experiment = QtWidgets.QPushButton()
        self.close_experiment.setSizePolicy(SIZE_POLICY)
        self.close_experiment.setFlat(True)
        self.close_experiment.setStyleSheet(f"background-color:{BACKGROUND_GREY};border-radius:{int(self.screen_size.height()*.024)}px")
        self.close_experiment.setIcon(QtGui.QIcon(image_path))
        self.close_experiment.setIconSize(QtCore.QSize(int(self.screen_size.width()*.05), int(self.screen_size.height()*.05)))
        self.close_experiment.clicked.connect(self.close)

        self.header =QtWidgets.QLabel()
        self.header.setFont(BASIC_FONT_LARGE)
        self.header.setStyleSheet(f"color: {FONT_COLOR_LIGHT}")
        

        self.header_button =QtWidgets.QLabel()
        self.header_button.setFont(BASIC_FONT_LARGE)

        self.header_button.setStyleSheet(f"background-color:{BACKGROUND_LGREEN};border-radius:{int(self.screen_size.height()*.024)}px; padding:10px 0 10px 0;")

        self.MainLayout.addWidget(self.close_experiment,0,0,1,1)
        self.MainLayout.addWidget(self.header,0,1,1,1)
        self.MainLayout.addWidget(self.header_button,0,2,1,1)

    
    def set_experiment_header(self, experiment_name, hyperlink):
        self.header.setText(experiment_name)
        
        if hyperlink == "":
            self.header_button.setVisible(False)
            return
        self.header_button.setText(f"<a style='text-decoration:none;color:white'href='{hyperlink}'>{self.program_settings['show_details'][self.language]}</a>")
        self.header_button.setTextFormat(QtCore.Qt.RichText)
        self.header_button.setOpenExternalLinks(True)


    def _create_experiment_material_layout(self):
        tab_widget = self.tabs["material"]["widget"]
        layout = self.tabs["material"]["layout"]
        if self.screen_size.width() <= 1024:
            self._material_rows, self._material_cols = 2,4
        else:
            self._material_rows, self._material_cols = 3,5

        for row in range(self._material_rows):
            layout.setRowStretch(row, 1)
        for col in range(self._material_cols):
            layout.setColumnStretch(col, 1)


        self.material_buttons=[]
        for button_idx in range(self._material_rows*self._material_cols):
            material_button = OverViewButton(parent=tab_widget, screen_size=self.screen_size)
            material_button.setSizePolicy(SIZE_POLICY)
            material_button.setAutoRaise(True)
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
            self.next_material_button.setStyleSheet(f"background-color:{BACKGROUND_LGREEN}; margin:10px; border-radius:10px;")
            self.next_material_button.setButtonIcon(image_path=f"{self.ROOT_DIR}/assets/system/next.png")
            self.next_material_button.setButtonText(f"{self.program_settings['bt_material_page'][self.language]} {self.material_page}/{int(math.ceil(len(self.materials)/(len(self.material_buttons)-1)))}")
            self.next_material_button.clicked.connect(self.update_material_page)
            self.next_material_button.text.setStyleSheet(f"color:rgb(230,230,230{BACKGROUND_WHITE};")
            self.next_material_button.icon_button.clicked.connect(self.update_material_page)
            

    def update_material_page(self):
        if self.material_page + 1 <= int(math.ceil(len(self.materials)/(len(self.material_buttons)-1))):
            self.material_page += 1
        else:
            self.material_page = 1
            self.last_visible_material_idx = -1
        self.next_material_button.setButtonText(f"{self.program_settings['bt_material_page'][self.language]} {self.material_page}/{int(math.ceil(len(self.materials)/(len(self.material_buttons)-1)))}")
        
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
        tab_widget.setStyleSheet(f"background-color:{BACKGROUND_BLACK}")
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
        self.setup_image.setSizePolicy(SIZE_POLICY)
        self.setup_image.setAutoRaise(True)
        self.setup_image.setIcon(QtGui.QIcon(image_path))
        self.setup_image.setIconSize(QtCore.QSize(int(self.screen_size.width()*.95), int(self.screen_size.height()*.75)))
        layout.addWidget(self.setup_image, 0,0)

        self.change_setup_image_button = QtWidgets.QPushButton()
        self.change_setup_image_button.setFont(BASIC_FONT_MID)
        self.change_setup_image_button.setText(f'[fritzing] - {self.program_settings["experiment_setup"]["complete_page"][self.language]}')
        self.change_setup_image_button.setStyleSheet(f"background-color: {FONT_COLOR_DARK}; color:{FONT_COLOR_LIGHT}; border-radius:5px; padding 5px")
        self.change_setup_image_button.setMinimumWidth(int(self.screen_size.width()*.8))
        layout.addWidget(self.change_setup_image_button,1,0, QtCore.Qt.AlignCenter)
        self.change_setup_image_button.clicked.connect(self.update_setup_image)
        

    def update_setup_image(self):
        if self.setup_page == len(self.setup_image_paths) - 1:
            self.setup_page = 0
            self.change_setup_image_button.setText(f'[fritzing] - {self.program_settings["experiment_setup"]["complete_page"][self.language]}')
        else:
            self.setup_page += 1
            self.change_setup_image_button.setText(f'[fritzing] - {self.program_settings["experiment_setup"]["step_page"][self.language]}   {self.setup_page}/{len(self.setup_image_paths)}')
        image_path = self.setup_image_paths[self.setup_page]
        self.setup_image.setIcon(QtGui.QIcon(image_path))


        
    def set_values(self, dir, new_values):
        if self.selected_system["system_id"] == 0:
            filename = f"{dir}/experiment_code/rpi.py"
        elif self.selected_system["system_id"] == 1:
            filename = f"{dir}/experiment_code/picopi.py"
        elif self.selected_system["system_id"] == 2:
            filename = f"{dir}/experiment_code/experiment_code.ino"

        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()

        new_lines={}
        for key, value in new_values.items():
            for line_idx,line in enumerate(data):
                if key in line:
                    if self.selected_system["system_id"] == 2:
                        new_text = f'{line[:line.find(key)]}{key}={value};\n'
                    else:
                        new_text = f'{line[:line.find(key)]}{key}={value}\n'
                    new_lines.update({line_idx:new_text})
                    break

        for replace_line, replace_str in new_lines.items():
            data[replace_line]= replace_str


        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(data)

        

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
        if self.experiment_is_running:
            QtWidgets.QMessageBox.warning(self.MainWidget,"",self.program_settings["close_experiment_warning"][self.language])
        else:
            self.MainWidget.close() 


    def show_fullscreen(self):
        self.MainWidget.showFullScreen()








class Running_Experiment(QtCore.QObject):
    value_for_ui = QtCore.pyqtSignal(str)
    experiment_is_running = True

    def __init__(self, selected_system, dir, serial_read_freq_hz:int = 1, timeout=5):
        super().__init__()
        self.selected_system = selected_system
        self.dir = dir
        self.serial_read_freq = serial_read_freq_hz
        self.timeout = timeout
        

    def start_experiment(self):
        if self.selected_system["system_id"] == 0:
            spec = importlib.util.spec_from_file_location("module.name", f'{self.dir}/experiment_code/rpi.py')
            experiment_module_rpi = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(experiment_module_rpi)
            self.experiment = experiment_module_rpi.Experiment(self.experiment_is_running, self.value_for_ui)
            self.experiment.run()        
                
        elif self.selected_system["system_id"] == 1:

            experiment = multiprocessing.Process(target=self.run_picopi)
            try:
                experiment.start()
                time.sleep(1.5)
                ser = serial.Serial(port=self.selected_system["comport"],baudrate=9600, timeout=self.timeout)
                ser.flushInput()
                while self.experiment_is_running:
                    self.value_for_ui.emit(ser.readline().decode("utf-8"))
                    time.sleep(1/self.serial_read_freq)
                #print("Experiment Stopped by Button")
                experiment.terminate()
                os.system(f'ampy --port {self.selected_system["comport"]} reset')
            except Exception or KeyboardInterrupt as e:
                print(e)
                experiment.terminate()
                os.system(f'ampy --port {self.selected_system["comport"]} reset')

    def run_picopi(self):
        #print(f'ampy --port {self.selected_system["comport"]} run {self.dir[self.dir.rfind("topics"):]}/experiment_code/picopi.py')
        os.system(f'ampy --port {self.selected_system["comport"]} run {self.dir[self.dir.rfind("topics"):]}/experiment_code/picopi.py')
