# This is your main script.
from machine import Pin
from utime import sleep

FREQUENCY=2

try:
    # Initialisierung der Onboard-LED
    led_onboard = Pin(15, Pin.OUT)

    # Wiederholung (Endlos-Schleife)
    counter = 0
    while True:
        counter+=1
        # LED einschalten
        led_onboard.on()
        print(f"state=on\n")
        # halbe Sekunde warten
        sleep(1/(2*FREQUENCY))
        # LED ausschalten
        led_onboard.off()
        print(f"state=off\n")
        # 1 Sekunde warten
        sleep(1/(2*FREQUENCY))
        
except Exception and KeyboardInterrupt as e:
    print(f"{e}\n")