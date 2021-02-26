import numpy as np
import pandas as pd
import os
import csv

# tkinter imports
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox 

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
		
		self.main_frame = Frame(self.root, bg="white")				# main frame
		self.activities_frame = Frame(self.main_frame, bg="white")	# activities frame		
		self.range_edits_frame = Frame(self.main_frame, bg="white")	# edit options frame

		self.merged_filename = filename
		self.activities = [act.strip() for act in activities.split(",")]

		self.headers = []
		self.values = []

		self.activity_ranges = {}	# activities mapped with a list of their ranges

		self.cur_start = None		# current start of range selected
		self.cur_end = None			# current end of range selected
		self.cur_ranges = []		# list of all current selected ranges

	def activity_in_range(self, time):
		"""Returns the activity that the given time falls into."""
		
		act = "Unknown"

		# k = activity
		# v = list of ranges
		for k,v in self.activity_ranges.items():
			for i in range(0, len(v)):
				start = float(v[i][0])
				end = float(v[i][1])
				if float(time) >= start and float(time) <= end:
					act = k
		
		return act

	def assign_activities(self, times):
		"""Creates list of activities instead of times."""

		acts = []
		for t in times:
			acts.append(self.activity_in_range(t))
		return acts

	def close_window(self):
		"""Close window."""

		self.root.quit()
		self.root.destroy()
	
	def confirm_range(self):
		"""Confirm the selected ranges to assign to the activity."""

		current_activity = self.activities_list.get()
		if len(current_activity) == 0:
			messagebox.showinfo("Error", "No activity selected.")
			return

		if current_activity not in self.activity_ranges:
			self.activity_ranges[current_activity] = []

		# add the ranges selected to activity 
		for r in self.cur_ranges:
			self.activity_ranges[current_activity].append(r)

		self.cur_ranges = []
		self.current_range_selections.delete('1.0', END)
		self.update_range_list()

	def create_gui(self):
		"""Create widgets."""

		self.main_frame.pack(side="top", padx=10, pady=10)

		### ACTIVITY SELECTION ###

		choose_activity_lbl = tk.Label(self.activities_frame, text="Choose activity", bg="white")
		choose_activity_lbl.grid(row=0, column=0, padx=5, pady=5)

		self.activities_list = ttk.Combobox(self.activities_frame, textvariable=tk.StringVar(), state="readonly", width=50)
		self.activities_list['values'] = self.activities
		self.activities_list.grid(row=0, column=1, padx=5, pady=5)

		self.activities_frame.grid(row=0, column=0)

		### RANGE EDITING/CONFIRMING ###

		# current selected range(s) for selected activity
		self.current_range_selections = scrolledtext.ScrolledText(self.range_edits_frame, wrap = tk.WORD, bg="white", width=60, height=7)
		self.current_range_selections.grid(row=0, column=0, rowspan=3, padx=5, pady=5)

		# choose index of which range to delete
		self.delete_entry = tk.Entry(self.range_edits_frame, bg="white", width=7)
		self.delete_entry.grid(row=0, column=1, padx=5, pady=5)

		# confirm range to delete
		confirm_delete_btn = tk.Button(self.range_edits_frame, text="Confirm delete")
		confirm_delete_btn["command"] = self.remove_range_selection
		confirm_delete_btn.grid(row=1, column=1, padx=5, pady=5)

		# confirm selected ranges to add to all ranges
		confirm_range_btn = tk.Button(self.range_edits_frame, text="Confirm range(s)")
		confirm_range_btn["command"] = self.confirm_range
		confirm_range_btn.grid(row=2, column=1, padx=5, pady=5)

		self.range_edits_frame.grid(row=1, column=0)

		### SELECTED RANGES ###

		self.all_ranges = scrolledtext.ScrolledText(self.main_frame, wrap = tk.WORD, bg="white", width=40, height=15)
		self.all_ranges.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

		### APPLY CHANGES ###

		done_btn = tk.Button(self.main_frame, text=("Apply changes to " + self.merged_filename))
		done_btn["command"] = self.label_file
		done_btn.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

	def create_plot(self):
		"""Read csv file and create plot."""

		fig, ax1 = plt.subplots(figsize=(12, 4))

		# figure properties
		ax1.set(facecolor='#FFFFCC')
		ax1.set_xlabel(self.headers[0])
		ax1.set_ylabel("Data Points")

		# plot values
		x = self.values[0]
		for i in range(1, len(self.values)):
			ax1.plot(x, self.values[i], label=self.headers[i])

		# grid canvas on frame
		canvas = FigureCanvasTkAgg(fig, self.main_frame)
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)

		def onselect_func(xmin, xmax):
			indmin, indmax = np.searchsorted(self.values[0], (xmin, xmax))
			indmax = min(len(self.values[0]) - 1, indmax)

			thisx = self.values[0][indmin:indmax]
			# thisy = self.values[indmin:indmax] # unused right now but may use in future

			self.cur_start = thisx[0]
			self.cur_end = thisx[-1]
			self.cur_ranges.append([self.cur_start, self.cur_end])

			self.update_ranges()

		self.span = SpanSelector(ax1, onselect=onselect_func, direction='horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))

		def init_app(self):
		"""Initialize app settings and variables."""

		self.root.title("Label Datasets")
		self.root.config(background = "white") 
		self.root.minsize(1200, 700)

	def label_file(self):
		"""Label csv file with associated activities."""

		# debugging: print activites and its ranges
		# for k,v in self.activity_ranges.items():
		# 	print("activity=" + str(k))
		# 	for i in range(0, len(v)):
		# 		print(v[i])

		# TODO: validate csv is not empty?

		# read csv file and get first header
		data = pd.read_csv(self.merged_filename)
		output_filename = self.merged_filename.replace(".csv", "-output.csv")
		header1 = list(data.columns.values)[0]

		# get list of activities at each time
		activities_to_write = self.assign_activities(data[header1])

		# write those activities to new csv file
		data['Activity'] = activities_to_write
		data.to_csv(output_filename, index=False)
		
		self.root.quit()
		self.root.destroy()

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

	def remove_range_selection(self):
		"""Remove a range from the current selection."""

		# check there was index entered
		if len(self.delete_entry.get()) == 0:
			messagebox.showinfo("Error", "No index entered.")
			self.delete_entry.delete(0, 'end')
			return
		
		try:
			idx = int(self.delete_entry.get())

			# check valid index
			if idx < 0 or idx >= len(self.cur_ranges):
				messagebox.showinfo("Error", "Index out of range.")
				self.delete_entry.delete(0, 'end')
				return

			# remove the range from current selections
			element_to_remove = self.cur_ranges[idx]
			self.cur_ranges.remove(element_to_remove)

			# clear entry and update current selection box
			self.delete_entry.delete(0, 'end')
			self.update_ranges()

		except ValueError:
			messagebox.showinfo("Error", "Must be a number.")
			self.delete_entry.delete(0, 'end')
			return

	def update_ranges(self):
		"""Update the current range selections text box."""

		# TODO: error prevention if user tries to manually edit text box

		self.current_range_selections.delete('1.0', END)
		for i in range(0, len(self.cur_ranges)):
			self.current_range_selections.insert(END, str(i) + ": " + str(self.cur_ranges[i]) + "\n")

	def update_range_list(self):
		"""Update the list of all confirmed ranges."""
		
		self.all_ranges.delete("1.0","end")

		for k, v in self.activity_ranges.items():
			self.all_ranges.insert(tk.END, str(k) + "\n")
			for i in range(0, len(v)):
				entry = str(i) + ": " + str(v[i])
				self.all_ranges.insert(tk.END, entry + "\n")

	def run(self):
		self.init_app()
		self.read_file()
		self.create_gui()
		self.create_plot()
		self.root.mainloop()
