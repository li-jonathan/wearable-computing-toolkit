from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 
from combine_files import CombineFiles
from label_datasets import LabelDatasets
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# usage: python app.py

class App(tk.Frame):

	def __init__(self, master=None):
		"""Constructor."""

		super().__init__(master)
		self.master = master

		self.master.protocol("WM_DELETE_WINDOW", self.close_window)

		self.cf_frame = Frame(master, bg="white") # combine files frame
		self.ld_frame = Frame(master, bg="white") # label datasets frame
		self.ss_frame = Frame(master, bg="white")

		self.init_app()
		self.create_combine_files_widgets()
		self.create_label_datasets_widgets()

	def close_window(self):

		# figure out if span or canvas. might not need either?
		# if hasattr(App, 'span'):
		# 	self.span.remove()
		# if hasattr(App, 'canvas'):
		# 	self.canvas.draw_idle()

		self.master.quit() # NEED
		self.master.destroy()
	
	def init_app(self):
		"""Initialize app settings and variables."""

		self.master.title("Wearable Computing Toolkit")
		self.master.config(background = "white") 
		self.master.minsize(1200, 600)

		self.src_dir = None
		self.dest_dir = None
		self.merged_file = None
		self.activities = None

		self.activities = []
		self.headers = []
		self.values = []

		self.activity_ranges = {}

		self.curStart = None
		self.curEnd = None

	def create_combine_files_widgets(self):
		"""Widgets for combine files from source into destination."""

		self.cf_frame.grid(row=0, column=0, padx=10, pady=10)

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

		self.ld_frame.grid(row=1, column=0, padx=10, pady=10)

		label = tk.Label(self.ld_frame, bg="white", text="Label datasets with activity names", font=("Arial 18 bold"))
		label.grid(row=0, column=0, columnspan=3, pady=5)

		# browse merged file button
		merged_file_bf_btn = tk.Button(self.ld_frame, text="Browse for merged file")
		merged_file_bf_btn["command"] = self.browse_merged_file
		merged_file_bf_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

		# selected merged csv file label
		self.merged_file_lbl = tk.Label(self.ld_frame, bg="white")
		self.merged_file_lbl.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

		# list activities label
		num_activities_lbl = tk.Label(self.ld_frame, text="List activities (comma separated)", bg="white")
		num_activities_lbl.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

		# list of activities
		self.activities_list = tk.Text(self.ld_frame, bg="white", width=50, height=4)
		self.activities_list.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

		# label datasets button
		lbl_datasets_btn = tk.Button(self.ld_frame, text="Label datasets")
		lbl_datasets_btn["command"] = self.label_datasets
		lbl_datasets_btn.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

	def create_gui(self):

		self.ss_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

		select_activity_lbl = tk.Label(self.ss_frame, text="Choose activity", bg="white")
		select_activity_lbl.grid(row=0, column=0, padx=5, pady=5)

		self.activities_list = ttk.Combobox(self.ss_frame, textvariable=tk.StringVar(), state="readonly", width=50)
		self.activities_list['values'] = self.activities
		self.activities_list.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

		confirm_range_btn = tk.Button(self.ss_frame, text="Confirm range")
		confirm_range_btn["command"] = self.confirm_range
		confirm_range_btn.grid(row=0, column=4, padx=5, pady=5)

		self.range_lbl = tk.Label(self.ss_frame, bg="white")
		self.range_lbl.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

		done_btn = tk.Button(self.ss_frame, text=("Apply changes to " + self.merged_file))
		done_btn.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

	def confirm_range(self):
		self.activity_ranges[self.activities_list.get()] = [self.curStart, self.curEnd]
		print(self.activities_list.get() + ": [" + str(self.curStart) + ", " + str(self.curEnd) + "]")

	def create_plot(self):

		hdrs = self.headers
		y = self.values

		fig, ax1 = plt.subplots(figsize=(8, 4))
		ax1.set(facecolor='#FFFFCC')
		ax1.set_xlabel(hdrs[0])
		ax1.set_ylabel("Data Points")

		x = y[0]
		for i in range(1, len(y)):
			ax1.plot(x, y[i], label=hdrs[i])

		self.canvas = FigureCanvasTkAgg(fig, self.ss_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=5)

		def onselect_func(xmin, xmax):
			indmin, indmax = np.searchsorted(self.values[0], (xmin, xmax))
			indmax = min(len(self.values[0]) - 1, indmax)

			thisx = self.values[0][indmin:indmax]
			thisy = self.values[indmin:indmax]

			self.curStart = thisx[0]
			self.curEnd = thisx[-1]
			self.range_lbl["text"] = "[" + str(self.curStart) + ", " + str(self.curEnd) + "]"

		self.span = SpanSelector(ax1, onselect=onselect_func, direction='horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))
	
	def read_file(self):
		with open(self.merged_file,'r') as csvfile:
			plots = csv.reader(csvfile, delimiter=',')

			for hdr in next(plots):
				self.headers.append(hdr)
				self.values.append([])

			for row in plots:
				for i in range(len(self.headers)):
					self.values[i].append(float(row[i]))

	def browse_merged_file(self):
		"""Browse for source directory."""

		selected_file = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the merged file')
		self.merged_file = selected_file[selected_file.rfind("/", 0, selected_file.rfind("/"))+1:]
		self.merged_file_lbl["text"] = self.merged_file

	def label_datasets(self):
		self.activities = self.activities_list.get("1.0",END)
		self.activities = [act.strip() for act in self.activities.split(",")]
		# ld = LabelDatasets(self.merged_file, self.activities)
		# ld.run()
		self.read_file()
		self.create_gui()
		self.create_plot()


if __name__ == '__main__':

	root = tk.Tk()
	app = App(master=root)
	app.mainloop()