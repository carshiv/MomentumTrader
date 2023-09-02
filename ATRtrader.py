

# Commented out IPython magic to ensure Python compatibility.
#installing the dependencies and the required libraries
!pip install yfinance
!pip install pyfolio
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar
# Silence warnings
import warnings
warnings.filterwarnings('ignore')
import pyfolio as pf
# %matplotlib inline

#function to find the name of the Day of the Week (DOW) on a particular Date
def findDay(date):
    DOW = datetime.datetime.strptime(date,'%Y-%m-%d').weekday()
    return (calendar.day_name[DOW])
#sample input
#date = '2019-02-03'
#findDay(date)
#should give Sunday as output

#all F&O listed stocks on NSE, downloaded their ticker symbols from the NSE website
fno_list = [
'AARTIIND  ',
'ABB       ',
'ABBOTINDIA',
'ABCAPITAL ',
'ABFRL     ',
'ACC       ',
'ADANIENT  ',
'ADANIPORTS',
'ALKEM     ',
'AMBUJACEM ',
'APOLLOHOSP',
'APOLLOTYRE',
'ASHOKLEY  ',
'ASIANPAINT',
'ASTRAL    ',
'ATUL      ',
'AUBANK    ',
'AUROPHARMA',
'AXISBANK  ',
'BAJAJ-AUTO',
'BAJAJFINSV',
'BAJFINANCE',
'BALKRISIND',
'BALRAMCHIN',
'BANDHANBNK',
'BANKBARODA',
'BATAINDIA ',
'BEL       ',
'BERGEPAINT',
'BHARATFORG',
'BHARTIARTL',
'BHEL      ',
'BIOCON    ',
'BOSCHLTD  ',
'BPCL      ',
'BRITANNIA ',
'BSOFT     ',
'CANBK     ',
'CANFINHOME',
'CHAMBLFERT',
'CHOLAFIN  ',
'CIPLA     ',
'COALINDIA ',
'COFORGE   ',
'COLPAL    ',
'CONCOR    ',
'COROMANDEL',
'CROMPTON  ',
'CUB       ',
'CUMMINSIND',
'DABUR     ',
'DALBHARAT ',
'DEEPAKNTR ',
'DELTACORP ',
'DIVISLAB  ',
'DIXON     ',
'DLF       ',
'DRREDDY   ',
'EICHERMOT ',
'ESCORTS   ',
'EXIDEIND  ',
'FEDERALBNK',
'GAIL      ',
'GLENMARK  ',
'GMRINFRA  ',
'GNFC      ',
'GODREJCP  ',
'GODREJPROP',
'GRANULES  ',
'GRASIM    ',
'GUJGASLTD ',
'HAL       ',
'HAVELLS   ',
'HCLTECH   ',
'HDFC      ',
'HDFCBANK  ',
'HDFCLIFE  ',
'HEROMOTOCO',
'HINDALCO  ',
'HINDCOPPER',
'HINDPETRO ',
'HINDUNILVR',
'IBULHSGFIN',
'ICICIBANK ',
'ICICIGI   ',
'ICICIPRULI',
'IDEA      ',
'IDFC      ',
'IDFCFIRSTB',
'IEX       ',
'IGL       ',
'INDHOTEL  ',
'INDIACEM  ',
'INDIGO    ',
'INDUSINDBK',
'INDUSTOWER',
'INFY      ',
'INTELLECT ',
'IOC       ',
'IPCALAB   ',
'ITC       ',
'JINDALSTEL',
'JKCEMENT  ',
'JSWSTEEL  ',
'JUBLFOOD  ',
'KOTAKBANK ',
'L&TFH     ',
'LALPATHLAB',
'LAURUSLABS',
'LICHSGFIN ',
'LT        ',
'LTIM      ',
'LTTS      ',
'LUPIN     ',
'M&M       ',
'M&MFIN    ',
'MANAPPURAM',
'MARICO    ',
'MARUTI    ',
'MCDOWELL-N',
'MCX       ',
'METROPOLIS',
'MFSL      ',
'MGL       ',
'MOTHERSON ',
'MPHASIS   ',
'MRF       ',
'MUTHOOTFIN',
'NATIONALUM',
'NAUKRI    ',
'NAVINFLUOR',
'NESTLEIND ',
'NMDC      ',
'NTPC      ',
'OBEROIRLTY',
'OFSS      ',
'ONGC      ',
'PAGEIND   ',
'PEL       ',
'PERSISTENT',
'PETRONET  ',
'PFC       ',
'PIDILITIND',
'PIIND     ',
'PNB       ',
'POLYCAB   ',
'POWERGRID ',
'RAMCOCEM  ',
'RBLBANK   ',
'RECLTD    ',
'RELIANCE  ',
'SAIL      ',
'SBILIFE   ',
'SHREECEM  ',
'SHRIRAMFIN',
'SIEMENS   ',
'SRF       ',
'SUNPHARMA ',
'SUNTV     ',
'SYNGENE   ',
'TATACHEM  ',
'TATACOMM  ',
'TATACONSUM',
'TATAMOTORS',
'TATAPOWER ',
'TATASTEEL ',
'TCS       ',
'TITAN     ',
'TORNTPHARM',
'TRENT     ',
'TVSMOTOR  ',
'UBL       ',
'ULTRACEMCO',
'UPL       ',
'VEDL      ',
'VOLTAS    ',
'WIPRO     ',
'ZEEL      ',
'ZYDUSLIFE ']
fno_list = [x.strip(' ') for x in fno_list] #stripping unnecessary spaces
tickers = []
for count in range(len(fno_list)):
  tickers.append(fno_list[count] + ".NS") #appending .NS to tickers to make them ready for yFinance

