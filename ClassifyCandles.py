import sklearn
import BinanceRepo
import plotly
import plotly.graph_objects as go
from shapely.geometry import LineString


candles = BinanceRepo.getCandles4Hour('bnb', 50)

# print(candles.head())

ma7 = candles.close.ewm(span=7, adjust=False).mean()
ma25 = candles.close.ewm(span=25, adjust=False).mean()
ma99 = candles.close.ewm(span=99, adjust=False).mean()
date = list(candles['date'])

print(len(ma7), len(ma25), len(ma99), len(list(candles['date'])))

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
_7Crossed25 = False

if ma7Line.intersects(ma25) == True:
    macdSlope = BinanceRepo.slope(ma7x1, ma7x2, ma7y1, ma7y2)
    signalSlop = BinanceRepo.slope(ma25x1, ma25x2, ma25y1, ma25y2)
    if(macdSlope > signalSlop and ma7y2 > ma25y2):
        _7Crossed25 = True
        # ma7 has crossed ma25 upwords

# for i in range(len(list(candles['date']))):
#     print(ma7[i], candles['date'][i])
















# ma7Line = go.Scatter(
#     x=candles['date'],
#     y=ma7,
#     name='MA7',
#     line=dict(
#         color='rgb(5, 149, 0)'
#     )
# )

# ma25Line = go.Scatter(
#     x=candles['date'],
#     y=ma25,
#     name='MA25'
# )

# ma99Line = go.Scatter(
#     x=candles['date'],
#     y=ma99,
#     name='MA99'
# )

# data = go.Data([ma7Line, ma25Line, ma99Line])
# plotly.offline.iplot(data, filename='basic-line')