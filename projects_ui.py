# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 19:35:02 2021

@author: felix
"""

from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Checkbutton, IntVar, messagebox, PhotoImage
from PIL import Image, ImageTk
import math
import importlib.util



class Project():
    
    DEF_FONT = 'Helvetica 18'
    FONT_B = 'Helvetica 18 bold'
    FONT_L = 'Helvetica 32'
    
    def __init__ (self, window, main_widgets, data, name, directory, sys_content, language):
        self._project_name = name
        self._window = window
        self._data = data
        self._sys_content = sys_content
        self._directory = directory
        self._main_widgets = main_widgets
        self._widgets = {'label':{}, 'button':{},'listbox':{},'checkbutton':{},'text':{},'scrollbar':{}, 'frame':{} , 'radiobutton':{}, 'plot':{}}
        self._num_pages = len(data)
        self._current_page = 0
        self._language = language
        self._set_interface()
        #self._set_ui(self._data[self._current_page])
        
        
    def _close_project(self):
        self._window.grid_remove()
        self._main_widgets['frame']['main_frame'].grid()
    
        
    def _update_page(self, new_page):
        if self._data[self._current_page][0] == "info":
            for item in range(1, len(self._data[self._current_page])):
                self._widgets['label'][str(item)]['object'].destroy()
                self._widgets['label'].pop(str(item), None)
        
        self._window.update()
        self._current_page = new_page
        self._widgets['label']['page'].configure(text = "%d/%d"%(self._current_page + 1, self._num_pages))
        self._set_ui()
        
        
    def _back(self):
        if self._current_page > 0:
            self._update_page(self._current_page - 1)
        else:
            pass
        
    def _next(self):
        if self._current_page < self._num_pages -1:
            self._update_page(self._current_page + 1)
        else:
            pass
        
    def _set_interface(self, appointed_row = 0):
        frame_interface = Frame(self._window)
        frame_interface.grid(row = appointed_row, column = 0, sticky = 'new')
        frame_interface.grid_columnconfigure(1, weight = 1)
        self._widgets['frame'].update({'frame_interface':frame_interface})
        
        bt_close = Button(self._widgets['frame']['frame_interface'],
                         text = self._sys_content['bt_exit'],
                         fg = 'white',
                         bg = 'black',
                         font = Project.FONT_B,
                         command = self._close_project)
        bt_close.grid(row = 0, column = 0)
        self._widgets['button'].update({'close':bt_close})
        
        
        lb_name = Label(self._widgets['frame']['frame_interface'],
                        text = self._project_name,
                        font = Project.FONT_L)
        lb_name.grid(row = 0, column = 1)
        self._widgets['label'].update({'project_name':lb_name})
        
        
        bt_back = Button(self._widgets['frame']['frame_interface'],
                         text = '<--',
                         fg = 'white',
                         bg = 'orange',
                         font = Project.FONT_B,
                         command = self._back)
        bt_back.grid(row = 0, column = 2)
        self._widgets['button'].update({'back':bt_back})
        
        lb_page = Label(self._widgets['frame']['frame_interface'],
                        text = "%d/%d"%(self._current_page + 1, self._num_pages),
                        font = Project.FONT_L)
        lb_page.grid(row = 0, column = 3)
        self._widgets['label'].update({'page':lb_page})
        
        bt_next = Button(self._widgets['frame']['frame_interface'],
                         text = '-->',
                         fg = 'white',
                         bg = 'green',
                         font = Project.FONT_B,
                         command = self._next)
        bt_next.grid(row = 0, column = 4)
        self._widgets['button'].update({'back':bt_next})
        
        self._set_ui()
        
        
    def _set_ui(self):
        page_content = self._data[self._current_page]
        #self._window.grid_columnconfigure(0, weight = 1)
        
        if page_content[0] == "info":
            self._set_info_page(page_content)
        elif page_content[0] == 'experiment':
            
            spec = importlib.util.spec_from_file_location("module.name", page_content[1]['name'])
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            foo.Experiment(language = self._language).start_app()

                    
                
    def _set_info_page(self, page_content):
        for row in range(1, len(page_content)):
            self._window.grid_rowconfigure(row, weight = 1)
            
        for idx, item in enumerate(page_content):
            if idx == 0:
                pass
                #self._set_interface(idx)
            else:
                if item['type'] == 'text':
                    lbl = Label(self._window,
                                wraplength = self._main_widgets['frame']['main_project_list'].winfo_width(),
                                text = item['content'],
                                font = Project.DEF_FONT)
                    lbl.grid(row = idx, column = 0, sticky = 'n')
                    self._widgets['label'].update({str(idx):{'object':lbl}})
                    
                elif item['type'] == 'img':
                    
                    aim_height = int(self._main_widgets['frame']['main_project_list'].winfo_height()/len(page_content))
                    aim_width = self._main_widgets['frame']['main_project_list'].winfo_width()
                    loaded_img = Image.open(self._directory + '/graphics/' + item['content'])
                    scaled = self._scale_img(loaded_img, aim_height, aim_width)
                    img = ImageTk.PhotoImage(scaled)
                    lbl = Label(self._window,
                                image = img)
                    lbl.grid(row = idx, column = 0, sticky = 'n')
                    self._widgets['label'].update({str(idx):{'object':lbl, 'img':img}})
                    
                    
    def _scale_img(self, image, aim_height, aim_width):
        
        
        width, height = image.size
        
        scale_width = aim_width/width
        scale_height = aim_height/height
        if scale_width < scale_height:
            scale_factor = scale_width
        else:
            scale_factor = scale_height
        width_new = int(width*scale_factor)
        height_new = int(height*scale_factor)
        image = image.resize((width_new, height_new), Image.ANTIALIAS)
        return image
        