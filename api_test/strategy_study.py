import pyupbit
import urllib3
import pprint

# warning message 무시
urllib3.disable_warnings()

tickers = pyupbit.get_tickers('KRW')
# pprint.pprint(tickers)

for a in tickers:
    if 'LINK' in a:
        # print(f"Found it! {a}")
        pass

chart = pyupbit.get_ohlcv(ticker="KRW-OBSR")
print(chart)
# D-1 종가
d_1_close = chart.iloc[-2]['close']
print(d_1_close)

for i in range(5):
    i = i * -1
    chart.iloc[i]['close']

