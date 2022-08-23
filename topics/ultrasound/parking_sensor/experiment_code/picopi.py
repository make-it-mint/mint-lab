# This is your main script.
import _thread
from machine import Pin
from utime import sleep, ticks_diff, ticks_us

SPEED_OF_SOUND=330
FAR=20
MID=14
NEAR=8
CLOSE=4
FAR_HZ=1
MID_HZ=2
NEAR_HZ=4
CLOSE_HZ=8

distance = FAR+1


def start_beeper(thread_id):
    global distance,FAR,MID,NEAR,CLOSE,FAR_HZ,MID_HZ,NEAR_HZ,CLOSE_HZ
    BEEPER = Pin(15,Pin.OUT)
    #print(f"{distance_value}\n")
    try:
        while True:
            if distance > FAR:
                BEEPER.off()
                sleep(.01)
                continue
            
            if distance >MID:
                duration = float(1/(2*FAR_HZ))
            elif distance <= MID and distance > NEAR:
                duration = float(1/(2*MID_HZ))
            elif distance <= NEAR and distance > CLOSE:
                duration = float(1/(2*NEAR_HZ))
            else:
                duration = float(1/(2*CLOSE_HZ))

            BEEPER.on()
            sleep(duration)

            if not duration == 0:
                BEEPER.off()
                sleep(duration)
            else:
                sleep(.1)
                
    except Exception as e:
        print(e)

try:
    _thread.start_new_thread(start_beeper,(1,))
    factor = 100/1_000_000 #[m/us -> cm/s]
    TRIGGER = Pin(16, Pin.OUT)
    ECHO = Pin(17, Pin.IN)
    
    while True:
        

        TRIGGER.on()
        sleep(.00001)
        TRIGGER.off()
        
        
        while ECHO.value() == 0:
            StartTime = ticks_us()
            
        while ECHO.value() == 1:
            StopTime = ticks_us()
            
        TimeElapsed = ticks_diff(StopTime, StartTime)
        distance = (TimeElapsed * SPEED_OF_SOUND*factor)/2

        print(f"d={distance}\n")
        sleep(.1)

except Exception and KeyboardInterrupt as e:
    print(f"{e}\n")
