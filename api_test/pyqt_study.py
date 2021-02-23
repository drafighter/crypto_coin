import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("../../images/iconfinder_krusader_85.png"))

        # self.btn = QPushButton(text="매수", parent=self)
        # self.close_btn = QPushButton(text="종료", parent=self)
        # self.btn.move(10, 10)
        # self.close_btn.move(100, 10)
        # self.btn.clicked.connect(self.buy)
        # self.close_btn.clicked.connect(QApplication.instance().quit)

    def buy(self):
        print("몽땅 매수")


print(sys.argv)
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
print("윈도우 종료")
