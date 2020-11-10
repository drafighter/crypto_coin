import unittest
import inspect

from autotrading.machine.coinone_machine import CoinOneMachine


class CoinOneMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.coinone_machine = CoinOneMachine()

    def tearDown(self):
        pass

    # def test_set_token(self):
    #     print(inspect.stack()[0][3])
    #
    #     """
    #     1. 테스트나 실행환경이 바뀌었을 때는 토큰 재전송 후 메일로 수신된 키를 config.ini에 업데이트 후 grant_type 을 client_credentials 으로 설정
    #     2. config.ini 에 저장되어 있는 access_token 과 secret_key 가 변경된 경우 refresh_token 으로 설정
    #     그외는 korbit 과 동일한 client_credentials 로 설정해서 기존 access_token 사용
    #     """
    #     expire, access_tokken, refresh_tokken = self.coinone_machine.set_token(grant_type="client_credentials")
    #
    #     assert access_tokken
    #     print("access_tokken= %s, refresh_tokken= %s, expire= %s" % (access_tokken, refresh_tokken, expire))

    # def test_get_wallet_status(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.get_wallet_status()
    #     assert result
    #     print(result)

    # def test_buy_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.buy_order(currency_type="xrp",
    #                                             price="250",
    #                                             qty="10",
    #                                             order_type="limit"
    #                                             )
    #     assert result
    #     print(result)

    # def test_sell_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.sell_order(currency_type="xrp",
    #                                             price="1500",
    #                                             qty="10",
    #                                             order_type="limit"
    #                                             )
    #     assert result
    #     print(result)

    # def test_cancel_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.cancel_order(currency_type="xrp",
    #                                             price="1500",
    #                                             qty="5",
    #                                             order_type="sell",
    #                                             order_id="7c0ecdb1-1e4d-11e9-9ec7-00e04c3600d7"
    #                                              )
    #     assert result
    #     print(result)

    # def test_get_list_my_orders(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.get_list_my_orders(currency_type="xrp")
    #     assert result
    #     print(result)

    # def test_get_my_order_status(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.get_my_order_status(currency_type="xrp",
    #                                                       order_id="7c4dc5a9-1e4d-11e9-9ec7-00e04c3600d7")
    #     assert result
    #     print(result)
