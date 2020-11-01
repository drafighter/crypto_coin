import unittest
from autotrading.machine.korbit_machine import KorbitMachine
import inspect


class KorbitMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.korbit_machine = KorbitMachine()

    def tearDown(self):
        pass

    def test_set_token(self):
        print(inspect.stack()[0][3])
        expire, access_token, refresh_token = self.korbit_machine.set_token(grant_type="client_credentials")
        assert access_token
        print("Expire: %s, Access_token: %s, Refresh_token: %s" % (expire, access_token, refresh_token))

    def test_get_token(self):
        print(inspect.stack()[0][3])
        self.korbit_machine.set_token(grant_type="client_credentials")
        access_token = self.korbit_machine.get_token()
        assert access_token
        print("Access_token: " + access_token)
