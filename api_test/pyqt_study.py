import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/mywindow.ui")[0]


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

        # self.label = QLabel("Hello")
        # self.label.show()

    def btn_clicked(self):
        print("버튼 클릭")
        self.setGeometry(500, 300, 400, 400)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
print("윈도우 종료")
