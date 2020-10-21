from tkinter import *
import tkinter as tk
from tkinter import filedialog 
from combine_files2 import CombineFiles
import os

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Wearable Computing Toolkit")
        self.config(background = "white")
        p1 = PhotoImage(file = 'icon.png') 
        self.iconphoto(False, p1)
        self.minsize(450, 300)

        container = tk.Frame(self)
        container.config(background="white")
        container.pack(fill="both", expand=True)

        self.frames = {}
        self.frames["MainMenu"] = MainMenu(parent=container, controller=self)
        self.frames["PageOne"] = PageOne(parent=container, controller=self)

        self.frames["MainMenu"].grid(row=0, column=0, sticky="NSEW")
        self.frames["PageOne"].grid(row=0, column=0, sticky="NSEW")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background="white")

        combine_files_func_btn = tk.Button(self, text="Merge and align data streams", command=lambda: controller.show_frame("PageOne"))
        combine_files_func_btn.pack(pady=5)

        lbl_datasets_func_btn = tk.Button(self, text="Label datasets with activity names", command=lambda: controller.show_frame("PageOne"))
        lbl_datasets_func_btn.pack(pady=5)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background="white")

        self.src_dir = None
        self.dest_dir = None

        self.create_feature1_widgets()



    def combine_files(self):
        cf = CombineFiles(self.src_dir, self.dest_dir)
        cf.run()

        # combine files run log
        for l in cf.log:
            self.combine_files_log.insert(tk.END, l + "\n");
        self.combine_files_log.config(state=DISABLED)

    def create_feature1_widgets(self):
        
        ### SOURCE DIRECTORY ###

        # choose src dir label
        self.src_dir_prompt = tk.Label(self, bg="white")
        self.src_dir_prompt["text"] = "Choose source directory"
        self.src_dir_prompt.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # browse src dir button
        self.src_bf_btn = tk.Button(self)
        self.src_bf_btn["text"] = "Browse..."
        self.src_bf_btn["command"] = self.browse_src_dir
        self.src_bf_btn.grid(row=0, column=1, padx=5, pady=5)

        # display selected src dir
        self.src_dir_lbl = tk.Label(self, bg="white")
        self.src_dir_lbl.grid(row=0, column=2, padx=5, pady=5)

        ### DESTINATION DIRECTORY ###

        # choose dest dir label
        self.dest_dir_prompt = tk.Label(self, bg="white")
        self.dest_dir_prompt["text"] = "Choose destination directory"
        self.dest_dir_prompt.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # browse dest dir button
        self.dest_bf_btn = tk.Button(self)
        self.dest_bf_btn["text"] = "Browse..."
        self.dest_bf_btn["command"] = self.browse_dest_dir
        self.dest_bf_btn.grid(row=1, column=1, padx=5, pady=5)

        # display selected dest dir
        self.dest_dir_lbl = tk.Label(self, bg="white")
        self.dest_dir_lbl.grid(row=1, column=2, padx=5, pady=5)

        ### COMBINE FILES ###

        # combine files button
        self.combine_files_btn = tk.Button(self)
        self.combine_files_btn["text"] = "Combine files"
        self.combine_files_btn["command"] = self.combine_files
        self.combine_files_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.combine_files_log = tk.Text(self, bg="white", width=50, height=5)
        self.combine_files_log.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.main_menu_btn = tk.Button(self, text="Main Menu", command=lambda: self.controller.show_frame("MainMenu"))
        self.main_menu_btn.grid(row=4, column=2, pady=5, padx=5)


    def browse_src_dir(self):
        selected_dir = filedialog.askdirectory(parent=self, initialdir=os.getcwd(), title='Please select the source directory')
        self.src_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
        self.src_dir_lbl["text"] = self.src_dir

    def browse_dest_dir(self):
        selected_dir = filedialog.askdirectory(parent=self, initialdir=os.getcwd(), title='Please select the destination directory')
        self.dest_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
        self.dest_dir_lbl["text"] = self.dest_dir

if __name__ == "__main__":
    app = App()
    app.mainloop()