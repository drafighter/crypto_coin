import configparser

import requests

from autotrading.machine.base_machine import Machine


class KorbitMachine(Machine):
    """
    코빗 거래소와의 거래를 위한 클래스입니다.
    BASE_API_URL은 REST API 호출을 위한 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 코빗에서 거래가 가능한 화폐의 종류입니다.
    """
    BASE_API_URL = "https://api.korbit.co.kr"

    """
    BTC 비트코인, ETH 이더리움, XRP 리플, BCH 비트코인캐시, BSV 비트코인SV, EOS 이오스, LINK 체인링크, LTC 라이트코인
    TRX 트론, ZIL 질리카, XLM 스텔라루멘, OMG 오미세고, AERGO 아르고, BAT 베이직어텐션토큰, MED 메디블록
    ETC 이더리움클래식, QTUM 퀀텀, MKR 메이커, USDC 유에스디코인, FET 페치, BNB 바이낸스코인, DAI 다이    
    """
    TRADE_CURRENCY_TYPE = ["btc", "eth", "etc", "xrp", "bch", "ltc", "zil", "usdc", "bsv", "omg", "qtum", "bat",
                           "xlm", "aergo", "fet", "eos", "mkr", "dai", "link", "bnb", "trx", "med"]

    def __init__(self):
        """
        KorbitMachine 클래스에서 가장 먼저 호출되는 메서드입니다.
        config.ini에서 client_id, client_secret 정보를 읽어 옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['KORBIT']['client_id']
        self.CLIENT_SECRET = config['KORBIT']['client_secret']
        self.USER_NAME = config['KORBIT']['username']
        self.PASSWORD = config['KORBIT']['password']
        self.access_token = None
        self.refresh_token = None
        self.token_type = None
        self.expire = None

    def set_token(self, grant_type="client_credentials"):
        """액서스 토근 정보를 만들기 위한 메서드 입니다.
        grant_type=client_credentials 지정
        기존의 password 방식을 계속 사용할 수 있으나, 보안을 위하여 권장하지 않는다.

        :returns
            만료시간(expire), 액서스 토큰(access_token), 리프레시 토큰(refresh_token)을 반환합니다.

        :raises
            grant_type이 client_credentials이나 refresh_token이 아닌 경우 Exception을 발생시킵니다.

        """

        token_api_path = "/v1/oauth2/access_token"
        url_path = self.BASE_API_URL + token_api_path

        if grant_type == "client_credentials":
            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "grant_type": grant_type}
        elif grant_type == "refresh_token":
            data = {"client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "refresh_token": self.refresh_token,
                    "grant_type": grant_type}
        else:
            raise Exception("Unexpected grant_type")

        res = requests.post(url_path, data=data)
        result = res.json()
        self.access_token = result["access_token"]
        self.refresh_token = result["refresh_token"]
        self.token_type = result["token_type"]
        self.expire = result["expires_in"]
        return self.expire, self.access_token, self.refresh_token

    def get_token(self):
        """액세스 토큰 정보를 받기 위한 메서드입니다.
        :returns
            액세스 토큰(access_token이 있는 경우 봔환합니다.

        :raises
            access_token이 없는 경우 Exception을 발생시킵니다.
        """

        if self.access_token is not None:
            return self.access_token
        else:
            raise Exception("Need to set_token")



