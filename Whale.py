import datetime

class Whale(object):
    From = str()
    To = str()
    Amount = int()
    AmountUsd = int()
    Symbol = str()
    Time = datetime.datetime
    IsUp = int()

    def __init__(self, fromm=None, to=None, amount=None, amountUsd=None, symbol=None, time=None, isUp=None):
        self.From = fromm
        self.To = to
        self.Amount = amount
        self.AmountUsd = amountUsd
        self.Symbol = symbol
        self.Time = time
        self.IsUp = isUp

    def __str__(self):
        isUp = str()
        if self.IsUp == 0:
            isUp = '|D|'
        elif self.IsUp == 1:
            isUp = '|U|'
        elif self.IsUp == 2:
            isUp = '|T|'
        return f'{isUp} From: {self.From} To: {self.To} |{self.Amount:,} : ${self.AmountUsd:,}| {self.Symbol} At: {self.Time}'
