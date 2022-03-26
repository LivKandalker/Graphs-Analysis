import logging
import os
from distutils.util import execute

import pandas
from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from pygments.lexers import web

plt.style.use('fivethirtyeight')
from scipy.stats import linregress
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

#app = Flask('templates-index.html')
app = Flask(__name__, template_folder='../../flask_project/flaskr/templates')
GRAPH_FOLDER = os.path.join('flaskr')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = GRAPH_FOLDER
# Decorator defines a route
# http://localhost:5000/


@app.route('/')
def index():
    """
    The link between python and HTML with flask
    :return: index.html
    """
    return render_template("index.html")

@app.route('/Send_To_Fibonacci', methods=['POST'])
def Send_To_Fibonacci():
    """
    handle data 2 save the details from the form in new varaibles and send to my Fibonacci function
    :return: message: "back to our website"
    """
    projectpath = request.form['projectFilepath']
    periodDateStart = request.form['periodDateStarted']
    periodDateEnd = request.form['periodDateEnd']
    fibonacci_graph = my_link_Fibonachi(projectpath, periodDateStart, periodDateEnd)

    #will print a message to the console
    logging.debug(fibonacci_graph)
    return fibonacci_graph


@app.route('/')
@app.route('/index')
@app.route('/my-link-Fibonachi/')
def my_link_Fibonachi(company_symbol, Date_start, Date_End):
  """
  Calculate all of the Fibonacci level with the max&min to the chosen period, and show fibonacci
   plot with tha Adj Close plot.
  :param company_symbol: Known company or coin symbol at the stocks market
  :param Date_start: Day,Month and Year for Start
  :param Date_End: Day,Month and Year for the End
  :return: Fibonacci plot for the period that chosen
  """
  #Save the plot in Varaible and return the plot to the HTML web

  # will print a message to the console
  logging.debug('I got clicked!')

  # Import specipic data from the Yahoo Finance website
  data = yf.download(company_symbol, start=Date_start, end=Date_End)
  data['date_id'] = ((data.index.date - data.index.date.min())).astype('timedelta64[D]')
  data['date_id'] = data['date_id'].dt.days + 1

  # Finding the maximum price and finding the minimum price
  maximum_price = data['Adj Close'].max()
  minimum_price = data['Adj Close'].min()

  # Get the difference and calculate the Fibonacci level
  difference = maximum_price - minimum_price
  first_level = maximum_price - difference * 0.236
  second_level = maximum_price - difference * 0.382
  third_level = maximum_price - difference * 0.5
  fourth_level = maximum_price - difference * 0.618

  # Define the graph size
  plt.figure(figsize=(12.33, 4.5))

  # Define the graph name-graph title and for the Adj close information
  plt.title('Fibonnacci Plot')
  plt.plot(data.index, data['Adj Close'])

  # Create colored straight lines according to calculated Fibonacci levels
  plt.axhline(maximum_price, linestyle='--', alpha=0.3, color='red')
  plt.axhline(first_level, linestyle='--', alpha=0.3, color='orange')
  plt.axhline(second_level, linestyle='--', alpha=0.3, color='yellow')
  plt.axhline(third_level, linestyle='--', alpha=0.3, color='green')
  plt.axhline(fourth_level, linestyle='--', alpha=0.3, color='blue')
  plt.axhline(minimum_price, linestyle='--', alpha=0.3, color='purple')

  # Define the font size of x & y label (Date & close price)
  plt.xlabel('Date', fontsize=18)
  plt.ylabel('Close Price in USD', fontsize=18)
  plt.plot(data.index, data['Adj Close'], maximum_price,first_level, second_level, third_level, fourth_level, minimum_price)
  plot_url= plt.show()
  return render_template('plots.html', plot_url='plot_url')



