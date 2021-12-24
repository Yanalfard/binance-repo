from binance.client import Client
import CatchTheWhale as eye
import time

client = Client('b8ZKmvQQw08XSm5LShuC2aEmLsuqxTDYsFrVqLpaeFJ13WjkjVshuW5HkW0FZSZQ',
                'VtrYrBVto7UfO7ZtlgEyucrNnndOSRDCrmtYrYvC4WZO6Xnv24HM5kWKp4SpowsM')


def checkPrice(symbol=str()):
    price = client.get_all_tickers()
    for i in price:
        if(i['symbol'] == f'{symbol.upper()}USDT'):
            return i['price']
    return None


def Differ(first=list(), second=list()):
    firstAmtUsd = list()
    firstSymbol = list()
    firstTime = list()
    for i in first:
        firstAmtUsd.append(i.AmountUsd)
        firstSymbol.append(i.Symbol)
        firstTime.append(i.Time)

    result = list()
    for i in second:
        if i.AmountUsd not in firstAmtUsd or i.Symbol not in firstSymbol or i.Time not in firstTime:
            result.append(i)
    return result


def trackWhales(symbol=None):
    first = eye.GetWhales(3000)
    while True:
        time.sleep(5)
        second = eye.GetWhales(3000)
        whales = Differ(first, second)
        first = second

        if whales != None:
            for i in whales:
                if symbol is None or symbol == i.Symbol:
                    print(i)

