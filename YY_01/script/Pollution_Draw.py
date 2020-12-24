#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : Pollution_Draw.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-23 17:06:34
# Last Modified Date: 2020-12-24 10:11:56
# Last Modified By  : sanwich <122079260@qq.com>

import sys
import pandas as pd
from datetime import datetime
from Draw import Ui_Form
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar



class MplCanvas(FigureCanvas):
    def __init__(self) -> None:
        self.fig = Figure()
        super(MplCanvas, self).__init__(self.fig)

        # size policy
        FigureCanvas.setSizePolicy(self,
                    QSizePolicy.Expanding,
                    QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class DrawWidget(QWidget):
    def __init__(self, filepath, year, month, day):
        super(DrawWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('%s年%s月%s日' % (year, month, day))
        self.setWindowIcon(QIcon('../source/draw.png'))
        self.canvas = MplCanvas()
        self.ui.verticalLayout.addWidget(self.canvas)
        self.ui.verticalLayout.addWidget(NavigationToolbar(self.canvas, self))
        self.year = year
        self.month = month
        self.day = day
        data = pd.read_excel(filepath, sheet_name=1, usecols=['年', '月', '日',
                                  '时', 'O3(ug/m3)', 'PM2.5(ug/m3)'])
        data['dt'] = data.apply(self.__gendt, axis=1)
        self.data = data
        self.plot()


    def plot(self):
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.plot()
        mask = (self.data['年'] == self.year) & \
               (self.data['月'] == self.month) & \
               (self.data['日'] == self.day)
        dt = self.data[mask]
        dt = dt.sort_values(by='dt').set_index('dt')
        start = datetime.strptime('%s-%s-%s 00:00:00'%(self.year, self.month, self.day), "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime('%s-%s-%s 23:00:00'%(self.year, self.month, self.day), "%Y-%m-%d %H:%M:%S")
        dt_ser = pd.date_range(start=start, end=end, freq='H')
        dt = dt.reindex(dt_ser)
        x = range(1, len(dt)+1)
        ax.plot(x, pd.to_numeric(dt.loc[:, 'O3(ug/m3)'], errors='coerce').to_list(), label='O3(ug/m3)')
        ax.plot(x, pd.to_numeric(dt.loc[:, 'PM2.5(ug/m3)'], errors='coerce').to_list(), label='PM2.5(ug/m3)')
        ax.set_xlim(0.5, 24.5)
        ax.set_xticks(list(x))
        ax.legend()
        self.canvas.fig.tight_layout()
        # 重新绘制GUI
        self.canvas.fig.canvas.draw_idle()


    def __gendt(self, ser):
        year = int(ser['年'])
        month = int(ser['月'])
        day = int(ser['日'])
        hour = int(str(ser['时']).split(':')[0])
        dt = datetime(year, month, day, hour)
        return dt


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DrawWidget(2020, 10, 22)
    widget.show()
    sys.exit(app.exec_())
