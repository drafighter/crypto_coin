import pyupbit
import time
import datetime

# 백데이터 만들기 (일봉 200개)
# df = pyupbit.get_ohlcv()
# print(df)
# df.to_excel("btc.xls")


def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5

    return target


f = open("api_test/upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)

target_value = cal_target("KRW-XRP")
op_mode = False
hold = False

while True:
    now = datetime.datetime.now()

    # 매도시도
    if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
        if op_mode is True and hold is True:
            xrp_balance = upbit.get_balance("KRW-XRP")
            upbit.sell_market_order("KRW-XRP", xrp_balance)
            hold = False

        op_mode = False
        time.sleep(10)

    # 매일 아침 09:00:00 에 그날의 목표가 계산
    if now.hour == 9 and now.minute == 0 and 20 <= now.second <= 30:
        target_value = cal_target("KRW-XRP")
        time.sleep(10)  # 10초 멈춤
        op_mode = True

    price = pyupbit.get_current_price("KRW-XRP")

    # 매수시도
    if op_mode is True and hold is False and price >= target_value:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order("KRW-XRP", krw_balance * 0.01)
        hold = True

    # 상태출력
    print(f"현재시간: {now}, 목표가: {target_value}, 현재가: {price}, 보유상태: {hold}, 동작상태: {op_mode}")

    time.sleep(2)
