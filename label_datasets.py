import numpy as np
import os
import csv

# tkinter imports
from tkinter import *
import tkinter as tk
from tkinter import ttk

# matplotlib imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

class LabelDatasets:

	def __init__(self, filename, activities):
		"""Constructor."""
		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.close_window)
		
		self.mainframe = Frame(self.root, bg="white")

		self.merged_filename = filename
		self.activities = [act.strip() for act in activities.split(",")]
		self.headers = []
		self.values = []

		self.activity_ranges = {}

		self.curStart = None
		self.curEnd = None
		self.curRanges = []

	def close_window(self):
		"""Close window."""

		self.root.quit()
		self.root.destroy()

	def init_app(self):
		"""Initialize app settings and variables."""

		self.root.title("Label Datasets")
		self.root.config(background = "white") 
		self.root.minsize(900, 550)

	def create_gui(self):

		self.mainframe.pack(side="top", padx=10, pady=10)

		select_activity_lbl = tk.Label(self.mainframe, text="Choose activity", bg="white")
		select_activity_lbl.grid(row=0, column=0, padx=5, pady=5)

		self.activities_list = ttk.Combobox(self.mainframe, textvariable=tk.StringVar(), state="readonly", width=50)
		self.activities_list['values'] = self.activities
		self.activities_list.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

		self.ranges = tk.Text(self.mainframe, bg="white", width=40, height=25)
		self.ranges.grid(row=0, column=4, rowspan=3, padx=5, pady=5)

		confirm_range_btn = tk.Button(self.mainframe, text="Confirm range")
		confirm_range_btn["command"] = self.confirm_range
		confirm_range_btn.grid(row=1, column=2, padx=5, pady=5)

		self.range_lbl = tk.Label(self.mainframe, bg="white")
		self.range_lbl.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

		# done_btn = tk.Button(self.mainframe, text=("Apply changes to " + self.merged_filename))
		# done_btn["command"] = self.label_file
		# done_btn.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

	def confirm_range(self):

		current_activity = self.activities_list.get()

		if current_activity not in self.activity_ranges:
			self.activity_ranges[current_activity] = []

		for l in self.curRanges:
			self.activity_ranges[current_activity].append(l)

		self.curRanges = []
		self.range_lbl["text"] = ""

		self.update_range_list()

	def create_plot(self):

		fig, ax1 = plt.subplots(figsize=(8, 4))
		ax1.set(facecolor='#FFFFCC')
		ax1.set_xlabel(self.headers[0])
		ax1.set_ylabel("Data Points")

		x = self.values[0]
		for i in range(1, len(self.values)):
			ax1.plot(x, self.values[i], label=self.headers[i])

		canvas = FigureCanvasTkAgg(fig, self.mainframe)
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column=0, columnspan=4)

		def onselect_func(xmin, xmax):
			indmin, indmax = np.searchsorted(self.values[0], (xmin, xmax))
			indmax = min(len(self.values[0]) - 1, indmax)

			thisx = self.values[0][indmin:indmax]
			thisy = self.values[indmin:indmax]

			self.curStart = thisx[0]
			self.curEnd = thisx[-1]

			self.curRanges.append([self.curStart, self.curEnd])

			if len(self.range_lbl["text"]) == 0:
				self.range_lbl["text"] = "[" + str(self.curStart) + ", " + str(self.curEnd) + "]"
			else:
				self.range_lbl["text"] = self.range_lbl["text"] + "\n[" + str(self.curStart) + ", " + str(self.curEnd) + "]"

		self.span = SpanSelector(ax1, onselect=onselect_func, direction='horizontal', useblit=True, span_stays=True, rectprops=dict(alpha=0.5, facecolor='red'))

	def update_range_list(self):
		
		self.ranges.delete("1.0","end")

		for k, v in self.activity_ranges.items():
			print(k)
			self.ranges.insert(tk.END, str(k) + "\n")
			for i in range(0, len(v)):
				entry = str(i) + ": " + str(v[i])
				print(entry)
				self.ranges.insert(tk.END, entry + "\n")
	
	def label_file(self):
		# label csv file with activities
		self.close_window
	
	def read_file(self):
		"""Reads file to find headers and values."""

		with open(self.merged_filename,'r') as csvfile:
			plots = csv.reader(csvfile, delimiter=',')

			for hdr in next(plots):
				self.headers.append(hdr)
				self.values.append([])

			for row in plots:
				for i in range(len(self.headers)):
					self.values[i].append(float(row[i]))

	def run(self):
		self.init_app()
		self.read_file()
		self.create_gui()
		self.create_plot()
		self.root.mainloop()
