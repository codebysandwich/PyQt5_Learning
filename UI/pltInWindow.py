# -*- encoding: utf-8 -*-
'''
@Author: sandwich
@Date: 2020-10-28 16:05:43
@LastEditTime: 2020-10-28 16:05:47
@LastEditors: sandwich
@Description: 在pyqt中使用matplotlib
@FilePath: /PyQt5_Learning/UI/pltInWindow.py
'''
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
    def __init__(self) -> None:
        super(UI_Mainwindow, self).__init__()
        self.widget = QWidget(self)
        self.canvas = MplCanvas()
        self.setCentralWidget(self.widget)
        self.bt = QPushButton("liner")
        self.bt.clicked.connect(self.plot)

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self.widget)
        self.widget.setLayout(layout)
        layout.addWidget(self.canvas)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        # 添加按钮绘制图片
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.bt)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setGeometry(300, 400, 800, 600)

    def plot(self):
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.plot(5*np.random.randn(100)+12)
        self.canvas.fig.tight_layout()
        # 重新绘制GUI
        self.canvas.fig.canvas.draw_idle()


if __name__ == "__main__":
    app = QApplication([])
    mainwindow = UI_Mainwindow()
    mainwindow.show()
    app.exec_()