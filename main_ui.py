from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import TopicButton
from software_data.constants import *
import math

def setup_main_window(main_window, screen_size):
    
    main_window.setStyleSheet(f"background-color:{BACKGROUND_COLOR}")
    main_window.setLocale(QtCore.QLocale(QtCore.QLocale.Language.German, QtCore.QLocale.Country.Germany))
    #Set Central Widget
    central_widget = QtWidgets.QWidget(main_window)
    central_widget.setSizePolicy(SIZE_POLICY)
    
    #Set Central Widget Layout
    central_widget_layout = QtWidgets.QGridLayout(central_widget)


    main_window.resize(screen_size)
    central_widget_layout.setColumnStretch(0, 1)
    central_widget_layout.setColumnStretch(1, 4)
    central_widget_layout.setRowStretch(0, 3)
    central_widget_layout.setRowStretch(1, 3)
    central_widget_layout.setRowStretch(2, 14)
    main_window.showFullScreen()

    return main_window, central_widget, central_widget_layout


def create_logo_widget(parent_layout, screen_size, asset_dir):
    logo = QtWidgets.QToolButton()
    logo.setSizePolicy(SIZE_POLICY)
    logo.setAutoRaise(True)
    parent_layout.addWidget(logo,0,0,1,1)
    image_path = f"{asset_dir}/assets/system/logo.png"
    logo.setIcon(QtGui.QIcon(image_path))
    logo.setIconSize(QtCore.QSize(int(screen_size.width()*.2), int(screen_size.height()*.1)))
    return logo


def create_nav_widgets(parent, parent_layout, screen_size, asset_dir):

    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QHBoxLayout(frame)
    frame.resize(int(screen_size.width()/4), int(screen_size.height()*2/16))
    parent_layout.addWidget(frame,1,0,1,1)

    item_width = int(frame.size().width()/2.5)


    parent.bt_previous = QtWidgets.QPushButton()
    parent.bt_previous.setSizePolicy(SIZE_POLICY)
    parent.bt_previous.setFlat(True)
    frame_layout.addWidget(parent.bt_previous)
    image_path = f"{asset_dir}/assets/system/previous.png"
    parent.bt_previous.setIcon(QtGui.QIcon(image_path))
    parent.bt_previous.setIconSize(QtCore.QSize(item_width, frame.size().height()))

    parent.bt_next = QtWidgets.QPushButton()
    parent.bt_next.setSizePolicy(SIZE_POLICY)
    parent.bt_next.setFlat(True)
    frame_layout.addWidget(parent.bt_next)
    image_path = f"{asset_dir}/assets/system/next.png"
    parent.bt_next.setIcon(QtGui.QIcon(image_path))
    parent.bt_next.setIconSize(QtCore.QSize(item_width, frame.size().height()))

    parent.bt_previous.clicked.connect(parent._previous_page)
    parent.bt_next.clicked.connect(parent._next_page)

    return frame, frame_layout


def create_interface_widgets(parent, parent_layout, screen_size, asset_dir, settings, language, font):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QGridLayout(frame)
    frame.resize(int(screen_size.width()/4), int(screen_size.height()*5.5/16))
    parent_layout.addWidget(frame,2,0,1,1)

    frame_layout.setRowStretch(0, 2)
    frame_layout.setRowStretch(1, 6)
    frame_layout.setRowStretch(2, 2)
    frame_layout.setRowStretch(3, 5)
    frame_layout.setRowStretch(4, 5)

    parent.sort_topics = QtWidgets.QToolButton()
    parent.sort_topics.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
    parent.sort_topics.setSizePolicy(SIZE_POLICY)
    parent.sort_topics.setAutoRaise(True)
    parent.sort_topics.setText(f"{settings['bt_topic'][language]}")
    parent.sort_topics.setStyleSheet(INTERFACE_BUTTON_SELECTED)
    parent.sort_topics.setFont(font)
    frame_layout.addWidget(parent.sort_topics,0,0,1,2)

    images=['system/new','system/beginner', 'system/settings','system/exit'] 
    widget_positions=[[1,0,1,1],[1,1,1,1],[3,0,1,1],[4,0,1,1]]
    button_list = []       


    for idx, image in enumerate(images):

        interface_button = QtWidgets.QToolButton()
        interface_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        interface_button.setSizePolicy(SIZE_POLICY)
        interface_button.setAutoRaise(True)

        interface_button.setStyleSheet(INTERFACE_BUTTON_UNSELECTED)

        image_path = f'{asset_dir}/assets/{image}.png'
        interface_button.setIcon(QtGui.QIcon(image_path))
        interface_button.setIconSize(QtCore.QSize(int(frame.size().width()/3.5), int(frame.size().width()/3.5)))
        frame_layout.addWidget(interface_button,widget_positions[idx][0],widget_positions[idx][1],widget_positions[idx][2],widget_positions[idx][3])
        button_list.append(interface_button)

    parent.system_selection = QtWidgets.QToolButton()
    parent.system_selection.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
    parent.system_selection.setSizePolicy(SIZE_POLICY)
    parent.system_selection.setAutoRaise(True)
    parent.system_selection.setStyleSheet(INTERFACE_BUTTON_UNSELECTED)
    for system in settings["systems"].keys():
        if settings["systems"][system]["system_id"] == settings["selected_system"]["system_id"]:
            image_path = f"{asset_dir}/assets/system/{system}.png"
            break
    parent.system_selection.setIcon(QtGui.QIcon(image_path))
    parent.system_selection.setIconSize(QtCore.QSize(int(frame.size().width()/3.5), int(frame.size().width()/3.5)))
    frame_layout.addWidget(parent.system_selection,3,1,2,1)


    parent.sort_new=button_list[0]
    parent.show_beginner=button_list[1]
    parent.open_settings=button_list[2]
    parent.close_software=button_list[3]

    parent.sort_topics.clicked.connect(parent._show_topics)
    parent.sort_new.clicked.connect(parent._sort_new)
    parent.show_beginner.clicked.connect(parent._show_easy_only)
    parent.open_settings.clicked.connect(parent._open_settings)
    parent.close_software.clicked.connect(parent.main_window.close)
    parent.system_selection.clicked.connect(parent._select_system)

    return frame, frame_layout





def create_topic_widgets(parent_widget, parent_layout, screen_size, asset_dir):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QGridLayout(frame)
    frame.resize(int(screen_size.width()*3/4), int(screen_size.height()))
    parent_layout.addWidget(frame,0,1,4,1)
    topic_buttons = []

    for button_idx in range((NUM_TOPIC_ROWS*NUM_TOPIC_COLUMNS)):
        button = TopicButton(parent=parent_widget, screen_size=screen_size)
        button.setSizePolicy(SIZE_POLICY)
        button.setAutoRaise(True)
        frame_layout.addWidget(button,int(button_idx/NUM_TOPIC_COLUMNS),int(button_idx%NUM_TOPIC_COLUMNS))
        topic_buttons.append(button)

    return frame, frame_layout, topic_buttons