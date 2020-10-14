from tkinter import *
import tkinter as tk
from tkinter import filedialog 

import os

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.frame1 = Frame(master)
        self.frame2 = Frame(master)
        self.frame3 = Frame(master)
        self.frame4 = Frame(master)

        self.srcdir = None
        self.destdir = None

        self.pack()
        self.build_app()
        self.create_feature1_widgets()

    def build_app(self):
        self.master.title("Weable Computing Toolkit")
        self.master.config(background = "white") 
        self.master.minsize(600, 300)


    def create_feature1_widgets(self):
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

        # choose src dir label
        self.srcprompt_lbl = tk.Label(self.frame1, bg="white")
        self.srcprompt_lbl["text"] = "Choose source directory"
        self.srcprompt_lbl.pack(side="left")

        # browse button
        self.bf_btn = tk.Button(self.frame1)
        self.bf_btn["text"] = "Browse..."
        self.bf_btn["command"] = self.browse_dir
        self.bf_btn.pack(side="right")

        # display selected src dir
        self.srcdir_lbl = tk.Label(self.frame2, bg="white")
        self.srcdir_lbl["text"] = "Source directory: ..."
        self.srcdir_lbl.pack()

        # enter dest dir label
        self.destprompt_lbl = tk.Label(self.frame3, bg="white")
        self.destprompt_lbl["text"] = "Enter destination directory:"
        self.destprompt_lbl.pack(side="left")

        # confirm entered dest dir
        self.destdir_btn = tk.Button(self.frame3)
        self.destdir_btn["text"] = "Enter"
        self.destdir_btn["command"] = self.get_destdir
        self.destdir_btn.pack(side="right")

        # entry field for dest dir
        self.destdir_ety = tk.Entry(self.frame3)
        self.destdir_ety.pack(side="right")

        # display dest dir
        self.destdir_lbl = tk.Label(self.frame4, bg="white")
        self.destdir_lbl["text"] = "Destination directory: ..."
        self.destdir_lbl.pack()


    def browse_dir(self):
        dirname= filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title='Please select a directory')
        # TODO: error check dirname
        self.srcdir = dirname[dirname.rfind('/'):]
        self.srcdir_lbl["text"] = "Source directory: " + self.srcdir

    def get_destdir(self):
        self.destdir = self.destdir_ety.get()
        if self.destdir == '':
            self.destdir_lbl["text"] = "Destination directory: ..."
        else:
            self.destdir_lbl["text"] = "Destination directory: " + self.destdir

if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(master=root)
    app.mainloop()