import math
from operator import le
from os import terminal_size
from pandas.core.algorithms import diff, factorize
from pandas.core.frame import DataFrame
from datetime import datetime, timedelta
from binance.client import Client
import pandas as pd
import numpy as np
from enum import Enum
from shapely.geometry import LineString

client = Client('b8ZKmvQQw08XSm5LShuC2aEmLsuqxTDYsFrVqLpaeFJ13WjkjVshuW5HkW0FZSZQ',
                'VtrYrBVto7UfO7ZtlgEyucrNnndOSRDCrmtYrYvC4WZO6Xnv24HM5kWKp4SpowsM')


def precision(no, per):
    return float((no * (100 - per)) / 100)


def slope(x1=float, x2=float, y1=float, y2=float):
    # input: float, float, float, float
    # output: float
    return (y2 - y1) / (x2 - x1)


def GetPriceOfToken(symbol=str):
    # input: str
    # output: float
    prices = client.get_all_tickers()
    for i in prices:
        if i['symbol'] == f"{symbol.upper()}USDT":
            return float(i['price'])
    return None


def getCandles(symbol=str(), timeFrame=int()):
    # input: dataframe {     str(), int()     }
    # output: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }

    candles = list(client.get_historical_klines_generator(
        f"{symbol.upper()}USDT", Client.KLINE_INTERVAL_1HOUR, f"{timeFrame} day ago UTC"))
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume = []
    for candle in candles:
        dates.append(datetime.fromtimestamp(int(candle[0]) / 1000))
        open_data.append(float(candle[1]))
        high_data.append(float(candle[2]))
        low_data.append(float(candle[3]))
        close_data.append(float(candle[4]))
        volume.append(float(candle[5]))

    klines = {'date': dates, 'open': open_data,
              'high': high_data, 'low': low_data, 'close': close_data, 'volume': volume}
    return pd.DataFrame.from_dict(klines)


def getCandles4Hour(symbol=str(), timeFrame=int()):
    # input: dataframe {     str(), int()     }
    # output: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }

    candles = list(client.get_historical_klines_generator(
        f"{symbol.upper()}USDT", Client.KLINE_INTERVAL_4HOUR, f"{timeFrame} day ago UTC"))
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume = []
    for candle in candles:
        dates.append(datetime.fromtimestamp(int(candle[0]) / 1000))
        open_data.append(float(candle[1]))
        high_data.append(float(candle[2]))
        low_data.append(float(candle[3]))
        close_data.append(float(candle[4]))
        volume.append(float(candle[5]))

    klines = {'date': dates, 'open': open_data,
              'high': high_data, 'low': low_data, 'close': close_data, 'volume': volume}
    return pd.DataFrame.from_dict(klines)


def getCandlesDaily(symbol=str(), timeFrame=int()):
    # input: dataframe {     str(), int()     }
    # output: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }

    candles = list(client.get_historical_klines_generator(
        f"{symbol.upper()}USDT", Client.KLINE_INTERVAL_1DAY, f"{timeFrame} day ago UTC"))
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume = []
    for candle in candles:
        dates.append(datetime.fromtimestamp(int(candle[0]) / 1000))
        open_data.append(float(candle[1]))
        high_data.append(float(candle[2]))
        low_data.append(float(candle[3]))
        close_data.append(float(candle[4]))
        volume.append(float(candle[5]))

    klines = {'date': dates, 'open': open_data,
              'high': high_data, 'low': low_data, 'close': close_data, 'volume': volume}
    return pd.DataFrame.from_dict(klines)


def indicateMacd(df=DataFrame()):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }
    # output: dataframe {     date:list(), macd:list(), signal:list()     }

    shortEma = df.close.ewm(span=12, adjust=False).mean()
    longEma = df.close.ewm(span=26, adjust=False).mean()
    macd = shortEma - longEma
    signal = macd.ewm(span=9, adjust=False).mean()
    result = {'date': list(df['date']), 'macd': macd, 'signal': signal}
    return pd.DataFrame.from_dict(result)


def calcRsi(series=list()):
    # input: list(float)
    # output: list(float)

    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    # first value is sum of avg gains
    u[u.index[13]] = np.mean(u[:14])
    u = u.drop(u.index[:(13)])
    # first value is sum of avg losses
    d[d.index[13]] = np.mean(d[:14])
    d = d.drop(d.index[:(13)])
    rs = pd.DataFrame.ewm(u, com=13, adjust=False).mean() / \
        pd.DataFrame.ewm(d, com=13, adjust=False).mean()
    return 100 - 100 / (1 + rs)


