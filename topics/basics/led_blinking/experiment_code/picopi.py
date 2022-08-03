# This is your main script.
from machine import Pin
from utime import sleep

FREQUENCY=2

try:
    # Initialisierung der Onboard-LED
    led_onboard = Pin("LED", Pin.OUT)

    # Wiederholung (Endlos-Schleife)
    counter = 0
    while True:
        counter+=1
        # LED einschalten
        led_onboard.on()
        # halbe Sekunde warten
        sleep(1/FREQUENCY)
        # LED ausschalten
        led_onboard.off()
        # 1 Sekunde warten
        sleep(1/FREQUENCY)
        print(f"counter={counter}\n")
except Exception and KeyboardInterrupt as e:
    print(f"{e}\n")