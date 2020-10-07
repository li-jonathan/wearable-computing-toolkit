import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os



root = tk.Tk()

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*"))) 
    return filename

def init_window():
    root.title("Wearable Computing Toolkit")
    root.config(background = "white") 
    root.minsize(800, 500)
    merge_files_lbl = Label(root, text="Select files to merge and align data streams: ", bg="white")
    browse_files_btn = Button(root, text = "Browse Files", command = browse_files)
    
    merge_files_lbl.grid(row=1, column=0)
    browse_files_btn.grid(row=1, column=1)

def main():

    init_window()
    root.mainloop()


if __name__ == '__main__':
    main()