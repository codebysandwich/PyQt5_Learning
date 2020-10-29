# -*- encoding: utf-8 -*-
'''
@Author: sandwich
@Date: 2020-10-25 15:08:41
@LastEditTime: 2020-10-25 15:08:45
@LastEditors: sandwich
@Description: 演示1
@FilePath: /PyQt_repo/script/app01.py
'''

from UI.design01 import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.callback)

    def callback(self):
        self.ui.lineEdit.setText('hello world')

if __name__ == "__main__":
    app = QApplication([])
    mainwindow = MainWindow()
    mainwindow.show()

    app.exec_()