@app.route('/my-link-Trends/')
def my_link_Trends(company_symbol, periodDateStart, periodDateEnd ):
  """
  Calculate the Trends-Lines - connect all of the local minimum value together, and connect
  all of the local maximum value together
  :param company_symbol:Known company or coin symbol at the stocks market
  :param periodDateStart:Day,Month and Year for Start
  :param periodDateEnd:Day,Month and Year for End
  :return: Two plot in one figure: 1)Adj close with Trends Line. 2) Volume plot
  """
  #will print a message to the console
  logging.debug('I got clicked!')

  # Import specipic data from the Yahoo Finance website
  data = yf.download(company_symbol, start=periodDateStart, end=periodDateEnd)

  data['date_id'] = ((data.index.date - data.index.date.min())).astype('timedelta64[D]')
  data['date_id'] = data['date_id'].dt.days + 1

  # Create a linear line for high trend line in graph
  #will print the data table to the console
  logging.debug(data)

  Data_Trends = data.copy()
  while len(Data_Trends) > 3:
    reg = linregress(
      x=Data_Trends['date_id'],
      y=Data_Trends['High'],
    )
    Data_Trends = Data_Trends.loc[Data_Trends['High'] > reg[0] * Data_Trends['date_id'] + reg[1]]

  reg = linregress(
    x=Data_Trends['date_id'],
    y=Data_Trends['High'],
  )

  data['high_trend'] = reg[0] * data['date_id'] + reg[1]

  # Create a linear line for low trend line

  Data_Trends = data.copy()

  while len(Data_Trends) > 3:
    reg = linregress(
      x=Data_Trends['date_id'],
      y=Data_Trends['Low'],
    )
    Data_Trends = Data_Trends.loc[Data_Trends['Low'] < reg[0] * Data_Trends['date_id'] + reg[1]]

  reg = linregress(
    x=Data_Trends['date_id'],
    y=Data_Trends['Low'],
  )

  data['low_trend'] = reg[0] * data['date_id'] + reg[1]

  #Create place for 2 Plot in one output
  fig, ax = plt.subplots(2)

  # plot for Trends
  ax[0].plot(data['Adj Close'])
  ax[0].plot(data['high_trend'])
  ax[0].plot(data['low_trend'])

  # Plot for Volume
  ax[1].plot(data['Volume'])

  # Save the plot in Varaible and return the plot to the HTML web
  plot_url = plt.show()
  return render_template('plots.html', plot_url=plot_url)


@app.route('/Send_to_Trend', methods=['POST'])
def Send_to_Trend():
    """
    handle data save the details from the form in new varaibles and send to my trends function
    :return: message: "back to our website"
    """
    projectpath = request.form['projectFilepath']
    periodDateStart = request.form['periodDateStarted']
    periodDateEnd = request.form['periodDateEnd']
    Trends_and_volume = my_link_Trends(projectpath, periodDateStart, periodDateEnd)
    return Trends_and_volume

