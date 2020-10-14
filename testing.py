import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



df = pd.read_csv('test.csv')

sw = df.transpose()

x = df.columns.tolist()
y = sw.values.tolist()

print(x)
print(y)

# for i in y:
# 	plt.plot(x,i)

# plt.gcf().autofmt_xdate()
# plt.show()
