# This is your main script.
from machine import Pin
from utime import sleep, ticks_diff, ticks_us

SPEED_OF_SOUND=330
RED=10
BLUE=5

try:
    factor = 100/1_000_000 #[m/us -> cm/s]
    TRIGGER = Pin(16, Pin.OUT)
    ECHO = Pin(17, Pin.IN)
    LED_RED = Pin(15,Pin.OUT)
    LED_BLUE = Pin(14,Pin.OUT)
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
        
        LED_RED.on() if distance <= RED else LED_RED.off()
            
        LED_BLUE.on() if distance <= BLUE else LED_BLUE.off()

        print(f"d={distance}\n")
        sleep(.1)

except Exception and KeyboardInterrupt as e:
    print(f"{e}\n")
