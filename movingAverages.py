import streamlit as st
import os
import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt 
import requests
import math
from termcolor import colored as cl 
import numpy as np

def moving_average():
    #streamlit app
    st.title("Moving Average Analysis")
    with st.expander(label="Know more about Moving Averages"):
        st.write("A moving average is a technical indicator that market analysts and investors may use to determine the direction of a trend. It sums up the data points of a financial security over a specific time period and divides the total by the number of data points to arrive at an average. It is called a “moving” average because it is continually recalculated based on the latest price data. When the price of an asset crosses above or below its moving average, it is considered a potential buying or selling signal, respectively. Conversely, if the price of the stock crosses below its moving average, it may be interpreted as a signal that the stock is continuing its downtrend and could be a potential selling opportunity.")
    #set fixed parameters
    plt.style.use('fivethirtyeight')
    plt.rcParams['figure.figsize'] = (15, 8)

    #grab market data using alpaca
    def get_ticker_data(ticker, days):
        data = yf.download(ticker, period=f"{days}d")
        return data

    #calculate the moving averages for both strategies
    def calc_moving_average(data, symbol, windows):
        for i in range(len(windows)):
            data[f'{windows[i]} day MA'] = data.Close.rolling(window=windows[i]).mean()

        if len(windows) > 1:
            data = data[data[f'{windows[1]} day MA'].notnull()]
        else:
            data = data[data[f'{windows[0]} day MA'].notnull()]

        return data


    #backtest for both strategies
    def ma_backtest(data, window, strategy='single', sellShort=False, slippage=0.003):
        '''
        data is a df that contains the closing price of the stock and moving averages
        window can be a single value for price crossover or a list for moving average crossover
        crossover equals price or ma to determine which strategy should be use
        '''
        # catch the enabling of short selling at the beginning
        if sellShort:
            sellSignal = -1
        else:
            sellSignal = 0

        # vectorized backtests by strategy
        if strategy == 'Single Moving Average':
            data['Side'] = np.where(data.Close >= data[f'{window[0]} day MA'], 1, sellSignal)
        elif strategy == 'Crossover Moving Average':
            data['Side'] = np.where(data[f'{window[0]} day MA'] >= data[f'{window[1]} day MA'], 1, sellSignal)

        # metrics for calculating return
        data['LagPrice'] = data['Close'].shift(1)
        data['PctChange'] = ((data['Close'] - data['LagPrice']) / data['LagPrice']).shift(-1)

        # variables to capture the buy and sell prices
        buyPrice = []
        sellPrice = []

        # Logic for noting each buy and sell by strategy/short selling included
        for i in range(len(data.Close)):
            if data['Side'][i] > data['Side'][i - 1]:
                buyPrice.append(data.Close[i])
                sellPrice.append(np.nan)
            elif data['Side'][i] < data['Side'][i - 1]:
                sellPrice.append(data.Close[i])
                buyPrice.append(np.nan)
            else:
                if i < 1:
                    if data.Side[i] < 0:
                        sellPrice.append(data.Close[i])
                        buyPrice.append(np.nan)
                    elif data.Side[i] == 0:
                        buyPrice.append(np.nan)
                        sellPrice.append(np.nan)
                    else:
                        buyPrice.append(data.Close[i])
                        sellPrice.append(np.nan)
                else:
                    buyPrice.append(np.nan)
                    sellPrice.append(np.nan)

        # putting it all together
        data['buyPrice'] = buyPrice
        data['sellPrice'] = sellPrice
        data['Slippage'] = ((data.buyPrice.fillna(0) + data.sellPrice.fillna(0)) * slippage) / data.Close
        data['Return'] = data.Side * data.PctChange - data.Slippage
        data['Return'][0] = -data.Slippage[0]  
        data['Cumulative'] = data.Return.cumsum()

        return data

    #tell the story with some visuals
    def plot(data,windows,strategy):
        plt.plot(data['Close'], alpha = 0.3, label = ticker)
        
        if len(windows) > 1:
            plt.plot(data[f'{window[0]} day MA'], alpha = 0.6, label = f'{window[0]} day MA')
            plt.plot(data[f'{window[1]} day MA'], alpha = 0.6, label = f'{window[1]} day MA')
        else:
            plt.plot(data[f'{window[0]} day MA'], alpha = 0.6, label = f'{window[0]} day MA')
            
        plt.scatter(data.index, data.buyPrice, marker = '^', s = 200, color = 'darkblue', label = 'BUY SIGNAL')
        plt.scatter(data.index, data.sellPrice, marker = 'v', s = 200, color = 'crimson', label = 'SELL SIGNAL')
        plt.legend(loc = 'upper left')

        plt.title(f'{ticker} {strategy} Trading Signals')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        return plot

    #inputs from user
    ticker = st.text_input("Please enter a ticker symbol","SPY").upper()
    days = st.number_input("Please enter the number of days of data you would like",30)
    strategy = st.radio('Select Strategy', ['Single Moving Average','Moving Average Crossover'])

    #filter moving average windows by strategy
    if strategy == 'Single Moving Average':
        single_ma = st.number_input("Please enter your moving average window",5)
        single_ma = [single_ma]
        strategy = 'Single Moving Average'
        window = single_ma
    else:
        lma = st.number_input("Please enter your long MA window",30)
        sma = st.number_input("Please enter your short MA window",5)
        strategy = 'Crossover Moving Average'
        window = [sma,lma]

    #short selling optioin
    enable_short = st.radio('Enable Short Selling',['Yes','No'])
    if enable_short == 'Yes':
        sellShort = True
    else:
        sellShort = False

    #main, after everything is set up. Run it through each of the functions
    data = get_ticker_data(ticker, days)
    data = calc_moving_average(data, ticker, window)
    sma_trade = ma_backtest(data, window, strategy, sellShort)
    plot(sma_trade, window, strategy)
    st.pyplot()

    strategy_return = sma_trade.Cumulative.iloc[-2]
    buy_hold = ((sma_trade.Close[-1]-sma_trade.Close[0])/sma_trade.Close[0])

    if strategy_return > buy_hold:
        st.success('Percent return on this strategy would have been {:.2%}'.format(strategy_return))
        st.info('Percent return on buy and hold would have been {:.2%}'.format(buy_hold))
    else:
        st.warning('Percent return on this strategy would have been {:.2%}'.format(strategy_return))
        st.success('Percent return on buy and hold would have been {:.2%}'.format(buy_hold))

    st.markdown("---")
    st.subheader("Detailed Breakdown")
    st.table(data)
