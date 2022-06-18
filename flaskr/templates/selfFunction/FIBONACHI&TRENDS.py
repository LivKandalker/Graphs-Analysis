#Import data from Yahoo Finance and all the library that we need

import numpy
import quandl
import yfinance
import seaborn
"""import requirementstxt"""
import matplotlib_venn


import pandas as pd
import yfinance as yf
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from tkinter import *

# Start

import quandl, math
from sklearn import preprocessing, svm
#, cross_validation, svm
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import style
import datetime

# get Bitcoin or any stocks that you want for every time period data
#change stocks or Digital coins here
# #change period time here

data = yf.download("ETH-USD", start="2017-10-01", end="2021-10-21")
print(data)
data0 = data.copy()
data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
print(data0['date_id'])
data0['date_id'] = data0['date_id'].dt.days + 1


data2 = data0.copy()
period_trading = 25 #200, 12, 25
End_ClosePrice = data2['Adj Close'].iloc[period_trading]
Start_ClosePrice = data2['Adj Close'].iloc[0]
ROC = (((End_ClosePrice - Start_ClosePrice)/Start_ClosePrice) * 100)
print(ROC)



# high trend line
print(data)
data1 = data0.copy()

while len(data1)>3:

    reg = linregress(
                    x=data1['date_id'],
                    y=data1['High'],
                    )
    data1 = data1.loc[data1['High'] > reg[0] * data1['date_id'] + reg[1]]

reg = linregress(
                    x=data1['date_id'],
                    y=data1['High'],
                    )

data0['high_trend'] = reg[0] * data0['date_id'] + reg[1]

# low trend line

data1 = data0.copy()

while len(data1)>3:

    reg = linregress(
                    x=data1['date_id'],
                    y=data1['Low'],
                    )
    data1 = data1.loc[data1['Low'] < reg[0] * data1['date_id'] + reg[1]]

reg = linregress(
                    x=data1['date_id'],
                    y=data1['Low'],
                    )

data0['low_trend'] = reg[0] * data0['date_id'] + reg[1]

fig, ax = plt.subplots(2)




#plot
ax[0].plot(data0['Adj Close'])
ax[0].plot(data0['high_trend'])
ax[0].plot(data0['low_trend'])

ax[1].plot(data0['Volume'])


#Calculate the max and min close price
df = data0.copy()
maximum_price = df['Adj Close'].max()
minimum_price = df['Adj Close'].min()
difference = maximum_price - minimum_price #Get the difference
first_level = maximum_price - difference * 0.236
second_level = maximum_price - difference * 0.382
third_level = maximum_price - difference * 0.5
fourth_level = maximum_price - difference * 0.618

new_df = data0.copy()
plt.figure(figsize=(12.33,4.5))
plt.title('Fibonnacci Plot')
plt.plot(new_df.index, new_df['Adj Close'])
plt.axhline(maximum_price, linestyle='--', alpha=0.3, color = 'red')
plt.axhline(first_level, linestyle='--', alpha=0.3, color = 'orange')
plt.axhline(second_level, linestyle='--', alpha=0.3, color = 'yellow')
plt.axhline(third_level, linestyle='--', alpha=0.3, color = 'green')
plt.axhline(fourth_level, linestyle='--', alpha=0.3, color = 'blue')
plt.axhline(minimum_price, linestyle='--', alpha=0.3, color = 'purple')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price in USD',fontsize=18)

plt.show()
