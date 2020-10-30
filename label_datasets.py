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

		self.topframe = Frame(self.root, bg="white") # combine files frame

		self.merged_filename = filename
		self.activities = [act.strip() for act in activities.split(",")]
		self.headers = []
		self.values = []

	def init_app(self):
		"""Initialize app settings and variables."""

		self.root.title("Label Datasets")
		self.root.config(background = "white") 
		self.root.minsize(900, 500)

	def create_gui(self):

		self.topframe.pack(side="top", padx=10, pady=10)

		select_activity_lbl = tk.Label(self.topframe, text="Choose activity", bg="white")
		select_activity_lbl.grid(row=0, column=0, padx=5, pady=5)

		activities_list = ttk.Combobox(self.topframe, textvariable=tk.StringVar(), state="readonly")
		activities_list['values'] = self.activities
		activities_list.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

		select_range_btn = tk.Button(self.topframe, text="Select range")
		select_range_btn['commmand'] = self.create_plot
		select_range_btn.grid(row=0, column=3, padx=5, pady=5)

		confirm_range_btn = tk.Button(self.topframe, text="Confirm range")
		confirm_range_btn.grid(row=0, column=4, padx=5, pady=5)

	def create_plot(self):

		print(self.headers)
		print(self.values)

		hdrs = self.headers
		y = self.values

		fig, ax1 = plt.subplots(figsize=(10, 5))
		ax1.set(facecolor='#FFFFCC')
		ax1.set_title('click and drag testing')
		ax1.set_xlabel(hdrs[0])
		ax1.set_ylabel("data points")

		x = y[0]
		for i in range(1, len(y)):
			ax1.plot(x, y[i], label=hdrs[i])

		span = SpanSelector(ax1, self.onselect, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))

		canvas = FigureCanvasTkAgg(fig, self.topframe)
		canvas.draw()
		canvas.get_tk_widget().grid(row=1, column=0, columnspan=5)

		canvas.mpl_connect('button_press_event',span)
	
	def read_file(self):
		with open(self.merged_filename,'r') as csvfile:
			plots = csv.reader(csvfile, delimiter=',')

			for hdr in next(plots):
				self.headers.append(hdr)
				self.values.append([])

			for row in plots:
				for i in range(len(self.headers)):
					self.values[i].append(float(row[i]))

	def onselect(self, xmin, xmax):

		indmin, indmax = np.searchsorted(self.values[0], (xmin, xmax))
		indmax = min(len(self.values[0]) - 1, indmax)

		thisx = self.values[0][indmin:indmax]
		thisy = self.values[indmin:indmax]

		start = thisx[0]
		end = thisx[-1]
		print("start=", start)
		print("end=", end)


	def run(self):
		self.init_app()
		self.read_file()
		self.create_gui()
		self.root.mainloop()
