from flask import Flask, render_template, request, redirect, url_for
import yfinance
import quandl
import numpy
import seaborn
import matplotlib
import matplotlib_venn
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from tkinter import *
import yfinance as yf
import pandas as pd
from scipy.stats import linregress
import quandl, math
from sklearn import preprocessing, svm
#, cross_validation, svm
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import style
import datetime




#app = Flask('template-index.html')
app = Flask(__name__, template_folder='../templates')
# Decorator defines a route
# http://localhost:5000/
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/my-link-Fibonachi/')
def my_link_Fibonachi(company_symbol, Date_start, Date_End):
  print ('I got clicked!')
  data = yf.download(company_symbol, start=Date_start, end=Date_End)

  data0 = data.copy()
  data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
  data0['date_id'] = data0['date_id'].dt.days + 1

  df = data0.copy()
  maximum_price = df['Adj Close'].max()
  minimum_price = df['Adj Close'].min()
  difference = maximum_price - minimum_price  # Get the difference
  first_level = maximum_price - difference * 0.236
  second_level = maximum_price - difference * 0.382
  third_level = maximum_price - difference * 0.5
  fourth_level = maximum_price - difference * 0.618

  new_df = data0.copy()
  plt.figure(figsize=(12.33, 4.5))
  plt.title('Fibonnacci Plot')
  plt.plot(new_df.index, new_df['Adj Close'])
  plt.axhline(maximum_price, linestyle='--', alpha=0.3, color='red')
  plt.axhline(first_level, linestyle='--', alpha=0.3, color='orange')
  plt.axhline(second_level, linestyle='--', alpha=0.3, color='yellow')
  plt.axhline(third_level, linestyle='--', alpha=0.3, color='green')
  plt.axhline(fourth_level, linestyle='--', alpha=0.3, color='blue')
  plt.axhline(minimum_price, linestyle='--', alpha=0.3, color='purple')
  plt.xlabel('Date', fontsize=18)
  plt.ylabel('Close Price in USD', fontsize=18)

  plot_url = plt.show()
  return render_template('index.html', plot_url=plot_url)

@app.route('/my-link-Trends/')
def my_link_Trends(company_symbol, periodDateStart, periodDateEnd ):
  print ('I got clicked!')
  data = yf.download(company_symbol, start=periodDateStart, end=periodDateEnd)

  data0 = data.copy()
  data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
  data0['date_id'] = data0['date_id'].dt.days + 1

  # high trend line
  print(data)
  data1 = data0.copy()

  while len(data1) > 3:
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

  while len(data1) > 3:
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

  # plot

  ax[0].plot(data0['Adj Close'])
  ax[0].plot(data0['high_trend'])
  ax[0].plot(data0['low_trend'])
  ax[1].plot(data0['Volume'])


  plot_url = plt.show()
  return render_template('index.html', plot_url=plot_url)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    periodDateStart = request.form['periodDateStarted']
    periodDateEnd = request.form['periodDateEnd']
    my_link_Trends(projectpath, periodDateStart, periodDateEnd)
    return "back to our website"

@app.route('/handle_data2', methods=['POST'])
def handle_data2():
    projectpath = request.form['projectFilepath']
    periodDateStart = request.form['periodDateStarted']
    periodDateEnd = request.form['periodDateEnd']
    my_link_Fibonachi(projectpath, periodDateStart, periodDateEnd)
    #return projectpath
    return "back to our website"

if __name__ == '__main__':
  app.run(debug=True)

#if __name__ == '__main__':
 #   app.run()