#creating a list of dataframes, where a single dataframe stores OHLC data of one stock
#dataframe at index i in the list corresponds to the OHLC data of fno_list[i] stock
ohlc_data = []
for stock_num in range(len(fno_list)):
  ohlc_data.append(pd.DataFrame(yf.download(tickers[stock_num],start='2019-06-01',end='2023-07-01')))

#iterating through the list of DataFrames, making some relevant changes to each
for i in range(len(ohlc_data)):
  #removing Date as the index column, and stripping it of timezone and time
  #makes the data easier to work with, and stops some troubles, also makes DOW easy
  #also  makes easier to retrieve the date at a particular index, when date is not the index
  ohlc_data[i] = ohlc_data[i].rename_axis('Date').reset_index()
  ohlc_data[i]['Date'] = ohlc_data[i]['Date'].dt.tz_localize(None)
  ohlc_data[i]['Date'] = pd.to_datetime(ohlc_data[i]['Date']).dt.date
  #assigning Day of the Week (DOW) to each date
  #would help in detecting weeks passed accurately, and during rebalancing
  ohlc_data[i]['DOW'] = [findDay(str(ohlc_data[i]['Date'][j])) for j in range(len(ohlc_data[i]['Date']))]
  #pct_change gives percent change, like 1 means 100% change
  ohlc_data[i]['52W Rolling Returns'] = ohlc_data[i]['Close'].pct_change().rolling(250).sum()
  #to reset Date as index, use code snippet given below, if needed
  #ohlc_data[i] = ohlc_data.set_index('Date')

#to access value at a particular index in a column
# use ohlc_data[i]["column"].iloc[index]
#below is the function to get top 5 at start of each week
#based on 52 week (250 days) rolling returns
def getTop5(index):
  returns = []
  for i in range(len(ohlc_data)):
    #stores all 52W rolling returns in a list, along with index no. of each stock
    #index no. stored to make retrieving things easier, index no. works as ID everywhere in the code
    returns.append([i,float(ohlc_data[i]["52W Rolling Returns"].iloc[index])])
  #list is sorted in ascending order and last 5 values returned
  returns = sorted(returns,key=lambda l:l[1])
  return returns[-1:-6:-1]

#function to calculate the average true range
def calculate_atr(data, window=14):
    high = data['High']
    low = data['Low']
    close = data['Close']
    tr1 = high - low
    tr2 = np.abs(high - close.shift())
    tr3 = np.abs(low - close.shift())
    #true range calculated by taking max of tr1, tr2, tr3
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    #atr calculated by taking rolling average of tr with default window=14
    atr = tr.rolling(window).mean()
    return atr

#trading simulation (backtesting)

