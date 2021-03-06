import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext

from combine_files import CombineFiles
from label_datasets import LabelDatasets
# from toolkit.combine_files import CombineFiles
# from toolkit.label_datasets import LabelDatasets

"""
Main application for Wearable Computing Toolkit

Combines multiple data stream csv files into one.
Input list of activities to use when labeling previously created file.

Usage: python app.py
"""

class App(tk.Frame):

	def __init__(self, master=None):
		"""Constructor."""

		super().__init__(master)
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.close_window)

		self.cf_frame = Frame(master, bg="white") # combine files frame
		self.ld_frame = Frame(master, bg="white") # label datasets frame

		self.init_app()
		self.create_combine_files_widgets()
		self.create_label_datasets_widgets()

	def close_window(self):
		"""Close window."""

		self.master.quit()
		self.master.destroy()

	def init_app(self):
		"""Initialize app settings and variables."""

		self.master.title("Combine Files & Label Datasets")
		self.master.config(background = "white") 
		self.master.minsize(930, 300)

		self.src_dir = None			# source directory
		self.dest_dir = None		# destination directory
		self.merged_file = None		# merged csv filename
		self.activities = None		# list of activites as string

	def create_combine_files_widgets(self):
		"""Widgets to combine files from source directory into destination directory."""

		self.cf_frame.pack(side="left", padx=10, pady=10)

		title_label = tk.Label(self.cf_frame, bg="white", text="Merge and align data streams", font=("Arial 18 bold"))
		title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

		### ===== BROWSE SOURCE DIRECTORY ===== ###

		# choose source directory
		src_dir_prompt = tk.Label(self.cf_frame, text="Choose source directory", bg="white")
		src_dir_prompt.grid(row=1, column=0, padx=5, pady=5, sticky=W)

		# browse source directory
		browse_src_btn = tk.Button(self.cf_frame, text="Browse...", command=self.browse_src_dir)
		browse_src_btn.grid(row=1, column=1, padx=5, pady=5)

		# display selected source directory
		self.src_dir_lbl = tk.Label(self.cf_frame, bg="white")
		self.src_dir_lbl.grid(row=1, column=2, padx=5, pady=5)

		### ===== BROWSE DESTINATION DIRECTORY ===== ###

		# choose destination directory
		dest_dir_prompt = tk.Label(self.cf_frame, text="Choose destination directory", bg="white")
		dest_dir_prompt.grid(row=2, column=0, padx=5, pady=5, sticky=W)

		# browse destination directory
		browse_dest_btn = tk.Button(self.cf_frame, text="Browse...", command=self.browse_dest_dir)
		browse_dest_btn.grid(row=2, column=1, padx=5, pady=5)

		# display selected destination directory
		self.dest_dir_lbl = tk.Label(self.cf_frame, bg="white")
		self.dest_dir_lbl.grid(row=2, column=2, padx=5, pady=5)

		### ===== COMBINE FILES ===== ###

		combine_files_btn = tk.Button(self.cf_frame, text="Combine files", command=self.combine_files)
		combine_files_btn.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

		# log for combining files pipeline
		self.combine_files_log = scrolledtext.ScrolledText(self.cf_frame, wrap = tk.WORD, bg="white", width=50, height=5)
		self.combine_files_log.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

	def browse_src_dir(self):
		"""Browse for source directory."""

		# TODO: allow for browsing into subdirectories (ex: "src/short")

		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the source directory')
		self.src_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.src_dir_lbl["text"] = self.src_dir

	def browse_dest_dir(self):
		"""Browse for destination directory."""

		# TODO: allow for browsing into subdirectories (ex: "dest/long")

		selected_dir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select the destination directory')
		self.dest_dir = selected_dir[selected_dir.rfind('/')+1:] + "/"
		self.dest_dir_lbl["text"] = self.dest_dir

	def combine_files(self):
		"""Combine files using src and dest."""

		cf = CombineFiles(self.src_dir, self.dest_dir)
		cf.run()

		# show log for combining files
		for l in cf.log:
			self.combine_files_log.insert(tk.END, l + "\n")
		
		self.combine_files_log.config(state=DISABLED)			# disable editing log box

	def create_label_datasets_widgets(self):
		"""Widgets to label datasets with activities"""

		self.ld_frame.pack(side="right", padx=10, pady=10)

		title_label = tk.Label(self.ld_frame, bg="white", text="Label datasets with activity names", font=("Arial 18 bold"))
		title_label.grid(row=0, column=0, columnspan=3, pady=5)

		### ===== BROWSE FOR MERGED FILE ===== ###

		# browse merged file
		merged_file_bf_btn = tk.Button(self.ld_frame, text="Browse for merged file", command=self.browse_merged_file)
		merged_file_bf_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

		# display selected merged csv file
		self.merged_file_lbl = tk.Label(self.ld_frame, bg="white")
		self.merged_file_lbl.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

		### ===== LIST ALL ACTIVITIES ===== ###

		activities_lbl = tk.Label(self.ld_frame, text="List activities (comma separated)", bg="white")
		activities_lbl.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

		# list of activities
		self.activities_list = tk.Text(self.ld_frame, bg="white", width=50, height=4)
		self.activities_list.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

		# label datasets
		lbl_datasets_btn = tk.Button(self.ld_frame, text="Label datasets", command=self.label_datasets)
		lbl_datasets_btn.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

	def browse_merged_file(self):
		"""Browse for merged file."""

		# TODO: allow for browsing into subdirectories

		selected_file = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the merged file')
		self.merged_file = selected_file[selected_file.rfind("/", 0, selected_file.rfind("/"))+1:]
		self.merged_file_lbl["text"] = self.merged_file

	def label_datasets(self):
		"""Label datasets."""

		self.activities = self.activities_list.get("1.0",END)			# get comma list of activities

		print(len(self.activities))

		# check for activities
		if len(self.activities) == 0:
			messagebox.showinfo("Error", "No activities entered.")

		# call label datasets gui
		ld = LabelDatasets(self.merged_file, self.activities)
		ld.run()
		
		# clear the text box if there are activities
		if len(self.activities) > 1:
			self.activities_list.delete(0, 'end')

if __name__ == '__main__':

	root = tk.Tk()
	app = App(master=root)
	app.mainloop()