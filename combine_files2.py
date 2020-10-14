import pandas as pd
import os
import sys
import argparse


class combine_files():

	def __init__(self, source, destination):
		self.src_folder = source
		self.dest_folder = destination
		
	def make_paths_absolute(self):
	    if os.path.isabs(source_folder) != True:
	        self.src_folder = os.path.abspath(self.src_folder)

	    if os.path.isabs(dest_folder) != True:
	        self.dest_folder = os.path.abspath(self.dest_folder)

	def validate_folders(self):
		if os.path.isdir(self.src_folder)==False:
	        print('Source folder '+self.src_folder+' cannot be found!\nExiting...')
	        sys.exit(0)
	    if os.path.isdir(self.dest_folder)==False:
	        print('Destination folder' +self.dest_folder+' cannot be found!\nExiting...')
	        sys.exit(0)


	def run(self):
		make_paths_absolute()
		validate_folders()
		