from PyQt5 import QtCore, QtGui, QtWidgets
from CustomWidgets import TopicButton
from constants import *


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
    central_widget_layout.setRowStretch(0, 4)
    central_widget_layout.setRowStretch(1, 1)
    central_widget_layout.setRowStretch(2, 10)
    main_window.showFullScreen()

    return main_window, central_widget, central_widget_layout


def create_logo_widget(parent_layout, screen_size, asset_dir):
    logo = QtWidgets.QToolButton()
    logo.setSizePolicy(SIZE_POLICY)
    logo.setAutoRaise(True)
    parent_layout.addWidget(logo,0,0,1,1)
    image_path = f"{asset_dir}/assets/system/logo.png"
    logo.setIcon(QtGui.QIcon(image_path))
    logo.setIconSize(QtCore.QSize(int(screen_size.width()/4.5), int(screen_size.height()*4.5/30)))
    return logo


def create_nav_widgets(parent_layout, screen_size, asset_dir):

    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QHBoxLayout(frame)
    frame.resize(int(screen_size.width()/4), int(screen_size.height()*2/16))
    parent_layout.addWidget(frame,1,0,1,1)

    item_width = int(frame.size().width()/3)


    bt_previous = QtWidgets.QPushButton()
    bt_previous.setSizePolicy(SIZE_POLICY)
    bt_previous.setFlat(True)
    bt_previous.setStyleSheet(
        f"""
        margin-right: 0;
        background-color:rgb(255, 186, 0);
        border: solid 3px rgb(0,0,0);
        border-top-left-radius: {int(frame.size().height()/2)}px;
        border-bottom-left-radius: {int(frame.size().height()/2)}px;""")
    frame_layout.addWidget(bt_previous)
    image_path = f"{asset_dir}/assets/system/previous.png"
    bt_previous.setIcon(QtGui.QIcon(image_path))
    bt_previous.setIconSize(QtCore.QSize(item_width, frame.size().height()))

    bt_next = QtWidgets.QPushButton()
    bt_next.setSizePolicy(SIZE_POLICY)
    bt_next.setFlat(True)
    bt_next.setStyleSheet(
        f"""
        margin-left: 0;
        background-color:rgb(0, 220, 0);
        border: solid 3px rgb(0,0,0);
        border-top-right-radius: {int(frame.size().height()/2)}px;
        border-bottom-right-radius: {int(frame.size().height()/2)}px;
        """)

    frame_layout.addWidget(bt_next)
    image_path = f"{asset_dir}/assets/system/next.png"
    bt_next.setIcon(QtGui.QIcon(image_path))
    bt_next.setIconSize(QtCore.QSize(item_width, frame.size().height()))

    return frame, frame_layout, bt_previous, bt_next


def create_interface_widgets(parent_layout, screen_size, asset_dir, settings, language, font):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QVBoxLayout(frame)
    frame.resize(int(screen_size.width()/4), int(screen_size.height()*5.5/16))
    parent_layout.addWidget(frame,2,0,1,1)
    buttons=['bt_topic','bt_sort_new','bt_show_beginner','languages']
    images=['system/all_topics','system/new','system/easy_experiments',f"languages/{settings['languages'][language]['icon']}"] 
    button_list = []       


    for button, image in zip(buttons,images):
        interface_button = QtWidgets.QToolButton()
        interface_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        interface_button.setSizePolicy(SIZE_POLICY)
        interface_button.setAutoRaise(True)

        if button == 'languages':
            interface_button.setText(f"  {settings[button][language]['name']}")
        else:
            interface_button.setText(f"  {settings[button][language]}")

        interface_button.setFont(font)

        if button == 'bt_topic':
            interface_button.setStyleSheet(INTERFACE_BUTTON_SELECTED)
        else:
            interface_button.setStyleSheet(INTERFACE_BUTTON_UNSELECTED)

        image_path = f'{asset_dir}/assets/{image}.png'
        interface_button.setIcon(QtGui.QIcon(image_path))
        interface_button.setIconSize(QtCore.QSize(int(frame.size().width()/5), int(frame.size().height()/len(buttons))))
        frame_layout.addWidget(interface_button)
        button_list.append(interface_button)




    return frame, frame_layout, button_list[0], button_list[1], button_list[2], button_list[3]


def create_system_widgets(parent_layout, screen_size, asset_dir, settings):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QHBoxLayout(frame)
    frame.resize(int(screen_size.width()/4), int(screen_size.height()*1.5/16))
    parent_layout.addWidget(frame,3,0,1,1)

    
    item_width = int(frame.size().width()/4)

    #Close Software
    close_software = QtWidgets.QPushButton()
    close_software.setSizePolicy(SIZE_POLICY)
    close_software.setFlat(True)
    close_software.setStyleSheet("")
    image_path = f"{asset_dir}/assets/system/exit.png"
    close_software.setIcon(QtGui.QIcon(image_path))
    close_software.setIconSize(QtCore.QSize(item_width, int(frame.size().height())))
    frame_layout.addWidget(close_software)

    #System Selection
    system_selection = QtWidgets.QPushButton()
    system_selection.setSizePolicy(SIZE_POLICY)
    system_selection.setFlat(True)
    system_selection.setStyleSheet("padding-bottom:10px")
    for system in settings["systems"].keys():
        if settings["systems"][system]["system_id"] == settings["selected_system"]["system_id"]:
            image_path = f"{asset_dir}/assets/system/{system}.png"
            break
    system_selection.setIcon(QtGui.QIcon(image_path))
    system_selection.setIconSize(QtCore.QSize(item_width, int(frame.size().height())))
    frame_layout.addWidget(system_selection)

    #Update Software
    update_software = QtWidgets.QPushButton()
    update_software.setSizePolicy(SIZE_POLICY)
    update_software.setFlat(True)
    update_software.setStyleSheet("")
    image_path = f"{asset_dir}/assets/system/update.png"
    update_software.setIcon(QtGui.QIcon(image_path))
    update_software.setIconSize(QtCore.QSize(item_width, int(frame.size().height())))
    frame_layout.addWidget(update_software)


    return frame, frame_layout, close_software, system_selection, update_software


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