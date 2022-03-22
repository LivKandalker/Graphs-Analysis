import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


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

fig, ax = plt.subplots(2)
df = pd.DataFrame(get_stock('FB', '2019-10-01', '2021-10-01'))
df['ROC'] = ROC(df['Adj Close'], 200)
df.tail()
ax[1].plot(df['ROC'])
ax[0].plot(df['Adj Close'])
print(df['ROC'])
plt.show()