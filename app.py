from tkinter import *
import tkinter as tk
from tkinter import filedialog 
from combine_files2 import CombineFiles
import os

class GUI(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master

		self.func1_frame = Frame(master, bg="white")

		self.src_dir = None
		self.dest_dir = None

		self.build_app()
		self.create_feature1_widgets()

	def combine_files(self):
		cf = CombineFiles(self.src_dir, self.dest_dir)
		cf.run()

		# combine files run log
		for l in cf.log:
			self.combine_files_log.insert(tk.END, l + "\n");
		self.combine_files_log.config(state=DISABLED)

	def build_app(self):
		self.master.title("Wearable Computing Toolkit")
		self.master.config(background = "white") 
		p1 = PhotoImage(file = 'icon.png') 
		self.master.iconphoto(False, p1)
		self.master.minsize(500, 300)


	def create_feature1_widgets(self):
		
		# self.func1_frame.grid(row=0, column=0, padx=10, pady=10)
		self.func1_frame.pack(pady=10)

		### SOURCE DIRECTORY ###

		# choose src dir label
		self.src_dir_prompt = tk.Label(self.func1_frame, bg="white")
		self.src_dir_prompt["text"] = "Choose source directory"
		self.src_dir_prompt.grid(row=0, column=0, padx=5, pady=5, sticky=W)

		# browse src dir button
		self.src_bf_btn = tk.Button(self.func1_frame)
		self.src_bf_btn["text"] = "Browse..."
		self.src_bf_btn["command"] = self.browse_src_dir
		self.src_bf_btn.grid(row=0, column=1, padx=5, pady=5)

		# display selected src dir
		self.src_dir_lbl = tk.Label(self.func1_frame, bg="white")
		self.src_dir_lbl.grid(row=0, column=2, padx=5, pady=5)

		### DESTINATION DIRECTORY ###

		# choose dest dir label
		self.dest_dir_prompt = tk.Label(self.func1_frame, bg="white")
		self.dest_dir_prompt["text"] = "Choose destination directory"
		self.dest_dir_prompt.grid(row=1, column=0, padx=5, pady=5, sticky=W)

		# browse dest dir button
		self.dest_bf_btn = tk.Button(self.func1_frame)
		self.dest_bf_btn["text"] = "Browse..."
		self.dest_bf_btn["command"] = self.browse_dest_dir
		self.dest_bf_btn.grid(row=1, column=1, padx=5, pady=5)

		# display selected dest dir
		self.dest_dir_lbl = tk.Label(self.func1_frame, bg="white")
		self.dest_dir_lbl.grid(row=1, column=2, padx=5, pady=5)

		### COMBINE FILES ###

		# combine files button
		self.combine_files_btn = tk.Button(self.func1_frame)
		self.combine_files_btn["text"] = "Combine files"
		self.combine_files_btn["command"] = self.combine_files
		self.combine_files_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

		self.combine_files_log = tk.Text(self.func1_frame, bg="white", width=50, height=5)
		self.combine_files_log.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

	def browse_src_dir(self):
		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the source directory')
		self.src_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.src_dir_lbl["text"] = self.src_dir

	def browse_dest_dir(self):
		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the destination directory')
		self.dest_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.dest_dir_lbl["text"] = self.dest_dir

if __name__ == '__main__':
	root = tk.Tk()
	app = GUI(master=root)
	app.mainloop()