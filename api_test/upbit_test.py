import requests
import pyupbit
import pandas as pd
import pprint

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
# tickers = pyupbit.get_tickers(fiat="BTC")
# print(tickers)
# print(len(tickers))

# 실수 소수점 1자리까지 표시설정

pd.options.display.float_format = "{:.1f}".format

# 시세캔들조회
df = pyupbit.get_ohlcv(ticker="KRW-BTC", interval="month", count=200)
print(df)
# df.to_excel("week_btc.xls")

# 현재가조회
# url = "http://api.upbit.com/v1/ticker"
# params = {"markets": "KRW-XRP"}
# resp = requests.get(url=url, params=params)
# data = resp.json()
# print(data)
# print("정식 api 이용 현재가조회", data[0]["trade_price"])
#
# price = pyupbit.get_current_price(ticker="KRW-XRP")
# print("래퍼 이용 현재가 조회 ", price)

# 연습문제
# 1. 업비트 원화시장에서 거래되는 모든 암호화폐 구하기
# upbit_krw_coins = pyupbit.get_tickers("KRW")

# 2. 하나씩 현재가 구하기
# 때마침 다수 종목 현재가 구할때 인자롤 리스트를 넘겨주면됨.
# 그러면 리턴값은 dictionary 로 리턴됨
# dictionary 화면 출력 for 문 작성
# coin_current_prices = {}
# coin_current_prices = pyupbit.get_current_price(upbit_krw_coins)
#
# for (k, v) in coin_current_prices.items():
#     print("%s 코인의 현재가는 %s" % (k, v))
#
# print("원화 암호화폐 갯수는 ", len(upbit_krw_coins))

# 호가정보 조회
# orderbooks = pyupbit.get_orderbook("KRW-XRP")
# orderbook = orderbooks[0]
# total_ask_sum = orderbook['total_ask_size']
#
# pprint.pprint(orderbooks[0])
# print(total_ask_sum)

# 매수 1호가와 매도 1호가의 잔량차이는?
# 호가 1번 정보 구하기
# order_no1 = orderbook['orderbook_units'][0]
# pprint.pprint(order_no1)
#
# order_no1_differ_sum = order_no1['ask_size'] - order_no1['bid_size']
# print(order_no1_differ_sum)

# Exchange API
f = open("api_test/upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)

# 계좌잔고조회
# balance = upbit.get_balance("KRW-OBSR")
# balances = upbit.get_balances()
# print(balances)

# xrp limit order
# xrp_price = pyupbit.get_current_price("KRW-XRP")
# print(xrp_price)

# resp = upbit.buy_limit_order("KRW-XRP", 200, 100)
# pprint.pprint(resp)

buy_uuid = '154ac686-e6b3-4db9-a00e-05604dff3fc7'

# 취소
# resp1 = upbit.cancel_order(buy_uuid)
# pprint.pprint(resp1)
