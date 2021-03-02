import pyupbit
import urllib3
import pandas as pd
import pprint

# warning message 무시
urllib3.disable_warnings()
pd.options.display.float_format = "{:.1f}".format
tickers = pyupbit.get_tickers('KRW')
# pprint.pprint(tickers)

for a in tickers:
    if 'LINK' in a:
        # print(f"Found it! {a}")
        pass

chart = pyupbit.get_ohlcv(ticker="KRW-ADX")
# print(chart)

# 5일 이동평균 구하기
ma5 = chart['close'].rolling(5).mean()

# 현재 종가가 정해지지 않았기 때문에 전날의 ma5값을 읽어온다.
last_ma5 = ma5[-2]

price = pyupbit.get_current_price(ticker="KRW-ADX")

if price > last_ma5:
    print(f"현재가 {price}이고, 전일 MA5가 {last_ma5} 이므로 상승장")
else:
    print(f"현재가 {price}이고, 전일 MA5가 {last_ma5} 이므로 하락장")

