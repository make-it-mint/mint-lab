# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""

import RPi.GPIO as GPIO
import time




def distance():
    
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
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
    
    distance = (TimeElapsed * 34300)/2
    
    if distance < 5:
        GPIO.output(GPIO_LED_KURZ, GPIO.HIGH)
    elif distance > 10:
        GPIO.output(GPIO_LED_LANG,GPIO.HIGH)
        
    return distance

def clean():
    GPIO.cleanup()



            
            
            
            