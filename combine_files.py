import pandas as pd
import os
import sys
import argparse

from mbient_data_file import MBientDataFile

"""
CombineFiles
From: https://git.cs.jmu.edu/WearableComputing/ActivityRecognition/blob/data_tools/Python/tools/combine_files.py
"""

class CombineFiles():

	def __init__(self, source, destination):
		"""Constructor."""

		self.src_folder = source
		self.dest_folder = destination
		self.log = []
		
	def make_paths_absolute(self):
		"""Math paths absolute."""

		self.log.append("Making paths absolute...")
		if os.path.isabs(self.src_folder) != True:
			self.src_folder = os.path.abspath(self.src_folder)
		if os.path.isabs(self.dest_folder) != True:
			self.dest_folder = os.path.abspath(self.dest_folder)

	def validate_folders(self):
		"""Determine if source and destination folders are valid folders."""

		self.log.append("Validating folders...")
		if os.path.isdir(self.src_folder)==False:
			self.log.append('Source folder '+self.src_folder+' cannot be found!\nExiting...')
			sys.exit(0)
		if os.path.isdir(self.dest_folder)==False:
			self.log.append('Destination folder' +self.dest_folder+' cannot be found!\nExiting...')
			sys.exit(0)

	def main(self):
		"""Main."""

		source = self.src_folder
		dest = self.dest_folder

		#get all the files out of the src/ folder
		input_file_path = source + '/' #this line may no longer be necessary
		files = os.listdir(input_file_path)

		mbient_files = list()

		for file in files:
			if "Accelerometer" or "Gyroscope" in file:
					dataFile= MBientDataFile(input_file_path+file)
					mbient_files.append(dataFile)

	    #basic sanity checking. See if all have same sample right and
	    #if they start are "roughly" the same time

	    #Check #0 Did we get any files?!
		if len(mbient_files) == 0:
			self.log.append('No files in source directory. Exiting.')
			return

	    #Check #1: See if files are all the same sample right
		initRate = mbient_files[0].sampleRate
		for i in range(1,len(mbient_files)):
			#TODO: come up with a better method than this. 2Hz sampling error may a lot...
			if abs(initRate - mbient_files[i].sampleRate)>2:
				self.log.append("Error! All files are not the same sample rate!")
				return


	    #Check #2: See if they all start at the "same" time
		startTimes = list()
		for file in mbient_files:
			startTimes.append(file.startTime)

		minimum = min(startTimes)
		maximum = max(startTimes)

		delta = abs(minimum - maximum)

		synchronize=False
		if delta>1000:
			self.log.append("Files have different start times. Synchronizing....")
			synchronize=True

	    #generate dataframes from each file. Concat into single file and
	    #if needed to synchronize follow https://mbientlab.com/tutorials/Apps.html#synchronizing-multiple-datasets-in-python
	    #perform left merge based upon the "oldest" file

	    #find the youngest file and make it "left"
		def sortMethod(mbientFile):
			return mbientFile.startTime

		mbient_files=sorted(mbient_files,key=sortMethod,reverse=True)

		left = mbient_files[0].generate_data_frame()

		for i in range(1,len(mbient_files)):
			right = mbient_files[i].generate_data_frame()

	        #merge from right to left on 'epoc' column. Nearest match with 5ms tolerance
			left = pd.merge_asof(left,right,on='epoc (ms)',direction='nearest',tolerance=5)

	    #all files are now merged into the "left" file
		dest_file_path = dest + '/merged.csv'

	    #don't print out index
		left.to_csv(dest_file_path,index=False)

		self.log.append("Successfully merged files in dest/merged.csv")

	def run(self):
		"""Run functions."""

		self.make_paths_absolute()
		self.validate_folders()
		self.main()
		