def isOrderedInLastHour(symbol=str):
    # input: str
    # output: bool

    trades = client.get_my_trades(symbol=f'{symbol.upper()}USDT')
    for i in trades:
        if(round(int(i['time']) / 1000) > (round(datetime.now().timestamp()) - 4200)):
            return True
    return False


def portfolioCheck(symbol=str, below=5):
    # input: str, int
    # output: bool

    balance = client.get_asset_balance(asset=symbol.upper())
    assetValue = GetPriceOfToken(symbol)
    price = assetValue * float(balance['free'])
    if price > below:
        return True
    return False


def getUsdtAmount():
    # input:
    # output: float

    balance = client.get_asset_balance(asset='USDT')
    return float(balance['free'])


def getSupport(symbol=str, fromDay=int):
    # input: str, int
    # output: dict {'min': float, 'date': datetime}

    candles = list(client.get_historical_klines_generator(
        f"{symbol.upper()}USDT", Client.KLINE_INTERVAL_1HOUR, f"{fromDay} day ago UTC"))
    min = float(candles[0][4])
    minDate = datetime
    for i in candles:
        no = float(i[4])
        if no < min:
            min = no
            minDate = datetime.fromtimestamp(int(i[0]) / 1000)
    return {'min': min, 'date': minDate}


def getResistance(symbol=str, fromDay=int):
    # input: str, int
    # output: dict {'min': float, 'date': datetime}

    candles = list(client.get_historical_klines_generator(
        f"{symbol.upper()}USDT", Client.KLINE_INTERVAL_1HOUR, f"{fromDay} day ago UTC"))
    max = float(candles[0][4])
    maxDate = datetime
    for i in candles:
        no = float(i[4])
        if no > max:
            max = no
            maxDate = datetime.fromtimestamp(int(i[0]) / 1000)
    return {'max': max, 'date': maxDate}


def isMacdOK(candels=DataFrame):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }
    # output: RES:int

    macdIndicator = indicateMacd(candels)
    length = len(macdIndicator['macd']) - 1
    # MACD
    mx1 = macdIndicator['date'][length - 1].timestamp()
    my1 = macdIndicator['macd'][length - 1]
    mx2 = macdIndicator['date'][length].timestamp()
    my2 = macdIndicator['macd'][length]
    # Signal
    sx1 = macdIndicator['date'][length - 1].timestamp()
    sy1 = macdIndicator['signal'][length - 1]
    sx2 = macdIndicator['date'][length].timestamp()
    sy2 = macdIndicator['signal'][length]
    macdLine = LineString([(mx1, my1), (mx2, my2)])
    signalLine = LineString([(sx1, sy1), (sx2, sy2)])
    # print(
    #     f"{bcolors.OKGREEN}{macdIndicator['date'][length-1]}|{macdIndicator['macd'][length-1]}{bcolors.ENDC} , {bcolors.OKBLUE}{macdIndicator['date'][length-1]}|{macdIndicator['signal'][length-1]}{bcolors.ENDC}")
    # print(
    #     f"{bcolors.OKGREEN}{macdIndicator['date'][length]}|{macdIndicator['macd'][length]}{bcolors.ENDC} , {bcolors.OKBLUE}{macdIndicator['date'][length]}|{macdIndicator['signal'][length]}{bcolors.ENDC}")
    if macdLine.intersects(signalLine) == True:
        macdSlope = slope(mx1, mx2, my1, my2)
        signalSlop = slope(sx1, sx2, sy1, sy2)
        if(macdSlope > signalSlop and my2 > sy2):
            return 100
        else:
            return -100
    else:
        return 0


def __sliceCandels(candels=DataFrame, fromm=int(0), till=int(1000000000)):
    length = len(candels['date'])
    indexes = list()
    dates = list()
    opens = list()
    highs = list()
    lows = list()
    closes = list()
    for i in range(length):
        if i > till or i <= fromm:
            pass
        else:
            indexes.append(i)
            dates.append(candels['date'][i])
            opens.append(candels['open'][i])
            highs.append(candels['high'][i])
            lows.append(candels['low'][i])
            closes.append(candels['close'][i])

    result = {'date': dates, 'open': opens, 'high': highs,
              'low': lows, 'close': closes, 'index': indexes}
    final =  pd.DataFrame.from_dict(result)
    return final


