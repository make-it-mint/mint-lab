import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO


class Experiment:
    EXPERIMENT="TEXT"
    ACTION="WRITE"
    CONTENT="hj0hj"
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui
        self.rfid_reader = SimpleMFRC522()

    def run(self):
        try:
            self.value_for_ui.emit("state=2")
            if self.ACTION == "WRITE":
                self.set_text()
            elif self.ACTION=="READ":
                self.value_for_ui.emit(self.get_text())

            self.value_for_ui.emit("state=1")
            time.sleep(.5)
            self.value_for_ui.emit("state=0")
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            GPIO.cleanup()
            self.value_for_ui.emit("state=-1")
            time.sleep(.5)
            self.value_for_ui.emit("state=0")

    def set_text(self):
        #print("Scanning for Card to write...")
        try:
            self.rfid_reader.write(f"{self.CONTENT}")
        except:
            return False
        finally:
            GPIO.cleanup()
        
        return True

    def get_text(self):
        #print("Scanning for Card to read...")
        try:
            
            idx, text = self.rfid_reader.read()
        except:
            return("")
            pass
        finally:
            GPIO.cleanup()
        
        return text

    
    def stop(self):
        GPIO.cleanup()
        self.is_running = False

