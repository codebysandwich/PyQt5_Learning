#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : app.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-21 14:30:49
# Last Modified Date: 2020-12-21 14:59:55
# Last Modified By  : sanwich <122079260@qq.com>


import sys
from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
