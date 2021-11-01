#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:36:07 2021

@author: pi
"""

from tkinter import Tk, Label, Button

import ultraschall
import time
import threading


window = Tk()
measure = False

def bt_click():
    global measure
    if not measure:
        measure = True
        threading.Thread(target = run_ultraschall).start()
    else:
        measure = False

def run_ultraschall():
    
    try:
        while measure:
            dist = ultraschall.distance()
            widgets['label']['ultraschall'].configure(text = "Measured Distance = %.1f cm" %dist)
            time.sleep(1)
        
        print("Measure stopped by Button Click")
        ultraschall.clean()
        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        ultraschall.clean()

def createWidgets():
    font_n = 'Helvetica 22'
    font_b = 'Helvetica 22 bold'
    widgets = {'label':{}, 'button':{}}
    l1 = Label(window,
               text = "No Distance measured",
               font = font_n)
    l1.grid(row = 0, column = 1)
    widgets['label'].update({'ultraschall':l1})
 
    b1 = Button(window,
                text = 'RUN',
                font = font_b,
                command = bt_click)
    b1.grid(row = 0, column = 0)
    widgets['button'].update({'run':b1})
    return widgets
    
widgets = createWidgets()
    
window.mainloop()