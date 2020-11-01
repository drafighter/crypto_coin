import configparser
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