def isRsiOk(candels=DataFrame):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }
    # output: int

    rsi = list(calcRsi(candels['close']))
    length = len(rsi)
    lastRsi = rsi[length - 1]
    x1 = rsi[length - 2]
    y1 = candels['date'][length - 2].timestamp()
    x2 = rsi[length - 1]
    y2 = candels['date'][length - 1].timestamp()
    lineSlope = slope(x1, x2, y1, y2)
    if lastRsi <= 30 and lineSlope > 0:
        return 50
    elif lastRsi >= 70 and lineSlope < 0:
        return -50
    else:
        return 0


def awesomeOscillator(candels=DataFrame()):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }
    # output: list(float)

    mps = list()
    aos = list()
    for i in range(len(candels['close'])):
        mps.append(
            {'data': float((float(candels['high'][i]) + float(candels['low'][i])) / 2)})
        mpspd = pd.DataFrame.from_dict(mps)
        sma5 = mpspd.data.rolling(5).mean()
        sma34 = mpspd.data.rolling(34).mean()
        aos.append(sma5[len(sma5) - 1] - sma34[len(sma34) - 1])
    return aos


def __calcFib(min=float, max=float, fib=list, isSupport=False):
    differ = max - min
    result = list()
    if len(fib) > 0:
        if isSupport:
            for i in fib:
                result.append(max - (differ * i))
        else:
            for i in fib:
                result.append(min + (differ * i))
    return result


def fibRetracementResistance(candels=DataFrame(), fib=list({0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2, 2.618, 3.618, 4.236})):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }, list(float)
    # output: list(float)

    result = list()
    # fib = {0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.414, 1.618, 2, 2.272,
    #        2.414, 2.618, 3, 3.272, 3.414, 3.618, 4, 4.272, 4.414, 4.618, 4.764}

    ao = awesomeOscillator(candels)
    x1 = ao[len(ao) - 2]
    y1 = candels['date'][len(ao) - 2].timestamp()
    x2 = ao[len(ao) - 1]
    y2 = candels['date'][len(ao) - 1].timestamp()
    lastSlope = firstSlope = slope(x1, x2, y1, y2)

    for i in range(len(ao) - 2, 2, -1):
        x1 = ao[i - 1]
        y1 = candels['date'][i - 1].timestamp()
        x2 = ao[i]
        y2 = candels['date'][i].timestamp()
        slop = slope(x1, x2, y1, y2)
        if lastSlope >= 0:
            if slop < 0:
                # turn twords down (MIN)
                lastSlope = slop
                result.append({'candle': {'date': candels['date'][i], 'open': candels['open'][i], 'high': candels['high'][i],
                                          'low': candels['low'][i], 'close': candels['close'][i]}, 'isMax': False})
        elif lastSlope < 0:
            if slop > 0:
                # turn twords up  (MAX)
                lastSlope = slop
                result.append({'candle': {'date': candels['date'][i], 'open': candels['open'][i], 'high': candels['high'][i],
                                          'low': candels['low'][i], 'close': candels['close'][i]}, 'isMax': False})

    if len(result) > 0:
        if firstSlope < 0:
            # skip first
            result = result[1:]

        if len(result) > 2:
            low = {'date': result[0]['candle']['date'],
                   'data': float(result[0]['candle']['low'])}
            high = {'date': result[1]['candle']['date'],
                    'data': float(result[1]['candle']['high'])}
            return __calcFib(low['data'], high['data'], fib)


def fibRetracementSupport(candels=DataFrame(), fib=list({0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2, 2.618, 3.618, 4.236})):
    # input: dataframe {     date:list(), open:list(), hign:list(), low:list(), close:list()     }, list(float)
    # output: list(float)

    result = list()
    # fib = {0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.414, 1.618, 2, 2.272,
    #        2.414, 2.618, 3, 3.272, 3.414, 3.618, 4, 4.272, 4.414, 4.618, 4.764}

    ao = awesomeOscillator(candels)
    x1 = ao[len(ao) - 2]
    y1 = candels['date'][len(ao) - 2].timestamp()
    x2 = ao[len(ao) - 1]
    y2 = candels['date'][len(ao) - 1].timestamp()
    lastSlope = firstSlope = slope(x1, x2, y1, y2)

    for i in range(len(ao) - 2, 2, -1):
        x1 = ao[i - 1]
        y1 = candels['date'][i - 1].timestamp()
        x2 = ao[i]
        y2 = candels['date'][i].timestamp()
        slop = slope(x1, x2, y1, y2)
        if lastSlope >= 0:
            if slop < 0:
                # turn twords down (MIN)
                lastSlope = slop
                result.append({'candle': {'date': candels['date'][i], 'open': candels['open'][i], 'high': candels['high'][i],
                                          'low': candels['low'][i], 'close': candels['close'][i]}, 'isMax': False})
        elif lastSlope < 0:
            if slop > 0:
                # turn twords up  (MAX)
                lastSlope = slop
                result.append({'candle': {'date': candels['date'][i], 'open': candels['open'][i], 'high': candels['high'][i],
                                          'low': candels['low'][i], 'close': candels['close'][i]}, 'isMax': False})

    if len(result) > 0:
        if firstSlope > 0:
            # skip first
            result = result[1:]

        if len(result) > 2:
            high = {'date': result[0]['candle']['date'],
                    'data': float(result[0]['candle']['high'])}
            low = {'date': result[1]['candle']['date'],
                   'data': float(result[1]['candle']['low'])}
            return __calcFib(low['data'], high['data'], fib=fib, isSupport=True)


