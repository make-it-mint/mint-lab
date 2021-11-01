# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:57:02 2021

@author: felix
"""
from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Radiobutton, Checkbutton, StringVar, IntVar, messagebox, PhotoImage

def create_widgets(parent, widgets, font):
    frame_nav = Frame(parent)
    frame_nav.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", pady = 4)
    widgets['frame'].update({'nav': frame_nav})
    widgets = set_nav_widgets(widgets['frame']['nav'], widgets, font)
    
    return widgets

def set_nav_widgets(parent, widgets, font):
    
    bt_new_project = Button(parent,
                            text = "NEW Project",
                            font = font)
    bt_new_project.grid(row = 0, column = 0, sticky = "nsew")
    widgets['button'].update({'nav_new_project': bt_new_project})
    
    bt_load_project = Button(parent,
                            text = "LOAD Project",
                            font = font)
    bt_load_project.grid(row = 0, column = 1, sticky = "nsew")
    widgets['button'].update({'nav_load_project': bt_load_project})
    
    bt_back = Button(parent,
                            text = "<--",
                            font = font)
    bt_back.grid(row = 0, column = 2, sticky = "nsew")
    widgets['button'].update({'nav_back': bt_back})
    
    lbl_page = Label(parent,
                            text = "0/0",
                            font = font)
    lbl_page.grid(row = 0, column = 3, sticky = "nsew")
    widgets['label'].update({'nav_page': lbl_page})
    
    bt_next = Button(parent,
                            text = "-->",
                            font = font)
    bt_next.grid(row = 0, column = 4, sticky = "nsew")
    widgets['button'].update({'nav_next': bt_next})
    
    bt_preview = Button(parent,
                            text = "Preview",
                            font = font)
    bt_preview.grid(row = 0, column = 5, sticky = "nsew")
    widgets['button'].update({'nav_preview': bt_preview})
    
    bt_add_page = Button(parent,
                            text = "Add Page",
                            font = font)
    bt_add_page.grid(row = 0, column = 6, sticky = "nsew")
    widgets['button'].update({'nav_add_page': bt_add_page})
    
    bt_delete_page = Button(parent,
                            text = "Delete Page",
                            font = font)
    bt_delete_page.grid(row = 0, column = 7, sticky = "nsew")
    widgets['button'].update({'nav_del_page': bt_delete_page})
    
    return widgets