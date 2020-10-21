import pandas as pd
import os
import sys
import argparse

"""
MBientDataFile class
From: https://git.cs.jmu.edu/WearableComputing/ActivityRecognition/blob/data_tools/Python/tools/combine_files.py
"""

#### Begin MBientDataFile Class ####

class MBientDataFile:

	filePath=None
	sensorType=None
	sampleRate=None
	sensorName=None
	captureDateTime=None
	MAC=None
	startTime=None
	_epoch_column_label='epoc (ms)'

	def _calc_sample_rate_and_start_time(self):
        # read the first 10 rows so we can get the sample rate
        #TODO: make this not hard coded. Will error is file is less than numRows
		numRows = 100
		data = pd.read_csv(self.filePath, nrows=numRows)
		times = data[self._epoch_column_label]
		deltas = times.diff()

		# average period between samples in milliseconds
		totalPeriod = deltas.sum(skipna=True) / (numRows - 1)

		self.sampleRate = 1 / (totalPeriod / 1000)
		self.startTime=times.get(0)


	def __init__(self,file_path):
		self.filePath=file_path
		(head,tail)=os.path.split(file_path)
		splits = tail.split("_")

		self.sensorName=splits[0]
		self.captureDateTime=splits[1]
		self.MAC=splits[2]
		self.sensorType=splits[3].split(".")[0]

		self._calc_sample_rate_and_start_time()

	def generate_data_frame(self):
		df = pd.read_csv(self.filePath)

		#delete un-needed column

		del df['timestamp (-0400)'] #delete UTC timestamp column

		#TODO: check to see which column exixts and then delete it based upon time
		#del df['timestamp (-0500)']  # delete UTC timestamp column

		del df['elapsed (s)'] #delete elapse column

        #rename data columns to append sensor name
		if self.sensorType=='Gyroscope':
			df=df.rename(columns={'x-axis (deg/s)': str(self.sensorName+"_Gx")})
			df=df.rename(columns={'y-axis (deg/s)': str(self.sensorName + "_Gy")})
			df=df.rename(columns={'z-axis (deg/s)': str(self.sensorName + "_Gz")})
		elif self.sensorType=='Accelerometer':
			df=df.rename(columns={'x-axis (g)': str(self.sensorName + "_Ax")})
			df=df.rename(columns={'y-axis (g)': str(self.sensorName + "_Ay")})
			df=df.rename(columns={'z-axis (g)': str(self.sensorName + "_Az")})

		return df