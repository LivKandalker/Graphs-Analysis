import yfinance as yf

msft = yf.Ticker("MSFT")
print("The market cap is : ")
print(msft.info['marketCap'])
print(" the net income : ")
print(msft.info['netIncomeToCommon'])

A = msft.info['marketCap']
B = msft.info['netIncomeToCommon']
print("the calculation is : ", A/B)

print("forward PE : ")
print(msft.info['forwardPE'])
print("trailing PE : ")
print(msft.info['trailingPE'])

# 'trailingPE'
# 'forwardPE'