def isInFisinity(mainNo, secondNo, persentage=1):
    if persentage > 100 or persentage < 0:
        return False

    no = (mainNo * persentage) / 100
    if (mainNo + no) >= secondNo and (mainNo - no) <= secondNo:
        return True
    return False


def rsiDivergenceBuy(candles, rsi_array, precisionNo=100):
    prices = list(candles['close'])
    dates = list(candles['date'])

    price_lows = []
    rsi_lows = []
    datesRes = []
    # Price lows
    for i in range(14, len(prices)):
        datesRes.append(dates[i])
        if i == 0 and prices[i] <= prices[i + 1]:
            price_lows.append(prices[i])
        elif i == len(prices) - 1 and prices[i] <= prices[i - 1]:
            price_lows.append(prices[i])
        elif prices[i - 1] >= prices[i] <= prices[i + 1]:
            price_lows.append(prices[i])
        else:
            price_lows.append(-1)

    # calcRsi lows
    for i in range(len(rsi_array)):
        if i == 0 and rsi_array[i] <= rsi_array[i + 1]:
            rsi_lows.append(rsi_array[i])
        elif i == len(rsi_array) - 1 and rsi_array[i] <= rsi_array[i - 1]:
            rsi_lows.append(rsi_array[i])
        elif rsi_array[i - 1] >= rsi_array[i] <= rsi_array[i + 1]:
            rsi_lows.append(rsi_array[i])
        else:
            rsi_lows.append(-1)

    secondPrices = list()
    secondRsis = list()
    secondDates = list()
    for i in range(len(price_lows)):
        if price_lows[i] != -1:
            secondPrices.append(price_lows[i])
            secondRsis.append(rsi_lows[i])
            secondDates.append(datesRes[i])

    min_price = math.inf
    min_rsi = 0
    selectedDate = dates[0]
    for i in range(1, len(secondPrices)):

        if secondPrices[i] + precision(secondPrices[i], precisionNo) < secondPrices[i - 1] and secondRsis[i] > secondRsis[i - 1] + precision(secondRsis[i - 1], precisionNo):
            min_price = secondPrices[i]
            min_rsi = secondRsis[i]
            selectedDate = secondDates[i]

    return (min_price, min_rsi, selectedDate)


def rsiDivergenceSell(candles, rsi_array, precisionNo=100):
    prices = list(candles['close'])
    dates = list(candles['date'])
    price_highs = []
    rsi_highs = []
    datesRes = []
    # Price lows
    for i in range(14, len(prices)):
        datesRes.append(dates[i])
        if i == 0 and prices[i] >= prices[i + 1]:
            price_highs.append(prices[i])
        elif i == len(prices) - 1 and prices[i] >= prices[i - 1]:
            price_highs.append(prices[i])
        elif prices[i - 1] <= prices[i] >= prices[i + 1]:
            price_highs.append(prices[i])
        else:
            price_highs.append(-1)

    # calcRsi lows
    for i in range(len(rsi_array)):
        if i == 0 and rsi_array[i] >= rsi_array[i + 1]:
            rsi_highs.append(rsi_array[i])
        elif i == len(rsi_array) - 1 and rsi_array[i] >= rsi_array[i - 1]:
            rsi_highs.append(rsi_array[i])
        elif rsi_array[i - 1] <= rsi_array[i] >= rsi_array[i + 1]:
            rsi_highs.append(rsi_array[i])
        else:
            rsi_highs.append(-1)

    secondPrices = list()
    secondRsis = list()
    secondDates = list()
    for i in range(len(price_highs)):
        if price_highs[i] != -1:
            secondPrices.append(price_highs[i])
            secondRsis.append(rsi_highs[i])
            secondDates.append(datesRes[i])

    selectedDate = dates[0]
    maxPriceRes = 0
    maxRsiRes = math.inf
    for i in range(1, len(secondPrices)):
        if secondPrices[i] > secondPrices[i - 1] + precision(secondPrices[i], precisionNo) and secondRsis[i] + precision(secondRsis[i], precisionNo) < secondRsis[i - 1]:
            maxPriceRes = secondPrices[i]
            maxRsiRes = secondRsis[i]
            selectedDate = secondDates[i]

    return (maxPriceRes, maxRsiRes, selectedDate)


