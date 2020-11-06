from datetime import time

import requests

from autotrading.machine.base_machine import Machine
import configparser


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
        """





