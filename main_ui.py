#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 07:52:26 2021

@author: felix
"""
from tkinter import  Tk, Label, Button, Listbox, END, Text, Scrollbar, Frame, N,S,E,W, LEFT, RIGHT, BOTTOM, TOP, X, Y, Checkbutton, IntVar, messagebox, PhotoImage, Menu
from PIL import Image, ImageTk
import math
import projects_ui
import codecs
import ast
import os
import git
class MainApp:
    
    
    DEF_FONT = 'Helvetica 18'
    FONT_B = 'Helvetica 18 bold'
    FONT_L = 'Helvetica 32'
    REPO_PATH = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, name = 'main', columns = 3, language = 'de'):
        self._language = language
        self._sys_content = self._load_data(os.path.join(self.REPO_PATH,'sys_language'), self._language)
        self._name = name
        self._content = self._load_data(os.path.join(self.REPO_PATH,'project_list'), self._language)
        self._main_menu = self._setup_root()
        self._num_col = columns
        self._num_rows = math.ceil(len(self._content)/self._num_col)
        self._widgets = {'label':{}, 'button':{},'listbox':{},'checkbutton':{},'text':{},'scrollbar':{}, 'frame':{} , 'radiobutton':{}, 'plot':{}, 'menu':{}}
        self.create_main_ui()
        self._set_menubar()
        
    def start_app(self):
        self._main_menu.mainloop()
        
                
            
        
    def _load_data(self, data_type, language = 'de'):
    
        path = f'{data_type}/{language}.txt'
        #print(path)
        with codecs.open(path, encoding='utf8') as f:
            lines = f.readlines()
            
        data = ''
        for line in lines:
            data += line
        data = ast.literal_eval(data)
        #print(data)
        return data
    

    def _setup_root(self):
        main_menu = Tk()
        main_menu.attributes("-fullscreen", True)
        main_menu.grid_columnconfigure(0, weight = 1)
        main_menu.grid_rowconfigure(0, weight = 1)
        main_menu.title("MINT Lab")
        
        return main_menu
    
    
    def _update_repo(self, tag_idx=-1):
        #old_tag
        repo = git.Repo(self.REPO_PATH)
        current_tag = repo.git.describe('--tags')
        repo.git.checkout('main')
        repo.remotes.origin.pull()
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        selected_tag = tags[tag_idx]
        if not current_tag==str(selected_tag):
            print(f"Changed from Version: {current_tag} to new Version: {selected_tag}")
            repo.git.checkout(str(selected_tag))
        else:
            print(f"Already checked out Version: {selected_tag}")    
    
    def _set_menubar(self):
        menubar=Menu(self._main_menu)
        
        file_menu=Menu(menubar)
        file_menu.add_command(label="Beenden", command=lambda:self._main_menu.destroy())
        
        menubar.add_cascade(label="Datei", menu=file_menu)
        
        
        update_menu=Menu(menubar)
        update_menu.add_command(label="Update MINT Lab", command=self._update_repo)
        update_menu.add_command(label="Update Betriebssystem")
        update_menu.add_command(label="Betriebssystem Updateinfos")
        
        menubar.add_cascade(label="Updates", menu=update_menu)
        
        self._main_menu.config(menu=menubar)
        
        self._widgets['menu'].update({'main_menubar':menubar})
        
        
        
    
    def _setup_main_frame(self):
        
        main_frame = Frame(self._main_menu)
        main_frame.grid(row = 0, column = 0, sticky = 'nsew')
        main_frame.grid_columnconfigure(0, weight = 1)
        main_frame.grid_columnconfigure(1, weight = 4)
        main_frame.grid_rowconfigure(0, weight = 1)
        self._widgets['frame'].update({'main_frame': main_frame})
        
        project_frame = Frame(self._main_menu, width = self._main_menu.winfo_width())
        project_frame.grid_rowconfigure(0, weight=1)
        project_frame.grid_columnconfigure(0, weight=1)
        project_frame.grid(row=0, column=0, sticky="nsew")
        project_frame.grid_remove()
        self._widgets['frame'].update({'project_frame': project_frame})
        
        
# =============================================================================
#         sys_buttons = Frame(self._widgets['frame']['main_frame'],
#                            borderwidth = 1)
#         sys_buttons.grid(row = 0, column = 0, sticky = 'nsew')
#         sys_buttons.grid_columnconfigure(0, weight = 1)
#         self._widgets['frame'].update({'main_sys_buttons': sys_buttons})
# =============================================================================
        
        
        projects = Frame(self._widgets['frame']['main_frame'])
        projects.grid(row = 0, column = 1, sticky = 'nsew')
        for col in range(self._num_col):
            projects.grid_columnconfigure(col, weight = 1)
        for row in range(1, self._num_rows + 1):
            projects.grid_rowconfigure(row, weight = 1)
        self._widgets['frame'].update({'main_project_list': projects})
        projects.update()
        
    def create_main_ui(self):
        
        self._setup_main_frame()
        
        
# =============================================================================
#         bt_close = Button(self._widgets['frame']['main_sys_buttons'],
#                           text = self._sys_content['bt_exit'],
#                           font = MainApp.FONT_B,
#                           bg = 'red',
#                           command = lambda: self._main_menu.destroy())
#         bt_close.grid(row = 0, column = 0, sticky = 'nsew')
#         self._widgets['button'].update({'main_exit': bt_close})
# =============================================================================
        
        
        
        lbl_1 = Label(self._widgets['frame']['main_project_list'],
                      text = self._sys_content['project_list_header'],
                      font = MainApp.FONT_L)
        lbl_1.grid(row = 0, column = 0, columnspan = self._num_col, sticky ='nsew', pady = (20,20))
        self._widgets['label'].update({'main_project_header': lbl_1})
        
        
        self._create_main_projects_list()
            
    def _create_main_projects_list(self):
        
        aim_height = int((self._widgets['frame']['main_project_list'].winfo_height()/self._num_rows)*.8)
        aim_width = int(self._widgets['frame']['main_project_list'].winfo_width()/self._num_col)
        for idx, entry in enumerate(self._content):
            cur_row = int(idx/self._num_col)
            cur_col = int(idx % self._num_col)
            image_path = f"{self.REPO_PATH}/{entry[3]}/{entry[1]}"
            loaded_img = Image.open(image_path)
            
            scaled = self._scale_img(loaded_img, aim_height, aim_width)
            img = ImageTk.PhotoImage(scaled)
            bt = Button(self._widgets['frame']['main_project_list'],
                        text = entry[0],
                        font = MainApp.FONT_B,
                        image = img,
                        bg = entry[2],
                        compound = TOP,
                        command = lambda i = entry: self._start_project(i[3], i[0]))
            bt.grid(row = cur_row + 1, column = cur_col, sticky = 'nsew', padx = 1, pady = 1)
            self._widgets['button'].update({entry[0]: {'name':bt, 'img': img}})

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
    
    def _start_project(self, name, project_name):
        
        try:
            #print(name)
            selected_data = self._load_data(name, self._language)
            #print("ALL:", selected_data)
            selected_data = selected_data[name]
            #print("PROJECT:", selected_data)
        except:
            messagebox.showinfo("Achtung","Keine Daten verfügbar")
            return
            
        self._widgets['frame']['main_frame'].grid_remove()
        self._widgets['frame']['project_frame'].grid()
        projects_ui.Project(window = self._widgets['frame']['project_frame'],
                            main_widgets = self._widgets,
                            data = selected_data,
                            name = project_name,
                            directory = name,
                            sys_content = self._sys_content,
                            language = self._language)
        
        
        

MainApp(columns = 3, language = 'de').start_app()