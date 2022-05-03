import sys, os, git, json
from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import TopicButton
from LanguageSelection import LanguageSelection
import pandas as pd
import importlib.util

class MainApp(object):
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASIC_FONT = QtGui.QFont('Arial', 28)
    BACKGROUND_COLOR = "rgb(62, 110, 145)"
    INTERFACE_BUTTON_UNSELECTED_SS = f"background-color:{BACKGROUND_COLOR}; padding-left: 20px; border: 5px solid rgb(52, 100, 135);\nborder-radius: 30px;"
    INTERFACE_BUTTON_SELECTED_SS = f"background-color:rgb(200,50,100); padding-left: 20px; border: 5px solid rgb(0, 0, 0);\nborder-radius: 30px;"
    
    def __init__(self, language, screen_size):
        super().__init__()
        self._language = language
        self._selection_starting_idx = 0
        self._display_type = "topic" #Options: topic or experiment
        self._topic_rows = 2
        self._topic_cols = 2
        content_json= json.load(open(os.path.join(MainApp.ROOT_DIR,"content.json")))
        self._sys_content = content_json["system"]
        self._experiments = pd.DataFrame(content_json["experiment_list"])
        self._screen_size = screen_size
        self._current_listed_content = self._experiments.topic.drop_duplicates()
        if self._screen_size.width() <= 1024:
            MainApp.BASIC_FONT = QtGui.QFont('Arial', 18)

        print(self._screen_size)

    def setupUi(self, MainWindow):
        self.main = MainWindow
        MainWindow.setObjectName("MainWindow")
        
        
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sizePolicy.setHorizontalStretch(1)
        self.sizePolicy.setVerticalStretch(1)
        self.sizePolicyPref = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

        MainWindow.setSizePolicy(self.sizePolicy)
        MainWindow.setStyleSheet(f"background-color:{MainApp.BACKGROUND_COLOR}")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.German, QtCore.QLocale.Country.Germany))

        #Set Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setSizePolicy(self.sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        #Set Central Widget Layout
        self.centralwidget_layout = QtWidgets.QGridLayout(self.centralwidget)
        

        MainWindow.resize(self._screen_size)
        self.centralwidget_layout.setColumnStretch(0, 1)
        self.centralwidget_layout.setColumnStretch(1, 4)
        self.centralwidget_layout.setRowStretch(0, 4)
        self.centralwidget_layout.setRowStretch(1, 1)
        self.centralwidget_layout.setRowStretch(2, 10)

        #Set logo
        self.logo = QtWidgets.QToolButton()
        self.logo.setSizePolicy(self.sizePolicy)
        self.logo.setAutoRaise(True)
        self.logo.setObjectName("logo")
        self.centralwidget_layout.addWidget(self.logo,0,0,1,1)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/logo.png"
        self.logo.setIcon(QtGui.QIcon(image_path))
        self.logo.setIconSize(QtCore.QSize(int(self._screen_size.width()/4.5), int(self._screen_size.height()*4.5/30)))
        self.logo.clicked.connect(self._set_to_default)
        #self.logo.setStyleSheet("background-color:rgb(0,0,0)")

        #Set Navigation Buttons in frame
        self.frame_nav = QtWidgets.QFrame()
        self.frame_nav_layout = QtWidgets.QHBoxLayout(self.frame_nav)
        self.frame_nav.resize(int(self._screen_size.width()/4), int(self._screen_size.height()*2/16))
        self.navigation_widgets(self.frame_nav_layout, self.frame_nav.size())
        self.centralwidget_layout.addWidget(self.frame_nav,1,0,1,1)
        #self.frame_nav.setStyleSheet("background-color:rgb(255,0,0)")

        #set interface buttons in frame
        self.frame_interface = QtWidgets.QFrame()
        self.frame_interface_layout = QtWidgets.QVBoxLayout(self.frame_interface)
        self.frame_interface.resize(int(self._screen_size.width()/4), int(self._screen_size.height()*5.5/16))
        self.interface_widgets(self.frame_interface_layout, self.frame_interface.size())
        self.centralwidget_layout.addWidget(self.frame_interface,2,0,1,1)
        #self.frame_interface.setStyleSheet("background-color:rgb(0,255,0)") 

        #set system widgets in frame
        self.frame_system = QtWidgets.QFrame()
        self.frame_system_layout = QtWidgets.QHBoxLayout(self.frame_system)
        self.frame_system.resize(int(self._screen_size.width()/4), int(self._screen_size.height()*1.5/16))
        self.system_widgets(self.frame_system_layout, self.frame_system.size())
        self.centralwidget_layout.addWidget(self.frame_system,3,0,1,1)
        #self.frame_system.setStyleSheet("background-color:rgb(0,0,255)")   

        #set topic widgets in frame
        self.frame_topics = QtWidgets.QFrame()
        self.frame_topics_layout = QtWidgets.QGridLayout(self.frame_topics)
        self.frame_interface.resize(int(self._screen_size.width()*3/4), int(self._screen_size.height()))
        self.topic_widgets(self.frame_topics_layout, self.frame_topics.size())
        self.centralwidget_layout.addWidget(self.frame_topics,0,1,4,1)
        #self.frame_topics.setStyleSheet("background-color:rgb(0,0,255)")     

        
        MainWindow.setCentralWidget(self.centralwidget)
               
        #self._set_to_default()
        #MainWindow.showFullScreen()

        

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.additionalActions()


    def _set_to_default(self):
        self._display_type="topic"
        self._selection_starting_idx = 0
        self._current_listed_content = self._experiments.topic.drop_duplicates()
        self._set_listed_content()

    def navigation_widgets(self, layout, parent_size):
        #Previous Button
        item_width = int(parent_size.width()/3)
        #layout.setContentsMargins(0, 0, 0, 0)
        self.previous = QtWidgets.QPushButton()
        self.previous.setSizePolicy(self.sizePolicy)
        self.previous.setFlat(True)
        self.previous.setObjectName("previous")
        self.previous.setStyleSheet(
            f"""
            margin-right: 0;
            background-color:rgb(255, 186, 0);
            border: solid 3px rgb(0,0,0);
            border-top-left-radius: {int(parent_size.height()/2)}px;
            border-bottom-left-radius: {int(parent_size.height()/2)}px;""")
        layout.addWidget(self.previous)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/previous.png"
        self.previous.setIcon(QtGui.QIcon(image_path))
        self.previous.setIconSize(QtCore.QSize(item_width, parent_size.height()))
        self.previous.clicked.connect(self._previous_page)

        #Next Button
        self.next = QtWidgets.QPushButton()
        self.next.setSizePolicy(self.sizePolicy)
        self.next.setFlat(True)
        self.next.setObjectName("next")
        self.next.setStyleSheet(
            f"""
            margin-left: 0;
            background-color:rgb(0, 220, 0);
            border: solid 3px rgb(0,0,0);
            border-top-right-radius: {int(parent_size.height()/2)}px;
            border-bottom-right-radius: {int(parent_size.height()/2)}px;
            """)
        layout.addWidget(self.next)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/next.png"
        self.next.setIcon(QtGui.QIcon(image_path))
        self.next.setIconSize(QtCore.QSize(item_width, parent_size.height()))
        self.next.clicked.connect(self._next_page)


    def _previous_page(self):
        """move to previsou page"""
        self._set_listed_content(direction=-1)

    def _next_page(self):
        """move to next page"""
        self._set_listed_content(direction=1)


    def interface_widgets(self, layout, parent_size):
        num_items = 4
        
        #Sort TOPICS Button
        self.sort_topics = QtWidgets.QToolButton()
        self.sort_topics.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.sort_topics.setSizePolicy(self.sizePolicy)
        self.sort_topics.setAutoRaise(True)
        self.sort_topics.setObjectName("sort_topics")
        self.sort_topics.setText(f"   {self._sys_content['bt_topic'][self._language]}")
        self.sort_topics.setFont(MainApp.BASIC_FONT)
        self.sort_topics.setStyleSheet(MainApp.INTERFACE_BUTTON_SELECTED_SS)
        layout.addWidget(self.sort_topics)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/all_topics.png"
        self.sort_topics.setIcon(QtGui.QIcon(image_path))
        self.sort_topics.setIconSize(QtCore.QSize(int(parent_size.width()/3), int(parent_size.height()/num_items)))
        self.sort_topics.clicked.connect(self._show_topics)

        #Sort Newest EXPERIMENTS Button
        self.sort_new = QtWidgets.QToolButton()
        self.sort_new.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.sort_new.setSizePolicy(self.sizePolicy)
        self.sort_new.setAutoRaise(True)
        self.sort_new.setObjectName("sort_new")
        self.sort_new.setText(f"   {self._sys_content['bt_sort_new'][self._language]}")
        self.sort_new.setFont(MainApp.BASIC_FONT)
        self.sort_new.setStyleSheet(MainApp.INTERFACE_BUTTON_UNSELECTED_SS)
        layout.addWidget(self.sort_new)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/new.png"
        self.sort_new.setIcon(QtGui.QIcon(image_path))
        self.sort_new.setIconSize(QtCore.QSize(int(parent_size.width()/3), int(parent_size.height()/num_items)))
        self.sort_new.clicked.connect(self._sort_new)

        #Sort and show only lowest level experiments
        self.show_beginner = QtWidgets.QToolButton()
        self.show_beginner.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.show_beginner.setSizePolicy(self.sizePolicy)
        self.show_beginner.setAutoRaise(True)
        self.show_beginner.setObjectName("show_beginner")
        self.show_beginner.setText(f"   {self._sys_content['bt_show_beginner'][self._language]}")
        self.show_beginner.setFont(MainApp.BASIC_FONT)
        self.show_beginner.setStyleSheet(MainApp.INTERFACE_BUTTON_UNSELECTED_SS)
        layout.addWidget(self.show_beginner)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/easy_experiments.png"
        self.show_beginner.setIcon(QtGui.QIcon(image_path))
        self.show_beginner.setIconSize(QtCore.QSize(int(parent_size.width()/3), int(parent_size.height()/num_items)))
        self.show_beginner.clicked.connect(self._show_easy_only)

        #Select Language
        self.select_language = QtWidgets.QToolButton()
        self.select_language.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.select_language.setSizePolicy(self.sizePolicy)
        self.select_language.setAutoRaise(True)
        self.select_language.setObjectName("show_language")
        self.select_language.setText(f"   {self._sys_content['languages'][self._language]['name']}")
        self.select_language.setFont(MainApp.BASIC_FONT)
        self.select_language.setStyleSheet(MainApp.INTERFACE_BUTTON_UNSELECTED_SS)
        layout.addWidget(self.select_language)
        image_path = f"{MainApp.ROOT_DIR}/assets/languages/{self._sys_content['languages'][self._language]['icon']}"
        self.select_language.setIcon(QtGui.QIcon(image_path))
        self.select_language.setIconSize(QtCore.QSize(int(parent_size.width()/5), int(parent_size.height()/num_items)))
        self.select_language.clicked.connect(self._select_language)


    def _show_easy_only(self, topic = None):
        """show easy experiments only"""
        #set to first page
        self._selection_starting_idx = 0
        if self._display_type == "topic":
            self._current_listed_content = self._experiments[self._experiments.level <= 1]
        elif self._display_type == "experiment":
            #check if already filtered for topic
            cur_topics = self._current_listed_content.topic.drop_duplicates()
            if len(cur_topics) == 1:
                self._current_listed_content = self._experiments[self._experiments.topic == cur_topics[0]]
            else:
                self._current_listed_content = self._experiments

            self._current_listed_content = self._current_listed_content[self._current_listed_content.level <= 1]

        self._current_listed_content = self._current_listed_content.sort_values(by="level", ascending=True)
        self._display_type = "experiment"
        self._set_listed_content()
        
    def _show_topics(self):
        """display topics"""
        #print("Now displaying topics")

    def _select_language(self):
        """select language and change content of displayed items"""
        #open new window
        language_selection = LanguageSelection(parent=self.main, languages = self._sys_content["languages"], root_dir=self.ROOT_DIR, cur_language=self._language)
        if language_selection.exec():
            #Reload all widgets with new language
            self._language = language_selection.Selected_Language
            self.translate_icons()

    def translate_icons(self):
        self._set_listed_content()
        self.sort_new.setText(f"   {self._sys_content['bt_sort_new'][self._language]}")
        self.show_beginner.setText(f"   {self._sys_content['bt_show_beginner'][self._language]}")
        self.select_language.setText(f"   {self._sys_content['languages'][self._language]['name']}")
        self.select_language.setIcon(QtGui.QIcon(f"{MainApp.ROOT_DIR}/assets/languages/{self._sys_content['languages'][self._language]['icon']}"))



    def _sort_new(self):
        """sort experimentes from new to old"""
        self._selection_starting_idx = 0
        if self._display_type == "topic":
            self._current_listed_content = self._experiments.sort_values(by="date-added", ascending=False)
        elif self._display_type == "experiment":
            cur_topics = self._current_listed_content.topic.drop_duplicates()
            if len(cur_topics) == 1:
                self._current_listed_content = self._experiments[self._experiments.topic == cur_topics[0]]
            else:
                self._current_listed_content = self._experiments

            self._current_listed_content = self._current_listed_content.sort_values(by="date-added", ascending=False)

        self._display_type = "experiment"
        self._set_listed_content()

    def system_widgets(self, layout, parent_size):
        #Close Software
        item_width = int(parent_size.width()/4)
        self.close_software = QtWidgets.QPushButton()
        self.close_software.setSizePolicy(self.sizePolicy)
        self.close_software.setFlat(True)
        self.close_software.setObjectName("close_software")
        self.close_software.setStyleSheet("")
        layout.addWidget(self.close_software)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/exit.png"
        self.close_software.setIcon(QtGui.QIcon(image_path))
        self.close_software.setIconSize(QtCore.QSize(item_width, int(parent_size.height())))
        self.close_software.clicked.connect(self.main.close)

        #Info
        self.info = QtWidgets.QPushButton()
        self.info.setSizePolicy(self.sizePolicy)
        self.info.setFlat(True)
        self.info.setObjectName("info")
        self.info.setStyleSheet("padding-bottom:10px")
        layout.addWidget(self.info)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/info.png"
        self.info.setIcon(QtGui.QIcon(image_path))
        self.info.setIconSize(QtCore.QSize(item_width, int(parent_size.height())))
        self.info.clicked.connect(self._show_info)

        #Update Software
        self.update_software = QtWidgets.QPushButton()
        self.update_software.setSizePolicy(self.sizePolicy)
        self.update_software.setFlat(True)
        self.update_software.setObjectName("update_software")
        self.update_software.setStyleSheet("")
        layout.addWidget(self.update_software)
        image_path = f"{MainApp.ROOT_DIR}/assets/system/update.png"
        self.update_software.setIcon(QtGui.QIcon(image_path))
        self.update_software.setIconSize(QtCore.QSize(item_width, int(parent_size.height())))
        self.update_software.clicked.connect(self._update_software)

    def _show_info(self):
        """Open Window to show software info, and allow manual selection of Software Version (git tags)"""
        print("Opening Info Window")

    def _update_software(self, version = -1):
        """Default version (-1) updates to latest version"""
        print("Now Updating...")

    def topic_widgets(self, layout, parent_size):
        self._topic_buttons = []

        for button_idx in range((self._topic_rows*self._topic_cols)):
            button = TopicButton(parent=self.centralwidget, parent_size=parent_size)
            button.setSizePolicy(self.sizePolicy)
            button.setAutoRaise(True)
            button.setObjectName(f"topic_{button_idx}")
            button.setText("")
            image_path = f"{MainApp.ROOT_DIR}/assets/system/default.png"
            button.setButtonIcon(image_path=image_path)
            layout.addWidget(button,int(button_idx/self._topic_cols),int(button_idx%self._topic_cols),1,1)
            self._topic_buttons.append(button)
        

    def _set_listed_content(self, direction=0):
        
        content = self._current_listed_content
        num_displays = len(self._topic_buttons)
        self._selection_starting_idx += (num_displays*direction)

        if self._selection_starting_idx < 0:
            self._selection_starting_idx = len(content) - len(content)%num_displays
        elif self._selection_starting_idx >= len(content):
            self._selection_starting_idx = 0

        if self._display_type == "topic":
            self.sort_topics.setText(f"   {self._sys_content['bt_topic'][self._language]}")
        elif self._display_type == "experiment":
            if len(pd.unique(content.topic)) == 1:
                self.sort_topics.setText(f"   {self._sys_content['topics'][pd.unique(content.topic)[0]][self._language]}")
            else:
                self.sort_topics.setText(f"   {self._sys_content['bt_topic'][self._language]}")

        for counter, display in enumerate(self._topic_buttons):
            
            try:
                if self._display_type == "topic":
                    topic = content[self._selection_starting_idx + counter]
                    display.setButtonText(self._sys_content["topics"][topic][self._language])
                    image_path = f"{MainApp.ROOT_DIR}/assets/topics/{topic}.png"
                    display.setButtonIcon(image_path)
                    display.disconnect()
                    display.setActive(True)
                    display.clicked.connect(lambda do_it, arg=topic :self._show_experiments_of_topic(arg))

                elif self._display_type == "experiment":
                    topic = self._sys_content["topics"][list(content.topic)[self._selection_starting_idx + counter]][self._language]
                    level = self._sys_content["levels"][self._language][list(content.level)[self._selection_starting_idx + counter]]
                    name = list(content.name)[self._selection_starting_idx + counter][self._language]
                    display.setButtonText(f"{name}\n----------\n{level}")
                        
                    if os.path.exists(f"{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}/assets/experiment_icon.png"):
                        image_path = f"{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}/assets/experiment_icon.png"
                    else:
                        image_path = f"{MainApp.ROOT_DIR}/assets/system/default.png"

                    experiment_directory = f"""{MainApp.ROOT_DIR}/topics/{list(content.topic)[self._selection_starting_idx + counter]}/{list(content.directory)[self._selection_starting_idx + counter]}"""
                    spec = importlib.util.spec_from_file_location("module.name", f"{experiment_directory}/experiment.py")
                    
                    try:
                        display.setButtonIcon(image_path)
                    except:
                        display.setButtonIcon(f"{MainApp.ROOT_DIR}/assets/system/default.png")
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
        experiment_module.Experiment(root_dir= MainApp.ROOT_DIR, parent = self.main, language=self._language, screen_size=self._screen_size)

    def additionalActions(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_ui = MainApp(language = 'de', screen_size = app.primaryScreen().size())
    main_ui.setupUi(main_window)
    main_ui._set_to_default()
    main_window.showFullScreen()
    
    sys.exit(app.exec())