# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 09:58:11 2021

@author: felix
"""
from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Checkbutton, IntVar, messagebox, PhotoImage
from PIL import Image, ImageTk
import math

class MeasureDistance:
    
    DEF_FONT = 'Helvetica 18'
    FONT_B = 'Helvetica 18 bold'
    FONT_L = 'Helvetica 32'
    
    def __init__(self, language):
        self._language = language
        self._main_menu = self._setup_root()
        self._widgets = {'label':{}, 'button':{},'listbox':{},'checkbutton':{},'text':{},'scrollbar':{}, 'frame':{} , 'radiobutton':{}, 'plot':{}}
        self._create_main_ui()
        
    def start_app(self):
        self._main_menu.mainloop()
        
    def _setup_root(self):
        main_menu = Tk()
        main_menu.attributes("-fullscreen", True)
        main_menu.grid_columnconfigure(0, weight = 1)
        main_menu.grid_rowconfigure(0, weight = 1)
        return main_menu
    
    def _create_main_ui(self):
                
        bt_close = Button(self._main_menu,
                          text = "Exit",
                          font = self.FONT_B,
                          bg = 'red',
                          command = lambda: self._main_menu.destroy())
        bt_close.grid(row = 0, column = 0, sticky = 'nsew')
        self._widgets['button'].update({'main_exit': bt_close})
        
MeasureDistance('de').start_app()
        
        