# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:31:25 2021

@author: felix
"""
from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Radiobutton, Checkbutton, StringVar, IntVar, messagebox, PhotoImage


def create_widgets(parent, widgets, font, widget_types, widget_params):
    
    frame_details = Frame(parent)
    frame_details.grid(row = 2, column = 0, sticky = "nsew", padx = 10)
    widgets['frame'].update({'frame_details': frame_details})
    widgets = set_details_widgets(frame_details, widgets, font, widget_types, widget_params)
    
    return widgets

def set_details_widgets(parent, widgets, font, widget_types, widget_params):
    
    frame_screen = Frame(parent)
    frame_screen.grid(row = 0, column = 0, sticky = "nsew", pady = 10)
    widgets['frame'].update({'frame_screen': frame_screen})
    widgets = set_layout_widgets(frame_screen, widgets, font)
    
    frame_widgets = Frame(parent)
    frame_widgets.grid(row = 1, column = 0, sticky = "nsew", pady = 10)
    widgets['frame'].update({'frame_widgets': frame_widgets})
    widgets = set_widget_selection(frame_widgets, widgets, font, widget_types)
    
    frame_widget_config = Frame(parent)
    frame_widget_config.grid(row = 2, column = 0, sticky = "nsew", pady = 10)
    widgets['frame'].update({'frame_widget_config': frame_widget_config})
    widgets = set_widget_config(frame_widget_config, widgets, font, widget_params)
    
    frame_widget_creation = Frame(parent)
    frame_widget_creation.grid(row = 3, column = 0, sticky = "nsew", pady = 10)
    widgets['frame'].update({'frame_widget_creation': frame_widget_creation}) 
    widgets = set_widget_creation(frame_widget_creation, widgets, font)
    
    return widgets
    
def set_layout_widgets(parent, widgets, font):
    bt_load_layout = Button(parent,
                            text = "Load\nLayout",
                            font = font)
    bt_load_layout.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, padx = (0, 20))
    widgets['button'].update({'layout_load_layout': bt_load_layout})
    
           
    lbl_row = Label(parent,
                     text = "Rows",
                     font = font)
    lbl_row.grid(row = 3, column = 0, sticky = "news")
    
    lbl_col = Label(parent,
                     text = "Cols",
                     font = font)
    lbl_col.grid(row = 4, column = 0, sticky = "news")
    
    txt_row = Text(parent,
                   height = 1,
                   width = 2,
                   font = font)
    txt_row.grid(row = 3, column = 1)
    widgets['text'].update({'layout_rows': txt_row})
    
    txt_col = Text(parent,
                   height = 1,
                   width = 2,
                   font = font)
    txt_col.grid(row = 4, column = 1)
    widgets['text'].update({'layout_cols': txt_col})
    
    
    bt_set_grid = Button(parent,
                     text = "Set Grid",
                     font = font)
    bt_set_grid.grid(row = 5, column = 0, columnspan = 2)
    widgets['button'].update({'layout_set_grid': bt_set_grid})
    
    lbl_screen = Label(parent,
                     text = "Screen",
                     font = font)
    lbl_screen.grid(row = 0, column = 2, rowspan = 3, sticky = "news")
    
    lbl_width = Label(parent,
                     text = "Width",
                     font = font)
    lbl_width.grid(row = 0, column = 3, sticky = "news")
    
    lbl_height = Label(parent,
                     text = "Height",
                     font = font)
    lbl_height.grid(row = 1, column = 3, sticky = "news")
    
    txt_width = Text(parent,
                   height = 1,
                   width = 5,
                   font = font)
    txt_width.grid(row = 0, column = 4)
    widgets['text'].update({'layout_width': txt_width})
    
    txt_height = Text(parent,
                   height = 1,
                   width = 5,
                   font = font)
    txt_height.grid(row = 1, column = 4)
    widgets['text'].update({'layout_height': txt_height})
    
    cb_fs_var = IntVar()
    cb_fullscreen = Checkbutton(parent,
                                text = "Fullscreen",
                                variable = cb_fs_var,
                                onvalue = 1,
                                offvalue = 0,
                                font = font)
    cb_fullscreen.grid(row = 2, column = 3, columnspan = 2, sticky = "news")
    widgets['checkbutton'].update({'fullscreen': {'widget':cb_fullscreen, 'state':cb_fs_var}})
    
    frame_matrix_layout = Frame(parent)
    frame_matrix_layout.grid(row = 3, column = 2, rowspan = 4, columnspan = 4, sticky = "nsew")
    widgets['frame'].update({'frame_grid': frame_matrix_layout})
    
    
    
    return widgets
    


def set_widget_selection(parent, widgets, font, widget_types):
    
    widget_choice_var = StringVar()
    widget_choice_var.set(widget_types[0])
    widgets['radiobutton'].update({'widget_choice':widget_choice_var})
    for idx, widget in enumerate(widget_types):
        row = int(idx/len(widget_types))
        column = int(idx%len(widget_types))
        rb = Radiobutton(parent,
                         text=widget,
                         variable= widgets['radiobutton']['widget_choice'],
                         value=widget,
                         font = font)
        rb.grid(row = row, column = column, sticky = "w")
        widgets['radiobutton'].update({widget: rb}) 
    
    parent.grid_columnconfigure(0, weight = 1)
    parent.grid_columnconfigure(1, weight = 1)
    
    return widgets
    
    
    
def set_widget_config(parent, widgets, font, widget_params):
    for idx, item in enumerate(widget_params):
        
        lbl = Label(parent,
                    text = item,
                    font = font)
        lbl.grid(row = idx, column = 0, sticky = 'w')
        
        if item == 'Text':
            lines = 5
            width = 50 
        else:
            lines = 1
            width = 20
            
        txt = Text(parent,
                   font = font,
                   width = width,
                   height = lines)
        txt.grid(row = idx, column = 1, sticky = 'w')
        widgets['text'].update({item: txt})
    
    return widgets
    
    
    
def set_widget_creation(parent, widgets, font):
    
    bt_clear_widget = Button(parent,
                            text = "Clear Selection",
                            font = font)
    bt_clear_widget.grid(row = 0, column = 0, sticky = "news")
    widgets['button'].update({'clear_widget': bt_clear_widget})
    
    bt_add_widget = Button(parent,
                            text = "Add Widget",
                            font = font)
    bt_add_widget.grid(row = 0, column = 1, sticky = "news")
    widgets['button'].update({'add_widget': bt_add_widget})
    
    bt_save_project = Button(parent,
                            text = "SAVE PROJECT",
                            bg = 'black',
                            fg = 'white',
                            font = font)
    bt_save_project.grid(row = 0, column = 2, sticky = "news")
    widgets['button'].update({'save_project': bt_save_project})
    
    return widgets
    