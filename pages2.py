from tkinter import *
from itertools import cycle
root = Tk()
root.geometry('400x400')

# these two configs cause the grid content to expand and allows us to use 
# anchor='nswe'. you MUST call these on each grid item allowed to expand.
root.grid_columnconfigure(0, weight=1)  
root.grid_rowconfigure(0, weight=1)     
frames = []
for color in ['red', 'green', 'blue', 'white', 'orange', 'pink']:
    f = Frame(root, background=color)
    f.grid(sticky='nwse', row=0, column=0) 
    frames.append(f)
iter_frames = cycle(frames)

# calling .tkraise on a gridded wiget will make it visible again, but keep 
# the object alive, so you can re-raise it. try adding text on each raise
Button(text='Next color', command=lambda:next(iter_frames).tkraise()).grid(row=1)
root.mainloop()