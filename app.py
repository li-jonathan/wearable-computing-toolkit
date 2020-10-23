from tkinter import *
import tkinter as tk
from tkinter import filedialog 
from combine_files import CombineFiles
import os

# usage: python app.py

class App(tk.Frame):

	def __init__(self, master=None):
		"""Constructor."""

		super().__init__(master)
		self.master = master

		self.cf_frame = Frame(master, bg="white") # combine files frame
		self.ld_frame = Frame(master, bg="white") # label datasets frame

		self.init_app()
		self.create_combine_files_widgets()
		self.create_label_datasets_widgets()

	def init_app(self):
		"""Initialize app settings and variables."""

		self.master.title("Wearable Computing Toolkit")
		self.master.config(background = "white") 
		p1 = PhotoImage(file = 'icon.png') 
		self.master.iconphoto(False, p1)
		self.master.minsize(850, 300)

		self.src_dir = None
		self.dest_dir = None
		self.merged_file = None


	def create_combine_files_widgets(self):
		"""Widgets for combine files from source into destination."""

		self.cf_frame.pack(side="left", padx=10, pady=10)

		### FIND SOURCE DIRECTORY ###

		label = tk.Label(self.cf_frame, bg="white", text="Merge and align data streams", font=("Arial 18 bold"))
		label.grid(row=0, column=0, columnspan=3, pady=5)

		# choose src dir label
		src_dir_prompt = tk.Label(self.cf_frame, text="Choose source directory", bg="white")
		src_dir_prompt.grid(row=1, column=0, padx=5, pady=5, sticky=W)

		# browse src dir button
		src_bf_btn = tk.Button(self.cf_frame, text="Browse...")
		src_bf_btn["command"] = self.browse_src_dir
		src_bf_btn.grid(row=1, column=1, padx=5, pady=5)

		# display selected src dir
		self.src_dir_lbl = tk.Label(self.cf_frame, bg="white")
		self.src_dir_lbl.grid(row=1, column=2, padx=5, pady=5)

		### FIND DESTINATION DIRECTORY ###

		# choose dest dir label
		dest_dir_prompt = tk.Label(self.cf_frame, text="Choose destination directory", bg="white")
		dest_dir_prompt.grid(row=2, column=0, padx=5, pady=5, sticky=W)

		# browse dest dir button
		dest_bf_btn = tk.Button(self.cf_frame, text="Browse...")
		dest_bf_btn["command"] = self.browse_dest_dir
		dest_bf_btn.grid(row=2, column=1, padx=5, pady=5)

		# display selected dest dir
		self.dest_dir_lbl = tk.Label(self.cf_frame, bg="white")
		self.dest_dir_lbl.grid(row=2, column=2, padx=5, pady=5)

		### COMBINE FILES ###

		combine_files_btn = tk.Button(self.cf_frame, text="Combine files")
		combine_files_btn["command"] = self.combine_files
		combine_files_btn.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

		self.combine_files_log = tk.Text(self.cf_frame, bg="white", width=50, height=5)
		self.combine_files_log.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

	def browse_src_dir(self):
		"""Browse for source directory."""

		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the source directory')
		self.src_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.src_dir_lbl["text"] = self.src_dir

	def browse_dest_dir(self):
		"""Browse for destination directory."""

		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the destination directory')
		self.dest_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.dest_dir_lbl["text"] = self.dest_dir

	def combine_files(self):
		"""Combine files using src and dest."""

		cf = CombineFiles(self.src_dir, self.dest_dir)
		cf.run()

		# show logs for combining files
		for l in cf.log:
			self.combine_files_log.insert(tk.END, l + "\n");
		self.combine_files_log.config(state=DISABLED)


	def create_label_datasets_widgets(self):
		"""Widgets to label datasets with activities"""

		self.ld_frame.pack(side="right", padx=10, pady=10)

		label = tk.Label(self.ld_frame, bg="white", text="Label datasets with activity names", font=("Arial 18 bold"))
		label.grid(row=0, column=0, columnspan=3, pady=5)

		# browse merged file button
		merged_file_bf_btn = tk.Button(self.ld_frame, text="Browse for merged file")
		merged_file_bf_btn["command"] = self.browse_merged_file
		merged_file_bf_btn.grid(row=1, column=1, padx=5, pady=5)

		self.merged_file_lbl = tk.Label(self.ld_frame, bg="white")
		self.merged_file_lbl.grid(row=2, column=1, padx=5, pady=5)

	def browse_merged_file(self):
		"""Browse for source directory."""

		selected_file = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the merged file')
		self.merged_file = selected_file[selected_file.rfind('/')+1:]
		self.merged_file_lbl["text"] = self.merged_file

if __name__ == '__main__':
	root = tk.Tk()
	app = App(master=root)
	app.mainloop()