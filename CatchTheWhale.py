import requests
from datetime import datetime, timedelta
from Whale import Whale


def UnixToTehran(unix):
    return (datetime.fromtimestamp(unix) - timedelta(hours=4, minutes=30))


def GetWhales(sec):
    if(sec > 3600):
        return None
    dt = datetime.now()
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    unixTime = round(timestamp - 16200)

    parameters = {
        "api_key": "YTwfGqQDv0kYdCDLmNkjqr2eRmVGnjzS",
        "start": str(unixTime - (sec-5))
    }
    result = requests.get(
        url="https://api.whale-alert.io/v1/transactions", params=parameters).json()
    listOfWhales = list()
    if result['count'] == 0:
        return None
    for i in result['transactions']:
        isUp = int()
        if i['symbol'] == 'usdt':
            isUp = 2
        if 'owner' not in i['from']:
            if 'owner' in i['to']:
                if isUp != 2:
                    isUp = 0
                listOfWhales.append(Whale('unknown', i['to']['owner'], i['amount'], i['amount_usd'], i['symbol'],
                                          datetime.fromtimestamp(int(i['timestamp']) + 16200) - timedelta(hours=4, minutes=30), isUp))

        if 'owner' not in i['to']:
            if 'owner' in i['from']:
                if isUp != 2:
                    isUp = 1
                listOfWhales.append(Whale(i['from']['owner'], 'unknown', i['amount'], i['amount_usd'], i['symbol'],
                                          datetime.fromtimestamp(int(i['timestamp']) + 16200) - timedelta(hours=4, minutes=30), isUp))
            # listOfWhales[len(listOfWhales)-1].IsUp = 2
    return listOfWhales

    # print('from', i['from']['owner_type'], 'to', i['to']['owner_type'], f"{int(round(i['amount_usd'])):,}",
    #       '$', i['symbol'], 'transacted at',
    #       datetime.fromtimestamp(int(i['timestamp']) + 16200) - timedelta(hours=4, minutes=30))]
