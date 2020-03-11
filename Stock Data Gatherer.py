import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

while True:
    print("Period can be entered as 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max.")
    p=str(input("Please enter the period: "))
    if p in ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]:
        break
    else:
        print("Incorrect period format, please try again.")

while True:
    print("Interval can be entered as 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo.")
    interv=str(input("Please enter the interval: "))
    if interv in ["1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"]:
        break
    else:
        print("Incorrect interval format, please try again.")

ticker=str(input("Please enter the ticker: "))
ticker_data=yf.download(ticker,period=p,interval=interv)

if interv in ["1m","2m","5m","15m","30m"]:
    ticker_time=ticker_data.axes[0].strftime('%H-%M').tolist()
elif interv in ["60m","90m","1h"]:
    ticker_time=ticker_data.axes[0].strftime('%d-%H').tolist()
elif interv in ["1d","5d"]:
    ticker_time=ticker_data.axes[0].strftime('%d-%b').tolist()
elif interv == "1wk":
    ticker_time=ticker_data.axes[0].strftime('%d-%b').tolist()
elif interv in ["1mo","3mo"]:
    ticker_time=ticker_data.axes[0].strftime('%b-%y').tolist()
else:
    print("Error determining interval size.")

ticker_open=ticker_data['Open'].tolist()
ticker_close=ticker_data['Close'].tolist()
ticker_high=ticker_data['High'].tolist()
ticker_low=ticker_data['Low'].tolist()

xi = list(range(len(ticker_time)))
reds=[[],[],[],[],[]] #[times,ymin,ymax,highs,lows]
greens=[[],[],[],[],[]]
blacks=[[],[],[],[],[]]
yminOC=[]
ymaxOC=[]
for i in range(0,len(ticker_open)):
    yminOC.append(min(ticker_close[i],ticker_open[i]))
    ymaxOC.append(max(ticker_close[i],ticker_open[i]))
    if ticker_open[i] < ticker_close[i]:#if open < close then green, else red
        greens[0].append(ticker_time[i])
        greens[1].append(yminOC[i])
        greens[2].append(ymaxOC[i])
        greens[3].append(ticker_high[i])
        greens[4].append(ticker_low[i])
    elif ticker_open[i] > ticker_close[i]:
        reds[0].append(ticker_time[i])
        reds[1].append(yminOC[i])
        reds[2].append(ymaxOC[i])
        reds[3].append(ticker_high[i])
        reds[4].append(ticker_low[i])
    else:
        blacks[0].append(ticker_time[i])
        blacks[1].append(yminOC[i])
        blacks[2].append(ymaxOC[i])
        blacks[3].append(ticker_high[i])
        blacks[4].append(ticker_low[i])

plt.vlines(greens[0],ymin=greens[1],ymax=greens[2],linewidth=5,color="green")#greens candle
plt.vlines(greens[0],ymin=greens[4],ymax=greens[3],color="green")#greens wick
plt.vlines(reds[0],ymin=reds[1],ymax=reds[2],linewidth=5,color="red")#reds candle
plt.vlines(reds[0],ymin=reds[4],ymax=reds[3],color="red")#reds wick
plt.vlines(blacks[0],ymin=blacks[1],ymax=blacks[2],linewidth=5,color="black")#blacks candle
plt.vlines(blacks[0],ymin=blacks[4],ymax=blacks[3],color="black")#reds wick
plt.xticks(xi, ticker_time)
plt.xlabel("Time")
plt.ylabel("Asset Value in Dollars")
plt.title(f"{ticker} Over {p} in {interv} Intervals")
plt.show()
