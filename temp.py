import yfinance as yf
import pandas as pd


def get_top5(stock_data):
    weekly_returns = stock_data['Close'].pct_change()
    top_5_stocks = weekly_returns.mean().sort_values(ascending=False).head(5)
    print(type(top_5_stocks))
    print(top_5_stocks)
    return top_5_stocks

#ATR indicator logic
def get_atr(stock_data):
    high = stock_data["High"]
    low = stock_data["Low"]
    close = stock_data["Close"]

    tr = pd.DataFrame(high - low)
    tr.columns = ["TR"]

    tr["H-L"] = abs(high - low.shift(1))
    tr["H-C"] = abs(high - close.shift(1))
    tr["L-C"] = abs(low - close.shift(1))

    tr["TR"] = tr.max(axis=1)
    atr = tr["TR"].rolling(window=14).mean()  # Window size as required

    return atr

tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0].SYMBOL.to_list()
symb = [scrip for scrip in tickers if "NIFTY" not in scrip] #Removing indices from the list
symb = [stock + ".NS" for stock in tickers] #Adding '.NS' in front of each symbol .

start_date = "2020-02-01"
end_date = "2022-02-01"

price_data = yf.download(symb , start = start_date, end = end_date ,interval="1wk") #Downloading FnO stock data

#Initializing dataFrame for recording trades .
trade_df = pd.DataFrame(columns=["Symbol", "Entry_Date", "Entry_Price", "Exit_Date", "Exit_Price", "Profit"])

topFiveGainers = get_top5(price_data).index

for symbol in topFiveGainers: #Looping through each stock
    stock_data = yf.download(symbol, start="2017-02-01", end="2020-02-01", interval="1wk")
    stock_data["ATR_Value"] = get_atr(stock_data)
    stock_data.dropna()

    entry_date = None
    entry_price = None
    exit_date = None
    exit_price = None
    trade_active = False

    for index, row in stock_data.iterrows():
        close_price = row["Close"]

        if not trade_active:
            print(index)
            print(symbol)
            entry_date = index
            entry_price = close_price
            print(close_price)
            trade_active = True
        else:

            stop_loss_price = entry_price - (2*(stock_data["ATR_Value"].values[0]))
            #stop_loss_price = entry_price - (entry_price * (3 / 100))
            if close_price <= stop_loss_price or index == stock_data.index[-1]:
                exit_date = index
                exit_price = close_price
                trade_active = False

                profit = (exit_price - entry_price) / entry_price * 100
                df2 = pd.DataFrame([[symbol, entry_date, entry_price,exit_date,exit_price,profit]],
                                   columns=["Symbol", "Entry_Date", "Entry_Price", "Exit_Date", "Exit_Price", "Profit"])
                trade_df = pd.concat([trade_df,df2]) #Appending trade data


                entry_date = None
                entry_price = None
                exit_date = None
                exit_price = None

print(trade_df) #Final P&L with entry and exit dates