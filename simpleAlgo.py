import requests
import json
import time

#API Key available at https://site.financialmodelingprep.com/developer
apiKey = "YOUR_API_KEY"

#Refer here for documentation https://site.financialmodelingprep.com/developer/docs
#Stock Ticker E.G: TSLA
#Crypto Ticker E.G: BTCUSD

def getData(ticker):
    response = requests.get("https://financialmodelingprep.com/api/v3/quote/" + ticker.upper() + "?apikey=" + apiKey)
    data = response.json()
    return data[0]

#getData("TSLA")

def getTechnical(ticker, technical, interval):
    validTechnicals = ("sma", "ema", "wma", "dema", "tema", "williams", "rsi", "adx", "standardDeviation")
    validIntervals = ("1min", "5min", "15min", "30min", "1hour", "4hour")
    if (technical.lower() in validTechnicals) and interval.lower() in validIntervals:
        response = requests.get("https://financialmodelingprep.com/api/v3/technical_indicator/" + interval + "/" + ticker.upper() + "?period=10&type=" + technical + "&apikey=" + apiKey)
        data = response.json()
        return data[0][technical]
    elif technical.lower() not in validTechnicals:
        raise ValueError('Invalid Technical Input')
    elif interval.lower() not in validIntervals:
        raise ValueError('Invalid Interval Input')

#getTechnical("BTCUSD","rsi","1min")

def startalgo(ticker, startCapital, buyLots, runtime):
    buyamount = buyLots
    cashCapital = startCapital
    buyprices = list()
    shares = 0
    currentpriceavg = 0
    t = 1
    initial = getData(ticker)
    initialprice = initial["price"]
    prevPrice = initialprice

    print("### ### ### ### ### ### ### ###")
    print("# Algorithm Initialised, Beginning Loop #")
    print("### ### ### ### ### ### ### ###")
    print("# Chosen Ticker: " + ticker)
    print("# Initial Ticker Price: $" + str(initialprice))
    
    while t < runtime:
        price = getData(ticker)["price"]
        rsi = round(getTechnical(ticker,"rsi","1min"),1)
        action = ""
        print("###########################")
        if len(buyprices) > 0:
            currentpriceavg = sum(buyprices) / len(buyprices)

        if (rsi < 35) and (cashCapital > (buyamount * price)):
            prevPrice = price
            shares += buyamount
            cashCapital -= (buyamount * price)
            buyprices.append(price)
            action = "BUY"
        elif (rsi > 65) and (price > currentpriceavg) and (shares > 0):
            prevPrice = price
            cashCapital += shares * price
            shares = 0
            buyprices = list()
            action = "SELL"
        else:
            action = "HOLD"

        if len(buyprices) > 0:
            currentpriceavg = sum(buyprices) / len(buyprices)
        priceChange = round(prevPrice - price, 2)
        priceChangeStr = ""
        if priceChange > 0:
            priceChangeStr = " | UP $" + str(priceChange)
        elif priceChange < 0:
            priceChangeStr = " | DOWN $" + str(priceChange)
        else:
            priceChangeStr = " | SAME $" + str(priceChange)

        print( ("## " + ticker + " " + action) )
        print("## RSI - " + str(rsi))
        print( ("# Ticker Price: ".ljust(20) + ("$" + str( round(price,3) )) ).ljust(34) + priceChangeStr )
        print( ("# Total Equity: ".ljust(20) + ("$" + str((shares * price) + cashCapital )) ).ljust(35) + ("| Cash Capital: ".ljust(20) + ("$" + str(cashCapital)) ) )
        print( ("# Positions Value: ".ljust(20) + ("$" + str(shares * price)) ).ljust(35) + ("| Share Avg: ".ljust(20) + ("$" + str(currentpriceavg)) ) )
        print( ("# Percentage Gain: ".ljust(20) + ("%" + str( round( ((((shares * price) + cashCapital ) - startCapital) / cashCapital ) * 100, 4) ))).ljust(35) + ("| Cash/Stock Ratio: ".ljust(20) + str(int(round( ((cashCapital / ((shares * price) + cashCapital )) * 100),0 ))) + "|" + str(int(round( (((shares * price) / ((shares * price) + cashCapital )) * 100),0 ))) ) )
        print("###########################")
        t += 1
        time.sleep(60) # Sleep for 60 seconds

    print("Algo Finished")

#Ticker, Starting Capital, Buy Amounts, Minutes for algo to run for.
startalgo("BTCUSD", 200000, 1, 120)