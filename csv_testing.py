import csv
import pandas as pd


def read_file2():
    data = pd.read_csv('empty.csv')

    if data.empty:
        print("empty")

    # headers = list(data.columns.values)
    # print(type(headers[0]))



def main():
    read_file2()

if __name__ == '__main__':
    main()