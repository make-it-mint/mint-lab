# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:17:35 2021

@author: felix
"""

from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Radiobutton, Checkbutton, StringVar, IntVar, messagebox, PhotoImage

def create_widgets(parent, widgets, font):
    frame_list = Frame(parent)
    frame_list.grid(row = 2, column = 1, sticky = "nsew", pady = 4)
    widgets['frame'].update({'frame_list': frame_list})
    widgets = set_list_widgets(frame_list, widgets, font)
    
    return widgets


def set_list_widgets(parent, widgets, font):
    l_box_widgets = Listbox(parent,
                            width = 30,
                            height = 20,
                            font = font)
    l_box_widgets.grid(row = 0, column = 0, sticky = "nsew")
    widgets['listbox'].update({'widget_list': l_box_widgets})
    
    button_show_selected_widget = Button(parent,
                            text = "Show Selected",
                            font = font)
    button_show_selected_widget.grid(row = 1, column = 0, sticky = "nsew")
    widgets['button'].update({'show_selected_widget': button_show_selected_widget})
    
    button_delete_selected_widget = Button(parent,
                            text = "Delete Selected",
                            font = font)
    button_delete_selected_widget.grid(row = 2, column = 0, sticky = "nsew")
    widgets['button'].update({'delete_selected_widget': button_delete_selected_widget})
    
    return widgets