@app.route('/my-link-ROC/')
def my_link_ROCtool(company_symbol, ROCperiodDateStart, ROCperiodDateEnd, ROCtermTrading):
    """
    Create a graph figure of the ROC tool from the HTML
    :param company_symbol:stocks symbol (TSLA - is the symbol for tesla company for example)
    :param ROCperiodDateStart:Date start user chose
    :param ROCperiodDateEnd:Date End user chose
    :param ROCtermTrading:Time of trading for
    :return:ROC tool from the HTML
    """
    def get_stock(company_symbol, Date_start, Date_End):
        """
        Get stock and period and create a data frame copy
        :param company_symbol: stocks symbol (TSLA - is the symbol for tesla company for example)
        :param Date_start: Date start user chose
        :param Date_End: Date End user chose
        :return: Data frame of Adj close
        """
        # Import specipic data from the Yahoo Finance website
        data = yf.download(company_symbol, start=Date_start, end=Date_End)

        data['date_id'] = ((data.index.date - data.index.date.min())).astype('timedelta64[D]')
        data['date_id'] = data['date_id'].dt.days + 1

        #Return the Adj Close column
        return data['Adj Close']

    def ROC(df, n):
        """
        Calculate the Rate of change
        :param df: Copy of the data frame
        :param n: Time of trading for
        :return: ROC
        """
        M = df.diff(n - 1)
        N = df.shift(n - 1)
        ROC = pd.Series(((M / N) * 100))

        #Return the series of ROC tool
        return ROC

    #Send the specipic data to get stock for the Adj close column
    df = pd.DataFrame(get_stock(company_symbol, ROCperiodDateStart, ROCperiodDateEnd))

    #Send the Adj close plot and the time for term trading to ROC function
    df['ROC'] = ROC(df['Adj Close'], int(ROCtermTrading))
    df.tail()

    #Define the size of the plot and the name title of the plot. Create graph for the index un ROC data frame
    plt.figure(figsize=(12.33, 4.5))
    plt.title('ROC Plot')
    plt.plot(df.index, df['ROC'])

    # Save the plot in Varaible and return the plot to the HTML web
    plot_url = plt.show()
    return render_template('index.html', plot_url=plot_url)

@app.route('/Send_To_ROC', methods=['POST'])
def Send_To_ROC():
    """
    handle data save the details from the form in new varaibles and send to my ROC tool function
    :return: message: "back to our website"
    """
    projectFilePath = request.form['projectFilepath']
    ROCperiodDateStart = request.form['ROCperiodDateStart']
    ROCperiodDateEnd = request.form['ROCperiodDateEnd']
    ROCtermTrading = request.form['termTrading']
    ROC_tool = my_link_ROCtool(projectFilePath, ROCperiodDateStart, ROCperiodDateEnd, ROCtermTrading)
    return ROC_tool

@app.route('/Send_To_SMA', methods=['POST'])
def Send_To_SMA():
    """
    handle data save the details from the form in new varaibles and send to my SMA tool function
    :return: message: "back to our website"
    """
    projectFilePath = request.form['projectFilepath']
    SMAperiodDateStart = request.form['SMAperiodDateStart']
    SMAperiodDateEnd = request.form['SMAperiodDateEnd']
    SMA_tool = my_link_SMAtool(projectFilePath, SMAperiodDateStart, SMAperiodDateEnd)
    return SMA_tool

@app.route('/my-link-SMA/')
def my_link_SMAtool(company_symbol, SMAperiodDateStart, SMAperiodDateEnd):
    """
    Create a graph figure of the SMA tool from the HTML
    (20 & 100 days)
    :param company_symbol:stocks symbol (TSLA - is the symbol for tesla company for example)
    :param SMAperiodDateStart:Date start user chose
    :param SMAperiodDateEnd:Date End user chose
    :return:SMA tool from the HTML
    """
    import matplotlib.pyplot as plt

    # set start and end dates
    start = SMAperiodDateStart
    end = SMAperiodDateEnd

    # extract the closing price data
    data = yf.download(company_symbol, start=start, end=end)

    data['date_id'] = ((data.index.date - data.index.date.min())).astype('timedelta64[D]')
    data['date_id'] = data['date_id'].dt.days + 1

    # create 20 days simple moving average column
    data['20_SMA'] = data['Adj Close'].rolling(window=20, min_periods=1).mean()

    # create 50 days simple moving average column
    data['50_SMA'] = data['Adj Close'].rolling(window=50, min_periods=1).mean()

    plt.figure(figsize=(20, 10))
    # plot close price, short-term and long-term moving averages
    data['Adj Close'].plot(color='k', label='Close Price')
    data['20_SMA'].plot(color='b', label='20 - day SMA')
    data['50_SMA'].plot(color='g', label='50 - day SMA')

    # Save the plot in Varaible and return the plot to the HTML web
    plot_url = plt.show()
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
  app.run(debug=True)

#if __name__ == '__main__':
 #   app.run()