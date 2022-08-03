import time
import RPi.GPIO as GPIO


class Experiment:
    SPEED_OF_SOUND=330
    RED=1
    BLUE=6
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        try:
            while self.is_running:
                if self.SPEED_OF_SOUND is None:
                    break

                self.value_for_ui.emit(f"d={self.measure_distance()}")
                time.sleep(1)
        except(Exception, KeyboardInterrupt) as e:
            print(e)
            print("Measurement stopped by User")
            self.cleanup_pins()


    def measure_distance(self):

        #distance = random.randint(2,40)
        
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 21
        GPIO_ECHO = 16
        GPIO_LED_KURZ = 26
        GPIO_LED_LANG = 5

        
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO,GPIO.IN)
        GPIO.setup(GPIO_LED_KURZ, GPIO.OUT)
        GPIO.setup(GPIO_LED_LANG, GPIO.OUT)
        
        GPIO.output(GPIO_LED_KURZ, GPIO.LOW)
        GPIO.output(GPIO_LED_LANG,GPIO.LOW)
        
        GPIO.output(GPIO_TRIGGER,True)
        
        time.sleep(.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        StartTime = time.time()
        StopTime = time.time()
        
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
            
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
            
        
        TimeElapsed = StopTime - StartTime
        
        distance = (TimeElapsed * self.SPEED_OF_SOUND*100)/2
        
        if distance <= self.RED:
            GPIO.output(GPIO_LED_KURZ, GPIO.HIGH)
        if distance <= self.BLUE:
            GPIO.output(GPIO_LED_LANG,GPIO.HIGH)
            
        return distance



    def stop(self):
        print("Measure stopped by Button Click")
        self.cleanup_pins()
        self.is_running = False

    def cleanup_pins(self):
        GPIO.cleanup()