def simplifyDate(date=datetime):
    if date.minute <= 30:
        if date.hour == 0:
            return datetime(date.year, date.month, date.day, 23, 30, 0)
        else:
            return datetime(date.year, date.month, date.day, date.hour - 1, 30, 0)
    else:
        dte = datetime(date.year, date.month, date.day, date.hour, 30, 0)
        return dte


c7Crossed25 = 0

def setC7Crossed25(input=False):
    global c7Crossed25    # Needed to modify global copy of globvar
    c7Crossed25 = input


def LaliIndicator(candlesIn4HourFromat=DataFrame()):

    ma7 = candlesIn4HourFromat.close.ewm(span=7, adjust=False).mean()
    ma25 = candlesIn4HourFromat.close.ewm(span=25, adjust=False).mean()
    ma99 = candlesIn4HourFromat.close.ewm(span=99, adjust=False).mean()
    date = list(candlesIn4HourFromat['date'])
    # print(len(ma7), len(ma25), len(ma99), len(list(candlesIn4HourFromat['date'])))
    length = len(date) - 1

    # MA7
    ma7x1 = date[length - 1].timestamp()
    ma7y1 = ma7[length - 1]
    ma7x2 = date[length].timestamp()
    ma7y2 = ma7[length]

    # MA25
    ma25x1 = date[length - 1].timestamp()
    ma25y1 = ma25[length - 1]
    ma25x2 = date[length].timestamp()
    ma25y2 = ma25[length]

    # MA99
    ma99x1 = date[length - 1].timestamp()
    ma99y1 = ma99[length - 1]
    ma99x2 = date[length].timestamp()
    ma99y2 = ma99[length]

    ma7Line = LineString([(ma7x1, ma7y1), (ma7x2, ma7y2)])
    ma25Line = LineString([(ma25x1, ma25y1), (ma25x2, ma25y2)])
    ma99Line = LineString([(ma99x1, ma99y1), (ma99x2, ma99y2)])

    if ma7Line.intersects(ma25Line) == True:
        ma7Slope = slope(ma7x1, ma7x2, ma7y1, ma7y2)
        ma25Slop = slope(ma25x1, ma25x2, ma25y1, ma25y2)
        if ma7Slope > ma25Slop and ma7y2 > ma25y2:
            setC7Crossed25(True)
        if ma7Slope < ma25Slop and ma7y2 < ma25y2:
            setC7Crossed25(False)

    if c7Crossed25 == True:
        if ma25Line.intersects(ma99Line):
            ma25Slope = slope(ma25x1, ma25x2, ma25y1, ma25y2)
            ma99Slope = slope(ma99x1, ma99x2, ma99y1, ma99y2)
            if ma25Slope > ma99Slope and ma25y2 > ma99y2:
                return True
    
    return False


# candles = getCandles4Hour('btc', 400)
# print(len(candles['date']))
# for i in range(200, 2400):
#     can = __sliceCandels(candles, till=i)
#     length = len(can['date'])
#     print(can['date'][length - 1])
#     buy = LaliIndicator(can)
#     if buy:
#         print("BUY")



# candles = getCandles('zil', 10)
# rsi = list(calcRsi(candles['close']))
# buy = rsiDivergenceBuy(candles, rsi, precisionNo=100)
# sell = rsiDivergenceSell(candles, rsi)

# print('buy', buy)
# print('sell', sell)


# __fib = list({0, 0.236, 0.382, 0.5, 0.618, 0.786,
#             1, 1.618, 2, 2.618, 3.618, 4.236})
# candels = getCandlesDaily('bnb', 100)
# fibResult = fibRetracementSupport(candels=candels, fib=__fib)
# for i in fibResult:
#     print(i)


# for i in fibResult:
#     print(isInFisinity(i, candels['close'][len(candels['close']) - 1]))
