#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : pltInWindow.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-21 11:01:57
# Last Modified Date: 2020-12-21 11:03:10
# Last Modified By  : sanwich <122079260@qq.com>
# -*- encoding: utf-8 -*-
'''
@Author: sandwich
@Date: 2020-10-28 16:05:43
@LastEditTime: 2020-10-28 16:05:47
@LastEditors: sandwich
@Description: 在pyqt中使用matplotlib
@FilePath: /PyQt5_Learning/UI/pltInWindow.py
'''

import sys
from script.timer import Timer
from PyQt5.QtCore import QTimer
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy


class MplCanvas(FigureCanvas):
    def __init__(self) -> None:
        self.fig = Figure()
        super(MplCanvas, self).__init__(self.fig)

        # size policy
        FigureCanvas.setSizePolicy(self,
                    QSizePolicy.Expanding,
                    QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class UI_Mainwindow(QMainWindow):
    """[summary]
    主窗体类设计
    Args:
        QMainWindow
    """
    def __init__(self) -> None:
        super(UI_Mainwindow, self).__init__()
        self.widget = QWidget(self)
        self.canvas = MplCanvas()
        self.setCentralWidget(self.widget)
        # 随机绘制折线图按钮
        self.bt = QPushButton("Liner")
        # 动态绘制按钮
        self.bt1 = QPushButton("Dynamic")
        self.bt.clicked.connect(self.bt_pressed)
        self.bt1.clicked.connect(self.bt1_pressed)
        self.bt2 = QPushButton("timer")
        self.bt2.clicked.connect(self.bt2_pressed)
        self._timer1 = Timer(self.dynamic_sin_plot)
        self._timer1.setInterval(100)
        self.sin_l = [0]
        self.dynamic_l = []
        self._timer = QTimer(self)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.dynamic_plot)

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self.widget)
        self.widget.setLayout(layout)
        layout.addWidget(self.canvas)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        # 添加按钮绘制图片
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.bt)
        button_layout.addWidget(self.bt1)
        button_layout.addWidget(self.bt2)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setGeometry(300, 300, 800, 600)

    def bt_pressed(self):
        self.plot(5*np.random.randn(100)+12)

    def plot(self, x):
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.plot(x)
        self.canvas.fig.tight_layout()
        # 重新绘制GUI
        self.canvas.fig.canvas.draw_idle()

    def bt1_pressed(self):
        if self.bt1.text() == 'Dynamic':
            self.bt.setEnabled(False)
            self.bt1.setText('Stop')
            self._timer.start()
        elif self.bt1.text() == 'Stop':
            self._timer.stop()
            self.bt1.setText('Dynamic')
            self.bt.setEnabled(True)

    def dynamic_plot(self):
        self.dynamic_l.append(np.random.random())
        self.plot(self.dynamic_l)

    def bt2_pressed(self):
        if self.bt2.text() == 'timer':
            self.bt.setEnabled(False)
            self.bt1.setEnabled(False)
            self.bt2.setText('stop')
            QApplication.processEvents()
            # draw sin
            self._timer1.start()
        elif self.bt2.text() == 'stop':
            self.bt.setEnabled(True)
            self.bt1.setEnabled(True)
            self.bt2.setText('timer')
            QApplication.processEvents()
            self._timer1.stop()

    def dynamic_sin_plot(self):
        self.plot(np.sin(self.sin_l))
        self.sin_l.append(self.sin_l[-1] + 0.1)


if __name__ == "__main__":
    app = QApplication([sys.argv])
    mainwindow = UI_Mainwindow()
    mainwindow.show()
    sys.exit(app.exec_())
