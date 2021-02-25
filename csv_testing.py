import csv
import pandas as pd


def read_file2():
    data = pd.read_csv('base.csv')

    headers = list(data.columns.values)
    print(type(headers[0]))

    test = in_range(data[headers[0]])

    for t in test:
        print(type(t))


    data['Activity'] = ""
    data.to_csv('output.csv', index=False)

def in_range(vals):
    acts = []

    for x in vals:
        print(float(x))
        acts.append(float(x))

    return acts

def main():
    read_file2()

if __name__ == '__main__':
    main()