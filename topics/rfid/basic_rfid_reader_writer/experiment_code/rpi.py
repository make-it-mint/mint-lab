import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO


class Experiment:
    EXPERIMENT="TEXT"
    ACTION="WRITE"
    CONTENT=""
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        try:
            self.value_for_ui.emit("state:2")
            if self.ACTION == "WRITE":
                self.set_text()
            elif self.ACTION=="READ":
                self.value_for_ui.emit(self.get_text())

            self.value_for_ui("state=1")
            time.sleep(2)
            self.value_for_ui("state=0")
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            GPIO.cleanup()
            self.value_for_ui("state=-1")
            time.sleep(2)
            self.value_for_ui("state=0")

    def set_text(self):
        rfid_reader = SimpleMFRC522()
        try:
            rfid_reader.write(f"{self.CONTENT}")
        except:
            return False
        finally:
            GPIO.cleanup()
        
        return True

    def get_text(self):
        rfid_reader = SimpleMFRC522()
        try:
            
            idx, text = rfid_reader.read()
        except:
            pass
        finally:
            GPIO.cleanup()
        
        return text

    
    def stop(self):
        print("Measure stopped by Button Click")
        GPIO.cleanup()
        self.is_running = False

