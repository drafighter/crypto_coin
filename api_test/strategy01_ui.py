import sys
import pyupbit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/bull.ui")[0]
tickers = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-ETC"]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        timer = QTimer(self)
        timer.start(5000)
        timer.timeout.connect(self.timeout)

        # self.tableWidget.setRowCount(len(tickers))

    def timeout(self):
        for i, ticker in enumerate(tickers):
            ticker_item = QTableWidgetItem(ticker)
            self.tableWidget.setItem(i, 0, ticker_item)

            price, last_ma5, state = self.get_market_infos(ticker)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(state))

    # noinspection PyMethodMayBeStatic
    def get_market_infos(self, ticker):
        df = pyupbit.get_ohlcv(ticker)

        ma5 = df['close'].rolling(window=5).mean()
        last_ma5 = ma5[-2]
        price = pyupbit.get_current_price(ticker)

        state = None
        if price > last_ma5:
            state = "상승장"
        else:
            state = "하락장"

        return price, last_ma5, state


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
