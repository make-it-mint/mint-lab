# This is your main script.
from machine import Pin
from utime import sleep

def run():
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
            sleep(0.1)
            # LED ausschalten
            led_onboard.off()
            # 1 Sekunde warten
            sleep(.1)
            print(f"counter={counter}:second_value=2\n")
    except KeyboardInterrupt:
        return "closed"

if __name__ == "__main__":
    run()