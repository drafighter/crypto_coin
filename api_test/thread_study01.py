import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Worker(QThread):
    def run(self):
        while True:
            print("안녕하세요.")
            self.sleep(1)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = Worker()
        self.worker.start()


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()