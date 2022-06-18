import plotly.graph_objects as go
import yfinance as yf

df = yf.download("BTC-USD", start="2017-10-01", end="2022-06-10")
df['date_id'] = ((df.index.date - df.index.date.min())).astype('timedelta64[D]')
df['date_id'] = df['date_id'].dt.days + 1
print(df['date_id'])
column_names = list(df.columns.values)
print(column_names)

fig = go.Figure(data=[go.Candlestick(x=df['date_id'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()