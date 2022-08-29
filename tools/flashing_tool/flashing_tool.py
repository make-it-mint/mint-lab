import sys, os, time
from PyQt5 import QtCore, QtGui, QtWidgets
from flashing_tool_ui import *
import multiprocessing
from serial.tools.list_ports import comports as list_comports




class FlashingTool(object):
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.width, self.height= 1200,800
        self.selected_comport = None
        self.selected_firmware = None
        self.firmware_path = None
        self.selected_micropython_script = None
        self.selected_action = None
        self.file_name_on_microcontroller =""
        self.script_is_running = False

    def setup_ui(self, main_window):
        self.main_window, self.central_widget, self.central_widget_layout = setup_main_window(main_window=main_window, width=self.width, height=self.height)
        self.main_window.setCentralWidget(self.central_widget)


        self.frame_filter, self.frame_filter_layout = setup_device_filter(
            parent=self,
            parent_layout=self.central_widget_layout,
            root=FlashingTool.ROOT_DIR
            )

        self.frame_flash_upython, self.frame_flash_upython_layout = setup_upython_flash(
            parent=self,
            parent_layout=self.central_widget_layout,
            root=FlashingTool.ROOT_DIR
            )

        self.frame_execution, self.frame_execution_layout, self.selected_action = setup_execution(
            parent=self,
            parent_layout=self.central_widget_layout,
            root=FlashingTool.ROOT_DIR
            )

    def _refresh_devices(self):
        self.comports_list_widget.clear()
        self.comports_list_widget.addItems([comport.device for comport in list_comports()])
    

    def _comport_selected(self):
        self.selected_comport=self.comports_list_widget.currentItem().text()
        #print(self.selected_comport)

    def _select_firmware(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window,"Choose Firmware Binary", "","Binaries (*.bin)", options=options)
        self.firmware_path =file_name
        self.lb_firmware_path.setText(self.firmware_path)
        if self.selected_comport and self.firmware_path:
            self.flashing_commands.setText(f"esptool.py --chip esp32 --port {self.selected_comport} erase_flash\n\n\nesptool.py --chip esp32 --port {self.selected_comport} --baud 460800 write_flash -z 0x1000 {self.firmware_path}")

    def _flash_firmware(self):
        if self.selected_comport and self.firmware_path:
            os.system(f'esptool.py --chip esp32 --port {self.selected_comport} erase_flash')
            os.system(f'esptool.py --chip esp32 --port {self.selected_comport} --baud 460800 write_flash -z 0x1000 {self.firmware_path}')
        if not self.selected_comport:print("ERROR: No Port Selected")
        if not self.firmware_path:print("ERROR: No Firmware File Selected")

    def _select_action(self):
        self.selected_action =self.cb_action_type.currentText()
        if self.selected_micropython_script and self.selected_action and self.selected_comport:
            print(f"os.system(ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script})")
        if not self.selected_comport:print("Command cannot be shown: No Port Selected")
        if not self.selected_micropython_script:print("Command cannot be shown: No MicroPython Script Selected")
        if not self.selected_action:print("Command cannot be shown: No Action Selected")


    def _select_python_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window,"Choose MicroPython File", "","Py File (*.py)", options=options)
        self.selected_micropython_script =file_name
        self.lb_selected_python_file.setText(self.selected_micropython_script)
        self._set_execution_text()

    def _set_execution_text(self):
        if self.selected_action == "run":
            if self.selected_micropython_script and self.selected_action and self.selected_comport:
                self.execution_command.setText(f"os.system(f'ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script}')")
            else:
                if not self.selected_comport:print("ERROR: No Port Selected")
                if not self.selected_micropython_script:print("ERROR: No MicroPython Script Selected")
                if not self.selected_action:print("ERROR: No Action Selected")
        elif self.selected_action =="put":
            if self.selected_micropython_script and self.selected_action and self.selected_comport and not self.file_name_on_microcontroller == "":
                self.execution_command.setText(f"os.system(f'ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script} {self.file_name_on_microcontroller}')")
            else:
                if not self.selected_comport:print("ERROR: No Port Selected")
                if not self.selected_micropython_script:print("ERROR: No MicroPython Script Selected")
                if not self.selected_action:print("ERROR: No Action Selected")
                if self.file_name_on_microcontroller == "":print("ERROR: No Name for File On Microcontroller Selected")


    def _execute_script(self):
        if not self.script_is_running:
            self.experiment_thread= multiprocessing.Process(target=self._start_script, args=(self.script_is_running,))
            self.experiment_thread.start()
        else:
            # self.experiment_thread.terminate()
            # time.sleep(3)
            os.system(f'ampy --port {self.selected_comport} reset')
            #os.system(f'ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script} {self.file_name_on_microcontroller}')
            self.execute_code.setStyleSheet(f"background-color:rgb(0,180,0); color:rgb(230,230,230); border: 0px solid gray")
            self.execute_code.setText("EXECUTE!")
            self.script_is_running = False

    def _start_script(self, script_state):
        if self.selected_action == "run":
            if self.selected_micropython_script and self.selected_action and self.selected_comport:
                self.execute_code.setStyleSheet(f"background-color:rgb(180,0,0); color:rgb(230,230,230); border: 0px solid gray")
                self.execute_code.setText("STOP SCRIPT")
                script_state = True
                print(script_state)
                try:
                    os.system(f'ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script} {self.file_name_on_microcontroller}')
                except Exception as e:
                    print(e)
            else:
                if not self.selected_comport:print("ERROR: No Port Selected")
                if not self.selected_micropython_script:print("ERROR: No MicroPython Script Selected")
                if not self.selected_action:print("ERROR: No Action Selected")


        elif self.selected_action =="put":
            if self.selected_micropython_script and self.selected_action and self.selected_comport and not self.file_name_on_microcontroller == "":
                self.execute_code.setStyleSheet(f"background-color:rgb(180,0,0); color:rgb(230,230,230); border: 0px solid gray")
                self.execute_code.setText("STOP SCRIPT")
                script_state = True
                try:
                    os.system(f'ampy --port {self.selected_comport} {self.selected_action} {self.selected_micropython_script} {self.file_name_on_microcontroller}')
                except Exception as e:
                    print(e)
            else:
                if not self.selected_comport:print("ERROR: No Port Selected")
                if not self.selected_micropython_script:print("ERROR: No MicroPython Script Selected")
                if not self.selected_action:print("ERROR: No Action Selected")
                if self.file_name_on_microcontroller == "":print("ERROR: No Name for File On Microcontroller Selected")





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_ui = FlashingTool()
    main_ui.setup_ui(main_window)
    
    sys.exit(app.exec())