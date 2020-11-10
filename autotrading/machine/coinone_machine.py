import base64
import hashlib
import hmac
import json
import time

import requests

from autotrading.machine.base_machine import Machine
import configparser


def get_nonce():
    """Private API 호출 시 사용할 nonce 값을 구하는 메서드

    :return:
        nonce 값 반환
    """
    return int(time.time())


def get_encode_payload(payload):
    """
    payload 를 BASE64 로 encoding 후 리턴하는 메소드
    :param payload: access_token, nonce 의 dictionary 객체
    :return: 인코딩된 payload
    """

    dumped_json = json.dumps(payload)
    return base64.b64encode(dumped_json.encode("utf-8"))


def get_signature(encoded_payload, secret_key):
    """
    X-COINONE-PAYLOAD 정보를 서명해서 암호화한 값을 반환하는 메소드
    :param encoded_payload:
    :param secret_key:
    :return: 사용자의 secret_key로 서명된 데이터를 반환
    """

    signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)
    return signature.hexdigest()


class CoinOneMachine(Machine):
    """
    코인원 거래소와 거래를 위한 클래스 입니다.
    BASE_API_URL은 REST API호출의 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 코인원에서 거래가 가능한 화폐의 종류입니다.
    """
    BASE_API_URL = "https://api.coinone.co.kr"
    TRADE_CURRENCY_TYPE = ["btc", "eth", "etc", "bch", "qtum", "krw", "xrp", "iota", "ltc"]

    def __init__(self):
        """
        CoinOneMachine 클래스의 최초 호출 메소드입니다.
        config.ini에서 access_token, secret_key 정보를 읽어옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.access_token = config['COINONE']['access_token']
        self.secret_key = config['COINONE']['secret_key']
        self.expire = None

    def set_token(self, grant_type="refresh_token"):
        """ 인증토큰 정보를 만들기 위한 메소드입니다.
        Returns:
            만료시간(expire), 인증토큰(access_token), 리프레스토큰(refresh_token)을 반환
        Raises:
            grant_type

        """
        token_api_path = "/oauth/refresh_token/"
        url_path = self.BASE_API_URL + token_api_path

        self.expire = 3600

        # 현재 access_token 읽어오기
        config = configparser.ConfigParser()
        config.read("conf/config.ini")

        # grant_type 이 refresh_token 일 경우 access_token 을 재발급 받는다.
        if grant_type == "refresh_token":
            headers = {"content-type": "application/x-www-form-urlencoded"}
            data = {"access_token": self.access_token}
            res = requests.post(url_path, headers=headers, data=data, verify=False)

            # request 후 받은 json 형태의 응답을 python dictionary 객체로 받는다.
            result = res.json()
            print("result : %s, token : %s" % (result, self.access_token))
            if result["result"] == "success":
                self.access_token = result["accessToken"]
                config["COINONE"]["access_token"] = self.access_token
                """
                config.set("COINONE", "access_token", self.access_token) 의 형태로 config 파일을 수정가능함.
                """

                with open("conf/config.ini", "w") as configfile:
                    config.write(configfile)
            else:
                raise Exception("Failed set_token")

        else:
            self.access_token = config["COINONE"]["access_token"]

        return self.expire, self.access_token, self.access_token

    def get_token(self):
        """
        인증토큰 정보를 받기 위한 메소드 입니다.
        
        Returns:
            인증토큰(access_token)이 있는 경우 반환
            
        Raises:
            access_token이 없는 경우 Exception 발생
        """

        if self.access_token is not None:
            return self.access_token
        else:
            raise Exception("Need to set_token")

    def get_wallet_status(self):
        """
        사용자의 지갑정보를 조회하는 메소드입니다.

        Returns:
            사용자의 지갑에 화폐별 잔고를 딕셔너리 형태로 반환합니다.
        """
        time.sleep(1)
        wallet_status_api_path = "/v2/account/balance/"
        url_path = self.BASE_API_URL + wallet_status_api_path

        """
        V2 Private API 인증방식 설명 작성
        1. HTTP Header 에 X-COINONE-PAYLOAD 와 X-COINONE-SIGNATURE 전송
            - X-COINONE-PAYLOAD는 access_token과 nonce 딕셔러리를 json으로 변경한뒤 BASE64로 Encoding 한 객체
            - nonce는 증가하는 정수값으로 int(time.time()) 형태로 적용
        2. signature : 서명은 전송할 데이터를 사용자의 secret_key로 암호화하는 작업
            - HMAC(X-COINONE-PAYLOAD, SECRET_KEY, SHA512).hexdigest()
        """

        payload = {
            "access_token": self.access_token,
            "nonce": get_nonce()
        }
        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        # https://tariat.tistory.com/818 (dictionary, for문과 if문까지 한줄에 작성하기 참조)
        wallet_status = {currency: result[currency] for currency in self.TRADE_CURRENCY_TYPE}
        return wallet_status

    def buy_order(self, currency_type=None, price=None, qty=None, order_type="limit"):
        """
        매수주문을 실행하는 메서드
        :param currency_type: 매수하려는 암호화폐, 기본값은 btc
        :param price: 1개 수량주문에 대한 원화(krw) 값
        :param qty: 주문수량
        :param order_type: 주문타입 (현재 코인원은 지정가 매매만 지원)
        :return: 주문상태 반환
        """

        if order_type != "limit":
            raise Exception("Coinone order type support only limit ")
        time.sleep(1)

        buy_limit_api_path = "/v2/order/limit_buy"
        url_path = self.BASE_API_URL + buy_limit_api_path

        payload = {
            "access_token": self.access_token,
            "price": int(price),
            "qty": float(qty),
            "currency": currency_type,
            "nonce": get_nonce()
        }

        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        return result

    def sell_order(self, currency_type=None, price=None, qty=None, order_type="limit"):
        """
        매도주문을 실행하는 메서드
        :param currency_type: 대도하려는 암호화폐, 기본값은 btc
        :param price: 1개 수량주문에 대한 원화(krw) 값
        :param qty: 주문수량
        :param order_type: 주문타입 (현재 코인원은 지정가 매매만 지원)
        :return: 주문상태 반환
        """

        if order_type != "limit":
            raise Exception("Coinone order type support only limit ")
        time.sleep(1)

        sell_limit_api_path = "/v2/order/limit_sell"
        url_path = self.BASE_API_URL + sell_limit_api_path

        payload = {
            "access_token": self.access_token,
            "price": int(price),
            "qty": float(qty),
            "currency": currency_type,
            "nonce": get_nonce()
        }

        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        return result
    
    def cancel_order(self, currency_type=None, order_type=None, order_id=None, price=None, qty=None):
        """
        취소주문을 실행하는 메소드
        :param price: 가격
        :param qty: 수량
        :param currency_type: 암호화폐의 종류
        :param order_type: 취소하려는 주문의 종류 (1:매도, 0:매수)
        :param order_id: 취소하며는 주문의 ID
        :return: 주문 상태를 반환
        """

        if currency_type is None or order_type is None or order_id is None:
            raise Exception("Need to parameter")

        time.sleep(1)
        cancel_api_path = "/v2/order/cancel"
        url_path = self.BASE_API_URL + cancel_api_path

        payload = {
            "access_token": self.access_token,
            "order_id": order_id,
            "is_ask": 1 if order_type is "sell" else 0,
            "price": int(price),
            "qty": float(qty),
            "currency": currency_type,
            "nonce": get_nonce()
        }

        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        return result

    def get_list_my_orders(self, currency_type=None):
        """
        사용자의 현재 예약(매매체결전) 중인 주문 현황을 조회하는 메소드   
        :param currency_type: 화폐의 종류
        :return: 거래 진행중인 현황을 리스트로 반환
        """

        time.sleep(1)
        list_api_path = "/v2/order/limit_orders"
        url_path = self.BASE_API_URL + list_api_path

        payload = {
            "access_token": self.access_token,
            "currency": currency_type,
            "nonce": get_nonce()
        }

        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        return result

    def get_my_order_status(self, currency_type=None, order_id=None):
        """
        사용자의 주문 상세 정보를 조회하는 메소드
        :param currency_type: 화폐의 종류
        :param order_id: 거래 ID
        :return: order_id에 해당하는 주문의 상세 정보를 반환
                status -> live(미체결), filled(체결), partially_filled(미체결)
        """

        list_api_path = "/v2/order/order_info"
        url_path = self.BASE_API_URL + list_api_path

        payload = {
            "access_token": self.access_token,
            "currency": currency_type,
            "order_id": order_id,
            "nonce": get_nonce()
        }

        encoded_payload = get_encode_payload(payload)
        signature = get_signature(encoded_payload, self.secret_key.encode("utf-8"))

        headers = {"Content-type": "application/json",
                   "X-COINONE-PAYLOAD": encoded_payload,
                   "X-COINONE-SIGNATURE": signature
                   }

        res = requests.post(url_path, headers=headers, data=payload, verify=False)
        result = res.json()

        return result

