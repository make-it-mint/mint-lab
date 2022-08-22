import time, ast
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO


class Experiment:
    ACTION_TYPE=custom_write
    TEXT=EFW
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        try:
            self.value_for_ui.emit("2")
            if self.action_type == "custom_write" or self.action_type == "personal_write" or self.action_type == "led_write":
                self.set_text()
            elif self.action_type == "custom_read" or self.action_type == "personal_read":
                self.value_for_ui.emit(self.get_text())
            elif self.action_type == "led_read":
                #print(self.get_text())
                led_action = ast.literal_eval(self.get_text())
                print("LEDs: " + str(led_action))
                if not self.start_led(led_action=led_action):
                    GPIO.cleanup()
                    self.rfid_content.value_for_ui("-2")
                    time.sleep(2)
                    self.rfid_content.value_for_ui("0")
                    return

            self.rfid_content.value_for_ui("1")
            time.sleep(2)
            self.rfid_content.value_for_ui("0")
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            GPIO.cleanup()
            self.rfid_content.value_for_ui("-1")
            time.sleep(2)
            self.rfid_content.value_for_ui("0")

    def set_text(self):
        rfid_reader = SimpleMFRC522()
        try:
            rfid_reader.write(f"{self.text}")
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

    def start_led(self, led_action:list):
        
        try:
            led_red_on = bool(led_action[0])
            if led_red_on:
                if not led_action[1] == "":
                    led_red_freq = int(led_action[1])
                else:
                    led_red_freq = 1
            else:
                led_red_freq = 1


            led_blue_on = bool(led_action[2])
            if led_blue_on:
                if not led_action[3] == "":
                    led_blue_freq = int(led_action[3])
                else:
                    led_blue_freq = 1
            else:
                led_blue_freq = 1


            GPIO.setmode(GPIO.BCM)
            BLUE_PIN = 16
            GPIO.setup(BLUE_PIN, GPIO.OUT)
            GPIO.output(BLUE_PIN, GPIO.LOW)
            RED_PIN = 20
            GPIO.setup(RED_PIN, GPIO.OUT)
            GPIO.output(RED_PIN, GPIO.LOW)
            pause_time = 1/(led_red_freq*led_blue_freq*2)
            counter = 0
            self.rfid_content.value_for_ui("3")
            while True:
                if led_blue_on and counter % led_red_freq == 0:
                    if GPIO.input(BLUE_PIN) == GPIO.LOW:
                        GPIO.output(BLUE_PIN, GPIO.HIGH)
                    else:
                        GPIO.output(BLUE_PIN, GPIO.LOW)

                if led_red_on and counter % led_blue_freq == 0:
                    if GPIO.input(RED_PIN) == GPIO.LOW:
                        GPIO.output(RED_PIN, GPIO.HIGH)
                    else:
                        GPIO.output(RED_PIN, GPIO.LOW)

                counter += 1
                time.sleep(pause_time)

        except Exception as e:
            print(e)
            return False
        finally:
            GPIO.cleanup()
        
        return True

    def stop(self):
        print("Measure stopped by Button Click")
        self.cleanup_pins()
        self.is_running = False

    def cleanup_pins(self):
        GPIO.cleanup()