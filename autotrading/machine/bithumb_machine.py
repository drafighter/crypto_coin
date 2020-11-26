import pybithumb
from autotrading.machine.base_machine import Machine
import configparser
import time
import requests


# tickers = pybithumb.get_tickers()
# price = pybithumb.get_current_price("BTC")
#
# print(tickers)
# print(price)

class BithumbMachine(Machine):
    """
    빗썸 거래소와 거래를 위한 클래스입니다.
    BASE_API_URL은 REST API호출의 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 빗썸에서 거래가 가능한 화폐의 종류입니다.
    """
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC", "XRP", "ALL"]

    def __init__(self):
        """
        BithumbMachine 클래스의 최초 호출 메소드 입니다.
        config.ini파일에서 connect_key, secret_key, username을 읽어옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect key']
        self.CLIENT_SECRET = config['BITHUMB']['secret key']
        self.USER_NAME = config['BITHUMB']['username']

    def get_ticker(self, order_currency=None, payment_currency="KRW"):
        """마지막 체결정보(Tick)을 얻기 위한 메소드입니다.
        Args:
            order_currency(str):화폐 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어있습니다.
            payment_currency(str):결제 통화(마켓), 기본값 : KRW
        Returns:
            결과를 딕셔너리로 반환합니다.
            결과의 필드는 timestamp, last, bid, ask, high, low, volume이 있습니다.
        """
        if order_currency is None:
            raise Exception('Need to currency type')
        if order_currency not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)

        ticker_api_path = "/public/ticker/{}_{}".format(order_currency, payment_currency)

        url_path = self.BASE_API_URL + ticker_api_path

        print(url_path)
        res = requests.get(url_path, verify=False)
        response_json = res.json()

        result = {}

        result["timestamp"] = str(response_json['data']["date"])
        result["last"] = response_json['data']["closing_price"]
        result["open"] = response_json['data']["opening_price"]
        result["prelast"] = response_json['data']["prev_closing_price"]
        result["high"] = response_json['data']["max_price"]
        result["low"] = response_json['data']["min_price"]
        result["volume"] = response_json['data']["units_traded_24H"]
        return result