#initial capital is taken to be 1,000,000
#rebalancing the portfolio at the start of each week (Monday)
capital = 1000000
#storing the value of our portfolio once every day, {cash + (value of stocks held)}
daily_portfolio_value = []
#ohlc_data[0]['DOW'].iloc[252] is Monday, so start from here
#data before that was just used for calculating the 52W rolling returns
for i in range(252,len(ohlc_data[0]['Date'])-1):
  #taking long positions when the week starts (i.e Monday)
  if (ohlc_data[0]['DOW'].iloc[i] == 'Monday'):
    daily_portfolio_value.append(capital)
    toBuy = [] #the 5 stocks to buy
    toBuy = getTop5(i)
    cost = 0
    for j in range(len(toBuy)):
      #1,000,000 divided into 5 equal parts, and then each part used to buy as much possible quantity of each stock
      cost = cost + ohlc_data[toBuy[j][0]]['Close'].iloc[i]*(200000//ohlc_data[toBuy[j][0]]['Close'].iloc[i])
      toBuy[j].append(ohlc_data[toBuy[j][0]]['Close'].iloc[i])
      toBuy[j].append(2*calculate_atr(ohlc_data[toBuy[j][0]]).iloc[i])
      toBuy[j].append(200000//ohlc_data[toBuy[j][0]]['Close'].iloc[i])
      #now toBuy contains the details of our holdings throughout the week, in the format given below
      #toBuy contains [index no., 52W rolling average, price at time of buying, stop loss, quantity to buy]
    capital = capital - cost
  #squaring off the positions at the end of week
  elif (ohlc_data[0]['DOW'].iloc[i+1] == 'Monday'):
    earnings = 0
    for j in range(len(toBuy)):
      earnings = earnings + ohlc_data[toBuy[j][0]]['Close'].iloc[i]*(toBuy[j][4])
    capital = capital + earnings
    toBuy = [] #emptying toBuy, as we've sold all our holdings
    daily_portfolio_value.append(capital)
  #checking those cases throughout the week when price hits stoploss
  #selling the stock as soon as the stoploss is hit
  #and removing that stock from toBuy list so that we don't erroneously sell that stock again at the end of the week
  else:
    to_be_del = []
    for k in range(len(toBuy)):
      curr_price = float(ohlc_data[toBuy[k][0]]['Close'].iloc[i])
      if (curr_price<=(toBuy[k][2]-toBuy[k][3])):
        capital = capital + ohlc_data[toBuy[k][0]]['Close'].iloc[i]*(toBuy[k][4])
        to_be_del.append(k)
    for m in range(len(to_be_del)):
      del toBuy[to_be_del[-1-m]]
    inv = 0 #the value of our stock holdings currently, inv-->inventory
    for j in range(len(toBuy)):
      inv = inv + ohlc_data[toBuy[j][0]]['Close'].iloc[i]*(toBuy[j][4])
    daily_portfolio_value.append(capital+inv)
#taking that edge case into account, when the last day of backtesting period occurs
#selling all our positions
#it was dealt with separately so that indexing issues don't occur inside the above loops
for j in range(len(toBuy)):
  earnings = earnings + ohlc_data[toBuy[j][0]]['Close'].iloc[len(ohlc_data[0]['Date'])-1]*(toBuy[j][4])
capital = capital + earnings
daily_portfolio_value.append(capital)
#daily_portfolio_value list now represents our portfolio value for each trading day, in a sequential format

#total profit when 1,000,000 was invested as the initial capital
total_profit = daily_portfolio_value[-1] - 1000000
print("Total Profit is: " + str(total_profit))

#profit percentage
profit_percentage = ((daily_portfolio_value[-1] - 1000000)/1000000)*100
print("Profit Percentage is: " + str(int(profit_percentage)) + "%")

#plotting the PnL graph

#making 2D PnL list which also includes the number of days passed
pnl = []
for i in range(len(daily_portfolio_value)):
  pnl.append([i,daily_portfolio_value[i]-1000000]) #subtracted 1,000,000 as we want the PnL
#making the PnL DataFrame using the 2D PnL list
pnldf = pd.DataFrame(pnl, columns =['Days Passed','PnL'])
#plotting th PnL graph
plt.plot(pnldf['Days Passed'],pnldf['PnL'])
plt.title('PnL Graph')
plt.xlabel('Days Passed')
plt.ylabel('Profit')

#using pyfolio to analyse the trading strategy

#first we need to add the timestamp (Date-Time) column back to the strategy_returns for it to work with pyfolio
#doing this by taking a random stock on the same stock exchange, Reliance on NSE, and taking timestamps (Date-Time) from it
#using ex2 (RELIANCE.NS data for the same time period as above) for taking corresponsing timestamps
ex2 = pd.DataFrame(yf.download('RELIANCE.NS',start='2019-06-01',end='2023-07-01'))
ex2 = ex2.rename_axis('Date').reset_index() #removing date as an index, making it a regular column
strat_ret_datetime = [] #will store timestamps for the time being, later merged with strategy_returns
for i in range(252,len(ex2['Date'])-1):
  strat_ret_datetime.append(ex2['Date'].iloc[i])
strat_ret_datetime.append(ex2['Date'].iloc[len(ex2['Date'])-1])
#we now have a pd.DataFrame column having daily timestamps for our trading simulation period
#now calculating the percent chnge for each week, and appending timestams with it
strat_returns = pd.DataFrame(daily_portfolio_value)
strategy_returns = strat_returns.pct_change()
#merging the timestamps data (Date-Time) with strategy_returns
strategy_returns['Date'] = strat_ret_datetime
strategy_returns['Date'] = pd.to_datetime(strategy_returns['Date'])
#setting Date-Time as index, for pyfolio to work properly
strategy_returns.set_index('Date', inplace=True)
#generting the tear sheet using pyfolio
pf.create_returns_tear_sheet(strategy_returns[0])