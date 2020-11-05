import unittest
import inspect

from autotrading.machine.coinone_machine import CoinOneMachine


class CoinOneMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.coinone_machine = CoinOneMachine()

    def tearDown(self):
        pass

    def test_set_token(self):
        print(inspect.stack()[0][3])
        expire, access_tokken, refresh_tokken = self.coinone_machine.set_token(grant_type="client_credentials")
        assert access_tokken
        print("access_tokken= %s, refresh_tokken= %s, expire= %s" % (access_tokken, refresh_tokken, expire))
