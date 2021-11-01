# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 08:49:26 2021

@author: felix
"""

from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Radiobutton, Checkbutton, StringVar, IntVar, messagebox, PhotoImage
from PIL import Image, ImageTk
import nav_widgets as nav
import list_widgets as list_w
import details_widgets as details


class CreatorApp:
    WIDGET_TYPES = ['Button','Image','Text']
    WIDGET_PARAMS = ['Backgroundcolour', 'Textcolour', 'Fontsize','Command', 'Name', 'Filename', 'Text']
    
    DEF_FONT = 'Helvetica 16'
    FONT_B = 'Helvetica 18 bold'
    FONT_L = 'Helvetica 32'
    
    def __init__(self, columns = 10, rows = 10, language = 'de'):
        self._language = language
        self._num_col = columns
        self._num_row = rows
        self._widgets = {'label':{}, 'button':{},'listbox':{},'checkbutton':{},'text':{},'scrollbar':{}, 'frame':{} , 'radiobutton':{}}
        self._page_grid_buttons = {}
        self._selected_grid_pos = []
        self._current_widget ={}
        self._current_page = []
        self._project = {'name':'','directory':'','pages':[]}
        self._window = Tk()
        self._create_ui()
        self._widget_validity = True
        
        
    def start_app(self):
        self._window.mainloop()
        
        
    def _create_ui(self):
        
        #self._window.grid_columnconfigure(0, weight = 3)
        #self._window.grid_columnconfigure(1, weight = 1)
        
        lbl_project = Label(self._window,
                            text = "Projectname",
                            font = self.DEF_FONT)
        lbl_project.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")
        self._widgets['label'].update({'projectname': lbl_project})
        
        self._widgets = nav.create_widgets(self._window, self._widgets, self.DEF_FONT)

        self._widgets = list_w.create_widgets(self._window, self._widgets, self.DEF_FONT)
        
        self._widgets = details.create_widgets(self._window, self._widgets, self.DEF_FONT, self.WIDGET_TYPES, self.WIDGET_PARAMS)
        self._update_widget_config()
        
        self._set_grid_views(self._widgets['frame']['frame_grid'])
    
        
        self._configure_buttons()
        
        
        
    def _configure_buttons(self):
        
        '''NAV BUTTONS'''
        self._widgets['button']['nav_new_project'].configure(command = lambda: self._create_new_project())
        self._widgets['button']['nav_load_project'].configure(command = lambda: self._load_project())
        self._widgets['button']['nav_back'].configure(command = lambda: self._back())
        self._widgets['button']['nav_next'].configure(command = lambda: self._next())
        self._widgets['button']['nav_preview'].configure(command = lambda: self._show_preview())
        self._widgets['button']['nav_add_page'].configure(command = lambda: self._add_page())
        self._widgets['button']['nav_del_page'].configure(command = lambda: self._delete_page())
        
        
        '''LIST BUTTONS'''
        self._widgets['button']['show_selected_widget'].configure(command = lambda: self._show_selected_widget())
        self._widgets['button']['delete_selected_widget'].configure(command = lambda: self._delete_selected_widget())
            
        
        '''LAYOUT BUTTONS'''
        self._widgets['button']['layout_load_layout'].configure(command = lambda: self._load_layout())
        self._widgets['button']['layout_set_grid'].configure(command = lambda: self._set_grid())
        self._widgets['button']['layout_load_layout'].configure(command = lambda: self._load_layout())
        
        
        '''WIDGET TYPES'''
        for item in self.WIDGET_TYPES:
            self._widgets['radiobutton'][item].configure(command = lambda: self._update_widget_config())
            
            
        '''CREATION BUTTONS'''
        self._widgets['button']['clear_widget'].configure(command = lambda: self._clear_selection())
        self._widgets['button']['add_widget'].configure(command = lambda: self._add_widget())
        self._widgets['button']['save_project'].configure(command = lambda: self._save_project())
        
   
            
    def _update_widget_config(self):
        
        if self._widgets['radiobutton']['widget_choice'].get() == 'Button':
            self._widgets['text']['Filename'].grid_remove()
            self._widgets['text']['Command'].grid()
            self._widgets['text']['Name'].grid()
        elif self._widgets['radiobutton']['widget_choice'].get() == 'Image':
            self._widgets['text']['Filename'].grid()
            self._widgets['text']['Command'].grid_remove()
            self._widgets['text']['Name'].grid_remove()
        elif self._widgets['radiobutton']['widget_choice'].get() == 'Text':
            self._widgets['text']['Filename'].grid_remove()
            self._widgets['text']['Command'].grid_remove()
            self._widgets['text']['Name'].grid_remove()
        

        
    
    '''###################### NAV AREA ######################################'''
    
    def _create_new_project(self):
        print("Project Created")
        
    def _load_project(self):
        print("Project Loaded")
        
    def _back(self):
        print("Back")
        
    def _next(self):
        print("Next")
        
    def _show_preview(self):
        print("Preview")
        
    def _add_page(self):
        print("Add Page")
    
    def _delete_page(self):
        print("Delete Page")
        
    '''################## DETAILS AREA ######################################'''
    
    def _load_layout(self):
        print("Load Layout")
    
    '''################## LIST AREA #########################################'''
    
    def _show_selected_widget(self):
        print("Show Selected Widget")
        
    def _delete_selected_widget(self):
        print("Delete Selected Widget")
        
    '''################## CREATION AREA #####################################'''
    
    def _clear_selection(self):
        print("CLEAR IT ALL!!")
        
    
    def _add_widget(self):
        print("ADD IT TO PAGE")
        
    def _save_project(self):
        print("SAVE IT!!!")
    
    '''################## MATRIX AREA #######################################'''
    
    def _set_grid_views(self, parent):
        
        grid_frame = Frame(parent)
        grid_frame.grid(row = 0, column = 0, sticky = "nsew")
        self._widgets['frame'].update({'current_grid': grid_frame})
        
        num_buttons = self._num_row*self._num_col
        for item in range(num_buttons):
            cur_row = int(item/self._num_col)
            cur_col = int(item%self._num_col)
            name = '%d,%d'%(cur_row, cur_col)
            
            if name in self._selected_grid_pos:
                colour = 'light blue'
                state = 1
            else:
                colour = 'light gray'
                state = 0
                
            bt = Button(grid_frame,
                        text = name,
                        bg = colour,
                        font = self.DEF_FONT,
                        command = lambda bt_name = name: self._select_grid_pos(bt_name))
            bt.grid(row = cur_row, column = cur_col, sticky = 'news')
            self._page_grid_buttons.update({name:{
                'object': bt,
                'state': state}})
        
        lbl_state = Label(grid_frame,
                          bg = 'light gray',
                          width = 5)
        lbl_state.grid(row = 0, column = self._num_col, rowspan = self._num_row, sticky = 'news')
        self._widgets['label'].update({'validity': lbl_state})
        self._check_grid_validity()
        
        
        
    def _select_grid_pos(self, bt_text):
        
        selected_item =  self._page_grid_buttons[bt_text]
        selected_bt = selected_item['object']
        bt_state = selected_item['state']
        if bt_state == 0:
            selected_bt.configure(background = 'light blue')
            self._selected_grid_pos.append(bt_text)
            self._page_grid_buttons[bt_text].update({'state':1})
        elif bt_state == 1:
            selected_bt.configure(background = 'light gray')
            self._selected_grid_pos.remove(bt_text)
            self._page_grid_buttons[bt_text].update({'state':0})
        elif bt_state == 2:
            print("Gridposition selected by other widget")
        
        self._check_grid_validity()
        
        
    
    def _check_grid_validity(self):
    
        c = [list(map(int, item.split(','))) for item in self._selected_grid_pos]
        c.sort()
        maximums = [0,0]
        minimums = [self._num_row, self._num_col]
        for item in c:
            if item[0] < minimums[0]:
                minimums[0] = item[0]
            if item[1] < minimums[1]:
                minimums[1] = item[1]
            if item[0] > maximums[0]:
                maximums[0] = item[0]
            if item[1] > maximums[1]:
                maximums[1] = item[1]  
            
        num_list_plan = ((maximums[0] - minimums[0] + 1) * (maximums[1] - minimums[1] + 1))
        
        if len(self._selected_grid_pos) != num_list_plan:
            self._widgets['label']['validity'].configure(bg = 'red')
            self._widget_validity = False
        else:
            self._widgets['label']['validity'].configure(bg = 'light green')
            self._widget_validity = True
    

        
    def _set_grid(self):
        print("Set Grid")
        self._widgets['frame']['current_grid'].destroy()
        self._page_grid_buttons.clear()
        print(len(self._page_grid_buttons))
        self._widgets['frame']['frame_grid'].update()
        self._num_row = int(self._widgets['text']['layout_rows'].get("1.0","end-1c"))
        self._num_col = int(self._widgets['text']['layout_cols'].get("1.0","end-1c"))
        self._set_grid_views(self._widgets['frame']['frame_grid'])
    

    
    

        
    def _change_widget(self):
        pass

        
    
        
        
CreatorApp().start_app()