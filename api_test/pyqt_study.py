import sys
import pyupbit
import urllib3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

# warning message 무시
urllib3.disable_warnings()

# form_class = uic.loadUiType("ui/mywindow.ui")[0]
form_class = uic.loadUiType("ui/upbit_sise.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setGeometry(300, 300, 400, 400)
        # self.setWindowIcon(QIcon("../../images/iconfinder_krusader_85.png"))
        # self.setWindowTitle("PyQt")
        #
        # self.btn = QPushButton(text="매수", parent=self)
        # btn1 = QPushButton("버튼1", self)
        # btn1.move(10, 10)
        # btn2 = QPushButton("버튼2", self)
        # btn2.move(10, 40)
        # btn1.clicked.connect(self.btn_clicked)

        self.pushButton.clicked.connect(self.btn_clicked)

        # QTime 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

    def btn_clicked(self):
        # print("== 코인 현재가 조회 ==")
        price = pyupbit.get_current_price("KRW-BTC")

        # price는 float형 이기때문에 str로 형변환해서 입력함.
        self.lineEdit.setText(str(price))
        # print(price)

    def timeout(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
print("윈도우 종료")
