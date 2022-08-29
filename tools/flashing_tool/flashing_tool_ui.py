from PyQt5 import QtCore, QtGui, QtWidgets


def setup_main_window(main_window, width, height):
    
    main_window.setStyleSheet(f"background-color:rgb(62, 110, 145)")
    #Set Central Widget
    central_widget = QtWidgets.QWidget(main_window)
    
    #Set Central Widget Layout
    central_widget_layout = QtWidgets.QGridLayout(central_widget)


    main_window.resize(width,height)
    central_widget_layout.setColumnStretch(0, 3)
    central_widget_layout.setColumnStretch(1, 2)
    central_widget_layout.setRowStretch(0, 1)
    central_widget_layout.setRowStretch(1, 3)
    main_window.show()

    return main_window, central_widget, central_widget_layout



def setup_device_filter(parent,parent_layout, root):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QGridLayout(frame)
    frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
    parent_layout.addWidget(frame,0,0,1,1)

    frame_layout.setColumnStretch(0, 4)
    frame_layout.setColumnStretch(1, 1)
    frame_layout.setRowStretch(0, 1)
    frame_layout.setRowStretch(1, 3)



    filter_label = QtWidgets.QLabel("Connected Devices")
    filter_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    filter_label.setFont(QtGui.QFont('Arial', 18))
    filter_label.setStyleSheet(f"color:rgb(230,230,230);")
    frame_layout.addWidget(filter_label,0,0)

    parent.bt_refresh = QtWidgets.QPushButton()
    parent.bt_refresh.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    parent.bt_refresh.setFlat(True)
    frame_layout.addWidget(parent.bt_refresh)
    image_path = f"{root}/assets/update.png"
    parent.bt_refresh.setIcon(QtGui.QIcon(image_path))
    parent.bt_refresh.setIconSize(QtCore.QSize(int(frame.size().width()*0.1), int(frame.size().height()*0.1)))
    frame_layout.addWidget(parent.bt_refresh,0,1)

    parent.bt_refresh.clicked.connect(parent._refresh_devices)




    parent.comports_list_widget = QtWidgets.QListWidget()
    parent.comports_list_widget.setStyleSheet(f"background-color:rgb(230,230,230)")
    parent.comports_list_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    parent.comports_list_widget.setFont(QtGui.QFont('Arial', 18))
    parent.comports_list_widget.clicked.connect(parent._comport_selected)
    frame_layout.addWidget(parent.comports_list_widget,1,0,1,2)
    parent._refresh_devices()

    return frame, frame_layout



