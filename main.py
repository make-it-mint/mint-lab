import sys, os, git, json
from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import LanguageSelection, SystemSelection
from Settings import SettingsInterface
import pandas as pd
import importlib.util
from main_ui import *
from software_data.constants import *

class MainApp(object):
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    
    def __init__(self, screen_size):
        super().__init__()
        self._settings = json.load(open(os.path.join(MainApp.ROOT_DIR,"software_data/software_settings.json")))
        self._language = self._settings["selected_language"]
        self._selection_starting_idx = 0
        self._display_type = "topic" #Options: topic or experiment
        self._experiments = pd.DataFrame(json.load(open(os.path.join(MainApp.ROOT_DIR,"software_data/experiment_list.json"))))
        self._screen_size = screen_size
        self._current_listed_content = self._experiments.topic.drop_duplicates()

        if self._screen_size.width() <= 1024:
            self.basic_font = BASIC_FONT_MID
        else:
            self.basic_font = BASIC_FONT_LARGE



    def setup_ui(self, main_window):

        self.main_window, self.central_widget, self.central_widget_layout = setup_main_window(
            main_window=main_window,
            screen_size = self._screen_size
            )

        #Set logo
        self.logo = create_logo_widget(
            parent_layout=self.central_widget_layout,
            screen_size=self._screen_size,
            asset_dir=MainApp.ROOT_DIR)
        self.logo.clicked.connect(self._set_to_default)


        #Set Navigation Buttons in frame
        self.frame_nav, self.frame_nav_layout = create_nav_widgets(
            parent=self,
            parent_layout=self.central_widget_layout,
            screen_size=self._screen_size,
            asset_dir=MainApp.ROOT_DIR
            )


        #set interface buttons in frame
        self.frame_interface, self.frame_interface_layout = create_interface_widgets(
            parent=self,
            parent_layout=self.central_widget_layout,
            screen_size=self._screen_size,
            asset_dir=MainApp.ROOT_DIR,
            settings=self._settings,
            language=self._language,
            font=self.basic_font
            )



        #set topic widgets in frame
        self.frame_topics, self.frame_topics_layout, self._topic_buttons = create_topic_widgets(
            parent_widget=self.central_widget,
            parent_layout=self.central_widget_layout,
            screen_size=self._screen_size,
            asset_dir=MainApp.ROOT_DIR
            )

        main_window.setCentralWidget(self.central_widget)


    def _set_to_default(self):
        self._display_type="topic"
        self._selection_starting_idx = 0
        self._current_listed_content = self._experiments[self._experiments.systems.apply(lambda item: self._settings["selected_system"]["system_id"] in item )]
        self._current_listed_content = self._current_listed_content.topic.drop_duplicates()
        self._set_listed_content()


    def _previous_page(self):
        """move to previsou page"""
        if not self._selection_starting_idx == 0:
            self._set_listed_content(direction=-1)


    def _next_page(self):
        """move to next page"""
        self._set_listed_content(direction=1)


    def _show_easy_only(self, topic = None):
        """show easy experiments only"""
        #set to first page
        self._selection_starting_idx = 0
        self._current_listed_content = self._experiments[self._experiments.systems.apply(lambda item: self._settings["selected_system"]["system_id"] in item )]
        if self._display_type == "topic":
            pass
        elif self._display_type == "experiment":
            #check if already filtered for topic
            cur_topics = self._current_listed_content.topic.drop_duplicates()
            if len(cur_topics) == 1:
                self._current_listed_content = self._current_listed_content[self._experiments.topic == cur_topics[0]]
            

        self._current_listed_content = self._current_listed_content[self._current_listed_content.level <= 1]

        self._current_listed_content = self._current_listed_content.sort_values(by="level", ascending=True)
        self._display_type = "experiment"
        self._set_listed_content()
        

    def _show_topics(self):
        """display topics"""



    def translate_icons(self):
        self._set_listed_content()
        self.sort_topics.setText(f"{self._settings['bt_topic'][self._language]}")


    def _sort_new(self):
        """sort experimentes from new to old"""
        self._selection_starting_idx = 0
        self._current_listed_content = self._experiments[self._experiments.systems.apply(lambda item: self._settings["selected_system"]["system_id"] in item )]

        if self._display_type == "topic":
            pass
        elif self._display_type == "experiment":
            cur_topics = self._current_listed_content.topic.drop_duplicates()
            if len(cur_topics) == 1:
                self._current_listed_content = self._current_listed_content[self._experiments.topic == cur_topics[0]]
            else:
                pass

        self._current_listed_content = self._current_listed_content.sort_values(by="date-added", ascending=False)

        self._display_type = "experiment"
        self._set_listed_content()


    def _select_system(self):
        """Open Window to select system RPi/PicoPi/Arduino etc."""
        system_selection = SystemSelection(parent=self.main_window, systems = self._settings["systems"], root_dir=self.ROOT_DIR, cur_selected_sytem=self._settings["selected_system"])
        
        if system_selection.exec():
            self._settings["selected_system"] = system_selection.New_Selected_System
            #Reload all widgets according to selected system
            for system in self._settings["systems"].keys():
                if self._settings["systems"][system]["system_id"] == self._settings["selected_system"]["system_id"]:
                    image_path = f"{MainApp.ROOT_DIR}/assets/system/{system}.png"
                    break
            self.system_selection.setIcon(QtGui.QIcon(image_path))
            self._set_to_default()
            self._overwrite_settings_file()
        else:
            pass


    def _open_settings(self, version = -1):
        """Default version (-1) updates to latest version"""
        settings_window = SettingsInterface(root_dir=self.ROOT_DIR, settings=self._settings, parent=self.main_window)
        if settings_window.exec():
            self._settings["has_keyboard"] = int(settings_window.has_keyboard)
            self._settings["selected_language"]=settings_window.selected_language
            self._language = self._settings["selected_language"]
            self.translate_icons()
            self._overwrite_settings_file()


    def _set_listed_content(self, direction=0):
        
        content = self._current_listed_content
        content = content.reset_index(drop=True)
        num_displays = len(self._topic_buttons)
        self._selection_starting_idx += (num_displays*direction)

        if self._selection_starting_idx < 0:
            self._selection_starting_idx = len(content) - len(content)%num_displays
        elif self._selection_starting_idx >= len(content):
            self._selection_starting_idx = 0

        if self._display_type == "topic":
            self.sort_topics.setText(f"{self._settings['bt_topic'][self._language]}")
        elif self._display_type == "experiment":
            if len(pd.unique(content.topic)) == 1:
                self.sort_topics.setText(f"{self._settings['topics'][pd.unique(content.topic)[0]][self._language]}")
            else:
                self.sort_topics.setText(f"{self._settings['bt_topic'][self._language]}")

        for counter, display in enumerate(self._topic_buttons):
            
            try:
                if self._display_type == "topic":
                    topic = content[self._selection_starting_idx + counter]
                    display.setButtonText(self._settings["topics"][topic][self._language])
                    image_path = f"{MainApp.ROOT_DIR}/assets/topics/{topic}.png"
                    display.setButtonIcon(image_path)
                    display.disconnect()
                    display.setActive(True)
                    display.clicked.connect(lambda do_it, arg=topic :self._show_experiments_of_topic(arg))

                elif self._display_type == "experiment":
                    topic = self._settings["topics"][list(content.topic)[self._selection_starting_idx + counter]][self._language]
                    level = self._settings["levels"][self._language][list(content.level)[self._selection_starting_idx + counter]]
                    name = list(content.name)[self._selection_starting_idx + counter][self._language]
                    display.setButtonText(f"{name}\n----------\n{level}")
                        
                    if os.path.exists(f"{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}/assets/experiment_icon.png"):
                        image_path = f"{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}/assets/experiment_icon.png"
                    else:
                        image_path = f"{MainApp.ROOT_DIR}/assets/system/default.png"

                    experiment_directory = f"""{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}"""
                    spec = importlib.util.spec_from_file_location("module.name", f"{experiment_directory}/experiment_ui.py")
                    
                    display.setButtonIcon(image_path)

                    display.disconnect()
                    display.setActive(True)
                    display.clicked.connect(lambda start_it, arg=spec :self._start_experiment(arg))
                else:
                    print("Wrong display type selected, should be topic or experiment")
                    break

                display.setEnabled(True)
            except Exception as e:
                display.setButtonIcon()
                display.setButtonText()
                display.setEnabled(False)
                display.setActive(False)

    def _show_experiments_of_topic(self, topic):
        self._selection_starting_idx = 0
        self._display_type = "experiment"
        self._current_listed_content = self._experiments[self._experiments.topic == topic]
        self._set_listed_content()

    def _start_experiment(self, spec):
        experiment_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(experiment_module)
        experiment_module.Experiment(root_dir= MainApp.ROOT_DIR, parent = self.main_window, language=self._language, screen_size=self._screen_size, program_settings=self._settings)



    def _overwrite_settings_file(self):
        with open(f'{self.ROOT_DIR}/software_data/software_settings.json', 'w', encoding='utf-8') as f:
            json.dump(self._settings, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_ui = MainApp(screen_size = app.primaryScreen().size())
    main_ui.setup_ui(main_window)
    main_ui._set_to_default()
    
    sys.exit(app.exec())