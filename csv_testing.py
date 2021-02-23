import csv
import pandas as pd


def read_file2():
    data = pd.read_csv('base.csv')

    headers = list(data.columns.values)
    data['Activity'] = "curl"
    data.to_csv('output.csv', index=False)

def read_file():
	
    headers = []

    ranges = {}

    ranges = ["0-5", "6-10", "11-15"]

    csvfile = open("base.csv",'r')
    output = open("testout.csv", 'w')

    data = csv.reader(csvfile, delimiter=',')
    writer = csv.writer(output, lineterminator='\n')

    for hdr in next(data):
        print(hdr.strip())
        headers.append(hdr.strip())

    a = []

    # for row in data:
    #     print(row[0])

    #     # for i in range(len(headers)):
    #     #     print(str(i) + row[i])
    #     print("end row")
    #     row.append("butt")
    #     a.append(row)
    
    # writer.writerows(a)
        

def in_range(key, x):
    """key like '1601655830786-1601655830795' """
    splitted = key.split("-")
    start = int(splitted[0])
    end = int(splitted[1])

    if x >= start and x <= end:
        print("in range: " + key)
    else:
        print("not in range")

def main():
    read_file2()

if __name__ == '__main__':
    main()