from time import sleep
import RPi.GPIO as GPIO


class Experiment:
    FREQUENCY=2
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO_LED = 26
        GPIO.setup(GPIO_LED, GPIO.OUT)

        while self.is_running:
            # LED einschalten
            GPIO.output(GPIO_LED,GPIO.HIGH)
            self.value_for_ui.emit(f"state=on")
            # halbe Sekunde warten
            sleep(1/(2*self.FREQUENCY))
            # LED ausschalten
            GPIO.output(GPIO_LED,GPIO.LOW)
            self.value_for_ui.emit(f"state=off")
            # 1 Sekunde warten
            sleep(1/(2*self.FREQUENCY))
            
        GPIO.cleanup()

    def stop(self):
        #print("Measure stopped by Button Click")
        self.is_running = False