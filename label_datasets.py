import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import os
import csv
from tkinter import *
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class LabelDatasets:

	def __init__(self, filename, activities):
		"""Constructor."""
		self.root = tk.Tk()
		self.mainframe = Frame(self.root, bg="white")

		self.merged_filename = filename
		self.activities = [act.strip() for act in activities.split(",")]
		self.headers = []
		self.values = []

		self.activity_ranges = {}

		self.curStart = None
		self.curEnd = None

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
		self.activities_list.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

		confirm_range_btn = tk.Button(self.mainframe, text="Confirm range")
		confirm_range_btn["command"] = self.confirm_range
		confirm_range_btn.grid(row=0, column=4, padx=5, pady=5)

		self.range_lbl = tk.Label(self.mainframe, bg="white")
		self.range_lbl.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

		done_btn = tk.Button(self.mainframe, text=("Apply changes to " + self.merged_filename))
		done_btn["command"] = self.exit
		done_btn.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

	def exit(self):
		print("done with label datasets")
		self.root.destroy()

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

		canvas = FigureCanvasTkAgg(fig, self.mainframe)
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column=0, columnspan=5)

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
