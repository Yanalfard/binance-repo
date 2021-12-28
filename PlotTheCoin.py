from operator import truediv
import BinanceRepo
import re
from pandas.core.frame import DataFrame
from datetime import datetime, timedelta
from binance.client import Client
import pandas as pd
import plotly
import numpy as np
from shapely.geometry import LineString
from Colors import bcolors
import time
import winsound
import plotly.graph_objects as go


client = Client('b8ZKmvQQw08XSm5LShuC2aEmLsuqxTDYsFrVqLpaeFJ13WjkjVshuW5HkW0FZSZQ',
                'VtrYrBVto7UfO7ZtlgEyucrNnndOSRDCrmtYrYvC4WZO6Xnv24HM5kWKp4SpowsM')


def fibSays(asset=str):
    asset = asset.replace('USDT', '')
    candels = BinanceRepo.getCandlesDaily(asset, 100)
    fibResultRes = BinanceRepo.fibRetracementResistance(
        candels=candels)
    fibResultSup = BinanceRepo.fibRetracementSupport(
        candels=candels)

    for i in range(len(fibResultRes)):
        lastCandleClose = float(
            candels['close'][len(candels['close']) - 1])
        if BinanceRepo.isInFisinity(fibResultRes[i], lastCandleClose):
            print(f"Fib says -> {bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")
            break
        elif BinanceRepo.isInFisinity(fibResultSup[i], lastCandleClose):
            print(f"Fib says -> {bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
            break


def macdSays(candels=DataFrame()):
    macdResult = BinanceRepo.isMacdOK(candels)
    if macdResult == 100:
        if BinanceRepo.portfolioCheck(asset) == False:
            if BinanceRepo.isOrderedInLastHour(asset) == False:
                print(
                    f"MACD says -> {bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
    elif macdResult == -100:
        if BinanceRepo.portfolioCheck(asset) == True:
            if BinanceRepo.isOrderedInLastHour(asset) == False:
                print(
                    f"MACD says -> {bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")


def rsiSays(candels=DataFrame()):
    rsiResult = BinanceRepo.isRsiOk(candels)
    if rsiResult == 50:
        print(f"RSI says -> {bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
    elif rsiResult == -50:
        print(f"RSI says -> {bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")


def rsiDivergenceSays(candels=DataFrame()):
    rsi = list(BinanceRepo.calcRsi(candels['close']))
    rsiBuyResult = BinanceRepo.rsiDivergenceBuy(candels, rsi, 100)
    rsiSellResult = BinanceRepo.rsiDivergenceSell(candels, rsi, 100)
    now = datetime.now()
    if rsiBuyResult[1] != 0:
        if rsiBuyResult[2] == BinanceRepo.simplifyDate(now) or rsiBuyResult[2] == BinanceRepo.simplifyDate(datetime(now.year, now.month, now.day, now.hour - 1, now.minute)):
            print(f"RSI Divergence says -> {bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
    if rsiSellResult[1] != 0:
        if rsiSellResult[2] == BinanceRepo.simplifyDate(now) or rsiSellResult[2] == BinanceRepo.simplifyDate(datetime(now.year, now.month, now.day, now.hour - 1, now.minute)):
            print(f"RSI Divergence says -> {bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")


# >MACD
# while True:
#     # time.sleep(1)
#     allPrices = client.get_all_tickers()
#     for i in allPrices:
#         asset = i['symbol']
#         if 'USDT' in asset:
#             try:
#                 asset = asset.replace("USDT" , "")
#                 candels = BinanceRepo.getCandles(asset, 10)
#                 macdResult = BinanceRepo.isMacdOK(candels)
#                 if macdResult == 100:
#                     if BinanceRepo.PortfolioCheck(asset) == False:
#                         if BinanceRepo.IsOrderedInLastHour(asset) == False:
#                             print(f"{bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
#                 elif macdResult == -100:
#                     if BinanceRepo.PortfolioCheck(asset) == True:
#                         if BinanceRepo.IsOrderedInLastHour(asset) == False:
#                             print(f"{bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")
#             except:
#                 pass


# >RSI
# while True:
#     allPrices = client.get_all_tickers()
#     print(datetime.now())
#     for i in allPrices:
#         asset = i['symbol']
#         if 'USDT' in asset:
#             try:
#                 asset = asset.replace('USDT', '')
#                 candels = BinanceRepo.getCandles(asset, 10)
#                 rsiResult = BinanceRepo.isRsiOk(candels)
#                 if rsiResult == 50:
#                     print(f"{bcolors.OKGREEN}BUY: {asset}{bcolors.ENDC}")
#                 elif rsiResult == -50:
#                     print(f"{bcolors.OKCYAN}SELL: {asset}{bcolors.ENDC}")
#             except:
#                 pass
#     print(datetime.now())


while True:
    allPrices = client.get_all_tickers()
    print(datetime.now())
    for i in allPrices:
        asset = i['symbol']
        if 'USDT' in asset:
            try:
                asset = asset.replace('USDT', '')
                candles = BinanceRepo.getCandles(asset, 10)

                fibSays(asset)
                macdSays(candles)
                rsiSays(candles)
                rsiDivergenceSays(candles)
            except:
                pass
    print(datetime.now())


# fig = go.Figure(data=[go.Candlestick(x=candels['date'],
#                                      open=candels['open'], high=candels['high'],
#                                      low=candels['low'], close=candels['close'])])
# fig.show()
#
#
# macdLine = go.Scatter(
#     x=macdIndicator['date'],
#     y=macdIndicator['macd'],
#     name='MACD',
#     line=dict(
#         color='rgb(5, 149, 0)'
#     )
# )
#
# SignalLine = go.Scatter(
#     x=macdIndicator['date'],
#     y=macdIndicator['signal'],
#     name='Signal'
# )
#
# data = go.Data([macdLine, SignalLine])
# plotly.offline.iplot(data, filename='basic-line')
