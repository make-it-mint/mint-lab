import time, threading
import RPi.GPIO as GPIO


class Experiment:
    SPEED_OF_SOUND=330
    FAR=20
    MID=14
    NEAR=10
    CLOSE=4
    FAR_HZ=1
    MID_HZ=2
    NEAR_HZ=4
    CLOSE_HZ=8

    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui
        self.distance_beeper = self.FAR + 1

    def run(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO_TRIGGER = 21
            GPIO_ECHO = 16
            

            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO,GPIO.IN)
            
            beeper_thread = threading.Thread(target=self.start_beeper).start()

            while self.experiment_is_running:
                #distance = random.uniform(0,22)

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
                self.distance_beeper = (TimeElapsed * self.SPEED_OF_SOUND*100)/2
                self.value_for_ui.emit(self.distance_beeper)
                time.sleep(.2)
        except(Exception, KeyboardInterrupt) as e:
            print(e)
            print("Measurement stopped by User")
            self.cleanup_pins()


    def start_beeper(self):

        GPIO_BEEPER = 5
        GPIO.setup(GPIO_BEEPER, GPIO.OUT)

        try:
            while self.experiment_is_running:
                if float(self.distance_beeper) > float(self.FAR):
                    GPIO.output(GPIO_BEEPER, GPIO.LOW)
                    continue
                
                if float(self.distance_beeper) >float(self.MID):
                    duration = float(1/(2*self.FAR_HZ))
                elif float(self.distance_beeper) <=float(self.MID) and self.distance_beeper > float(self.NEAR):
                    duration = float(1/(2*self.MID_HZ))
                elif float(self.distance_beeper) <=float(self.NEAR) and self.distance_beeper > float(self.CLOSE):
                    duration = float(1/(2*self.NEAR_HZ))
                else:
                    duration = float(1/(2*self.CLOSE_HZ))

                GPIO.output(GPIO_BEEPER, GPIO.HIGH)
                time.sleep(duration)

                if not duration == 0:
                    GPIO.output(GPIO_BEEPER, GPIO.LOW)
                    time.sleep(duration)
                else:
                    time.sleep(.1)
        except Exception as e:
            print(e)



    def stop(self):
        print("Measure stopped by Button Click")
        self.cleanup_pins()
        self.is_running = False

    def cleanup_pins(self):
        GPIO.cleanup()
