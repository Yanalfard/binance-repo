import time
from kucoin.client import Trade
from kucoin.client import Market
from kucoin.client import MarketData
import BinanceRepo as br
import threading

key = '61ca4d605e5fca0001956334'
secret = 'a21d16fd-ba29-4b1b-9566-761cb2aa45fb'
passPhrase = 'Fucking@$$Hole'


def getSymbolData(asset: str):
    asset = asset.upper() + '-USDT'
    symbolClient = MarketData(key=key, secret=secret, passphrase=passPhrase, url='https://api.kucoin.com')
    symbolList = symbolClient.get_symbol_list()
    for i in symbolList:
        if i['symbol'] == asset:
            print(i)


def buy(asset: str):
    # basic buy mechanism MUST BE EVOLVED FOR USE
    asset = asset.upper() + '-USDT'
    client = Trade(key=key, secret=secret, passphrase=passPhrase, url='https://api.kucoin.com')
    result = client.create_market_order(asset, side='buy', size='1')
    print(result)


def main():
    # buy('ftm')
    asset = 'sol'
    res = br.Stalker(asset)
    # for i in res:
    #     print(i['date'], i['status'])

    resLen = len(res) - 1
    readyForOrder = False

    while True:
        time.sleep(5)
        res2 = br.Stalker(asset)
        if str(res2[resLen]['date']) != str(res[resLen]['date']):
            readyForOrder = True
            res = res2
        if readyForOrder:
            if res[resLen]['status'] == True:
                pass
                # BUY
            elif res[resLen]['status'] == False:
                pass
                # SELL
            readyForOrder = False


if __name__ == '__main__':
    main()
