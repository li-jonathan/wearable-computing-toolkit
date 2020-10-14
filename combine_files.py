
'''
This script will be used to combine all csv files from the 'DataDump" git folder into one csv
Original Script: Amanda Redhouse 6.28.18

7.2.18
Modified to use paths to/from folders as function parameters. -JF

11.25.19
Updated program to use more pandas calls and less manual manipulation. Right to Left joins
are performed based upon https://mbientlab.com/tutorials/Apps.html#synchronizing-multiple-datasets-in-python
Program will now check if files all have same sample rate and will merged on shortest file time. -JF

1.12.20
Add argparse to check that source and destination are supplied

TODO:
Remove hard-coded file output name


Demo: within the tools/ folder in the data_tools branch run the following commands:
cp *.csv src/.  #copies the sample csv files into src/
python combine_files --dest dest/ --src src/ #should merge files and make a new “merged.csv” in dest/


'''
import pandas as pd
import os
import sys
import argparse

#### Begin MBientDataFile Class ####

class MBientDataFile:

    #file path to source file
    filePath=None

    #sensor/data type
    sensorType=None

    #sampling rate for data
    sampleRate=None

    #user assigned name for sensor
    sensorName=None

    #data/time in UTC format that data was captured
    captureDateTime=None

    #sensor MAC address
    MAC=None

    #first UNIX timestamp for data capture
    startTime=None

    #fixed label for time column names
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



#### End MBientDataFile Class ####


def main(source, dest):

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
        print('No files in source directory. Exiting.')
        return

    #Check #1: See if files are all the same sample right
    initRate = mbient_files[0].sampleRate
    for i in range(1,len(mbient_files)):
        #TODO: come up with a better method than this. 2Hz sampling error may a lot...
        if abs(initRate - mbient_files[i].sampleRate)>2:
            print("Error! All files are not the same sample rate!")
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
        print("Files have different start times. Synchronizing....")
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Combine mbient CSV files from multiple sensors into a single file.')
    parser.add_argument('--src', dest='src', nargs=1, action="store", help='Path to a folder where all input CSV files are located',
                        required=True)
    parser.add_argument('--dest', dest='dest', nargs=1, action="store",
                        help='Path to destination folder where output.csv file will be created', required=True)

    args = parser.parse_args()

    #pull out parameters and arguments
    source_folder = args.src[0]
    dest_folder = args.dest[0]

    print(sour)

    #make path absolute
    if os.path.isabs(source_folder) != True:
        source_folder = os.path.abspath(source_folder)

    #make path absolute
    if os.path.isabs(dest_folder) != True:
        dest_folder = os.path.abspath(dest_folder)

    #determine if source and destination folders are valid folders
    if os.path.isdir(dest_folder)==False:
        print('Destination folder' +dest_folder+' cannot be found!')
        print('Exiting...')
        sys.exit(0)
    if os.path.isdir(source_folder)==False:
        print('Source folder '+source_folder+' cannot be found!')
        print('Exiting...')
        sys.exit(0)

    #call main with folders
    main(source_folder,dest_folder)

    print('Done!')
