import requests
import pyupbit

# REST API 사용
# url = "https://api.upbit.com/v1/market/all?isDetails=true"
# resp = requests.get(url)
# data = resp.json()
#
# ticker_list = []
# for coin in data:
#     ticker = coin["market"]
#     if ticker.startswith("KRW"):
#         ticker_list.append(ticker)
#
# print(ticker_list)
# print(len(ticker_list))

# pyupbit wrapper 사용
tickers = pyupbit.get_tickers(fiat="BTC")
print(tickers)
print(len(tickers))

# 시세캔들조회
df = pyupbit.get_ohlcv("KRW-BTC", interval="week")
print(df)
df.to_excel("week_btc.xls")


