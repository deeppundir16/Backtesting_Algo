# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:25:33 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:45:57 2020

@author: User
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv ('C:/Users/User/Desktop/NIFTY1.csv')
df 
df['Close']

## Initialize the short and long windows

short_window = 50
long_window = 100

## Initialize the signals DataFrame with the signal column


df['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

## Create long simple moving average over the long window

df['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

df['Close'].plot(color = 'k', label= 'Close Price') 
df['short_mavg'].plot(color = 'b',label = 'short_mavg') 
df['long_mavg'].plot(color = 'g', label = 'long_mavg')


df['Signal'] = 0.0
df['Signal'] = np.where(df['short_mavg'] > df['long_mavg'], 1.0, 0.0)
df['Position'] = df['Signal'].diff()

## DF function
def backtest_strategy_stoploss(df):
    iBuyFlag = 0
    iSellFlag = 0
    iBuy = 0
    iSell = 0
    last_buy_price=0.00
    last_sell_price=0.00
    init = (iBuyFlag == 0 & iSellFlag == 0)
    for d in range(0,len(df)):
        
        iBuy = np.where(df['Position'].at[d] == 1,1,0)
        iSell = np.where(df['Position'].at[d] == -1,1,0)
        
        print("d:",d,"init:",init,"iBuy:",iBuy,"iSell:",iSell,"iBuyFlag:",iBuyFlag,"iSellFlag:",iSellFlag)   
      
        
        if (init == 1 & iBuy == 1):
                iBuyFlag = 1
                iSellFlag = 0
                last_buy_price= df['Close'].iat[d]
                iBuy = 0
                init = 0
        elif (init == 1 & iSell == 1):
                 iBuyFlag = 0
                 iSellFlag = 1
                 iSell = 0
                 init = 0
                 last_sell_price= df['Close'].iat[d]
                 print("72:",d)
        elif(iBuyFlag == 1 & iSell == 1):
                iBuyFlag = 0
                iSellFlag = 1
                iSell = 0
                last_sell_price= df['Close'].iat[d]
                df.at[d, 'Trade_MTM'] = (last_sell_price - last_buy_price)
                print("Buy Exit:",last_sell_price)
                print("Buy Entry:",last_buy_price)
                print("MTM:", (last_sell_price - last_buy_price))
        
        if(iBuy == 1 & iSellFlag == 1):
                    iBuyFlag = 1
                    iSellFlag = 0
                    iBuy=0
                    last_buy_price= df['Close'].iat[d]
                    df.at[d,'Trade_MTM'] = (last_sell_price - last_buy_price)  
                    print("d:",d,"Sell Exit:",last_buy_price,"Sell Entry:",last_sell_price,"MTM:", (last_sell_price - last_buy_price))
    
    '''
         else:
     
                print("iBuyFlag11:",iBuyFlag)
                print("iSellFlag22:",iSellFlag)
                print("22:",df['Position'].iat[d] == -1)
                print("33:",df['Position'].iat[d] == 1)
                print("44:",np.where(df['Position'].iat[d] == -1,1,0))
'''
                
## Let's see the profitability of long trades

df["Trade_Price"] = df.loc[(df["Position"] == 1) | (df["Position"] == -1), "Close"] 
        ##    df["Trade_MTM"] =   "Trade_Price": df.loc[(df["Position"] == 1, "Trade_Price"],
       ## "Trade_MTM": pd.Series(df["Trade_Price"] - df["Trade_Price"].shift(1)).loc

## Save to CSV
df.to_csv(r'C:\export_dataframe.csv', index = False, header=True)