def setup_upython_flash(parent,parent_layout, root):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QGridLayout(frame)
    frame.setStyleSheet(f"border: 1px solid gray; border-radius: 10px;")
    frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
    parent_layout.addWidget(frame,1,0,1,1)

    frame_layout.setColumnStretch(0, 1)
    frame_layout.setColumnStretch(1, 2)
    frame_layout.setRowStretch(0, 1)
    frame_layout.setRowStretch(1, 1)
    frame_layout.setRowStretch(2, 2)
    frame_layout.setRowStretch(3, 1)



    flashing_label = QtWidgets.QLabel("Flash MicroPython on Device")
    flashing_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    flashing_label.setFont(QtGui.QFont('Arial', 18))
    flashing_label.setStyleSheet(f"color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(flashing_label,0,0,1,2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)

    parent.bt_select_firmware = QtWidgets.QPushButton("SELECT\nFIRMWARE")
    parent.bt_select_firmware.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.bt_select_firmware.setFont(QtGui.QFont('Arial', 12))
    parent.bt_select_firmware.setStyleSheet(f"background-color:rgb(255,150,0); color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(parent.bt_select_firmware,1,0, QtCore.Qt.AlignTop)
    parent.bt_select_firmware.clicked.connect(parent._select_firmware)




    parent.lb_firmware_path = QtWidgets.QLabel("Filepath to Firmware")
    parent.lb_firmware_path.setWordWrap(True)
    parent.lb_firmware_path.setStyleSheet(f"color:rgb(230,230,230);border: 0px solid gray")
    parent.lb_firmware_path.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.lb_firmware_path.setFont(QtGui.QFont('Arial', 12))
    frame_layout.addWidget(parent.lb_firmware_path,1,1, QtCore.Qt.AlignTop)

    parent.flash_firmware = QtWidgets.QPushButton("FLASH!")
    parent.flash_firmware.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    parent.flash_firmware.setFont(QtGui.QFont('Arial', 18))
    parent.flash_firmware.setStyleSheet(f"background-color:rgb(0,180,0); color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(parent.flash_firmware,2,0,1,2)
    parent.flash_firmware.clicked.connect(parent._flash_firmware)

    parent.flashing_commands = QtWidgets.QTextEdit("If you want to manually do this, the necessary commands will show up here.\nSelect Device first, then select Firmware")
    parent.flashing_commands.setStyleSheet(f"color:rgb(230,230,230);border: 0px solid gray")
    parent.flashing_commands.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.flashing_commands.setFont(QtGui.QFont('Arial', 10))
    parent.flashing_commands.setReadOnly(True)
    frame_layout.addWidget(parent.flashing_commands,3,0,1,2)

    return frame, frame_layout




def setup_execution(parent,parent_layout, root):
    frame = QtWidgets.QFrame()
    frame_layout = QtWidgets.QGridLayout(frame)
    frame.setStyleSheet(f"border: 1px solid gray; border-radius: 10px;")
    frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
    parent_layout.addWidget(frame,0,1,2,1)


    frame_layout.setRowStretch(0, 1)
    frame_layout.setRowStretch(1, 1)
    frame_layout.setRowStretch(2, 2)



    flashing_label = QtWidgets.QLabel("Run Code on Microcontroller")
    flashing_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    flashing_label.setFont(QtGui.QFont('Arial', 18))
    flashing_label.setStyleSheet(f"color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(flashing_label,0,0,1,2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)

    action_label = QtWidgets.QLabel("Run Code on Microcontroller")
    action_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    action_label.setFont(QtGui.QFont('Arial', 12))
    action_label.setStyleSheet(f"color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(action_label,1,0,1,2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)

    parent.cb_action_type = QtWidgets.QComboBox()
    parent.cb_action_type.addItems(["run","put"])
    parent.cb_action_type.setStyleSheet(f"background-color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(parent.cb_action_type,2,0,1,2, QtCore.Qt.AlignTop)
    action = parent.cb_action_type.currentText()
    parent.cb_action_type.currentIndexChanged.connect(parent._select_action)

    parent.file_name_on_ucontroller = QtWidgets.QLineEdit()
    parent.file_name_on_ucontroller.setAlignment(QtCore.Qt.AlignTop)
    parent.file_name_on_ucontroller.setFont(QtGui.QFont('Arial', 12))
    parent.file_name_on_ucontroller.setPlaceholderText(f'filpath on uController (only for put)')
    parent.file_name_on_ucontroller.setStyleSheet(f"background-color:rgb(230,230,230); border-width:0px")
    frame_layout.addWidget(parent.file_name_on_ucontroller,3,0,1,2)


    parent.bt_select_python_file = QtWidgets.QPushButton("SELECT\nFILE")
    parent.bt_select_python_file.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.bt_select_python_file.setFont(QtGui.QFont('Arial', 12))
    parent.bt_select_python_file.setStyleSheet(f"background-color:rgb(255,150,0); color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(parent.bt_select_python_file,4,0)
    parent.bt_select_python_file.clicked.connect(parent._select_python_file)




    parent.lb_selected_python_file = QtWidgets.QLabel("Filepath to MicroPython File")
    parent.lb_selected_python_file.setWordWrap(True)
    parent.lb_selected_python_file.setStyleSheet(f"color:rgb(230,230,230);border: 0px solid gray")
    parent.lb_selected_python_file.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.lb_selected_python_file.setFont(QtGui.QFont('Arial', 12))
    frame_layout.addWidget(parent.lb_selected_python_file,4,1)



    parent.execute_code = QtWidgets.QPushButton("EXECUTE!")
    parent.execute_code.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    parent.execute_code.setFont(QtGui.QFont('Arial', 18))
    parent.execute_code.setStyleSheet(f"background-color:rgb(0,180,0); color:rgb(230,230,230); border: 0px solid gray")
    frame_layout.addWidget(parent.execute_code,5,0,1,2)
    parent.execute_code.clicked.connect(parent._execute_script)



    parent.execution_command = QtWidgets.QTextEdit("If you want to manually do this, the necessary command will show up here.")
    parent.execution_command.setStyleSheet(f"color:rgb(230,230,230);border: 0px solid gray")
    parent.execution_command.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    parent.execution_command.setFont(QtGui.QFont('Arial', 10))
    parent.execution_command.setReadOnly(True)
    frame_layout.addWidget(parent.execution_command,6,0,1,2)

    return frame, frame_layout, action