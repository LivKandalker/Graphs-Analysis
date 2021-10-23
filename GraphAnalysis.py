from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from scipy.stats import linregress
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#app = Flask('template-index.html')
app = Flask(__name__, template_folder='../templates')
# Decorator defines a route
# http://localhost:5000/

@app.route('/')
def index():
    """
    The link between python and HTML with flask
    :return: index.html
    """
    return render_template("index.html")

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
  """
  Calculate the Trends-Lines - connect all of the local minimum value together, and connect
  all of the local maximum value together
  :param company_symbol:Known company or coin symbol at the stocks market
  :param periodDateStart:Day,Month and Year for Start
  :param periodDateEnd:Day,Month and Year for End
  :return: Two plot in one figure: 1)Adj close with Trends Line. 2) Volume plot
  """
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
    return "Back to our site"


@app.route('/my-link-ROC/')
def my_link_ROCtool(company_symbol, ROCperiodDateStart, ROCperiodDateEnd, ROCtermTrading):
    def get_stock(company_symbol, Date_start, Date_End):
        data = yf.download(company_symbol, start=Date_start, end=Date_End)

        data0 = data.copy()
        data0['date_id'] = ((data0.index.date - data0.index.date.min())).astype('timedelta64[D]')
        data0['date_id'] = data0['date_id'].dt.days + 1
        df = data0.copy()

        return df['Adj Close']

    def ROC(df, n):
        M = df.diff(n - 1)
        N = df.shift(n - 1)
        ROC = pd.Series(((M / N) * 100))
        return ROC

    #fig, ax = plt.subplots(2)
    df = pd.DataFrame(get_stock(company_symbol, ROCperiodDateStart, ROCperiodDateEnd))
    df['ROC'] = ROC(df['Adj Close'], int(ROCtermTrading))
    df.tail()
    #ax[1].plot(df['ROC'])
    #ax[0].plot(df['Adj Close'])
    #print(df['ROC'])

    plt.figure(figsize=(12.33, 4.5))
    plt.title('ROC Plot')
    plt.plot(df.index, df['ROC'])

    plot_url = plt.show()
    return render_template('index.html', plot_url=plot_url)

@app.route('/handle_data3', methods=['POST'])
def handle_data3():
    projectFilePath = request.form['projectFilepath']
    ROCperiodDateStart = request.form['ROCperiodDateStart']
    ROCperiodDateEnd = request.form['ROCperiodDateEnd']
    ROCtermTrading = request.form['termTrading']
    my_link_ROCtool(projectFilePath, ROCperiodDateStart, ROCperiodDateEnd, ROCtermTrading)
    #return projectpath
    return "Back to our site"
if __name__ == '__main__':
  app.run(debug=True)

#if __name__ == '__main__':
 #   app.run()