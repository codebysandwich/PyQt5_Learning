#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : app.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-21 14:30:49
# Last Modified Date: 2020-12-23 21:01:16
# Last Modified By  : sanwich <122079260@qq.com>


import sys
import json
import pandas as pd
from script.QtDataSet import PandasModel
from script.Pollution_Draw import DrawWidget
from MainWindow import Ui_MainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QDesktopWidget, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self._datapath, self._wtype = self.__load_setting()
        self.ui.setupUi(self)
        self.setWindowTitle("天气形式数据删选")
        self.setWindowIcon(QIcon('./source/icon.png'))
        self._data = pd.DataFrame()
        self._model = PandasModel(self._data)
        self._types = []
        self.load()
        # 信号槽
        self.ui.cmb_type.currentIndexChanged.connect(self.type_callback)
        self.ui.cmb_year.currentIndexChanged.connect(self.year_callback)
        self.ui.cmb_month.currentIndexChanged.connect(self.month_callback)
        self.ui.cmb_day.currentIndexChanged.connect(self.day_callback)
        self.ui.tableView.clicked.connect(self.view_callback)
        self.ui.button_draw.clicked.connect(self.draw_callback)
        self.ui.button_reset.clicked.connect(self.reset)

    def load(self):
        """
        初始化tableView，初始化缓存
        """
        self._data = pd.read_excel(self._datapath, sheet_name=0, keep_default_na=False)
        self._model = PandasModel(self._data)
        self.__load_data(self._model)
        self._types = self._data[self._wtype].unique().tolist()
        # 天气形势过滤类型
        self.__reset_cmb(self.ui.cmb_type, self._types)
        self.__extra_filter()

    # ---------------私有函数--------------- #
    def __load_data(self, model):
        """
        将_model加载到tableView
        """
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(12, QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(13, QHeaderView.Stretch)

    def __extra_filter(self):
        """
        将_model数据删选依据提取出来
        """
        df = self._model.toDataFrame()
        years = sorted(df.iloc[:, 0].unique().tolist())
        months = sorted(df.iloc[:, 1].unique().tolist())
        days = sorted(df.iloc[:, 2].unique().tolist())
        self.__reset_cmb(self.ui.cmb_year, years)
        self.__reset_cmb(self.ui.cmb_month, months)
        self.__reset_cmb(self.ui.cmb_day, days)

    def __reset_cmb(self, cmb, items):
        cmb.clear()
        for i, item in enumerate(items):
            cmb.insertItem(i, str(item))
        cmb.setCurrentIndex(-1)

    def __load_setting(self):
        with open('./source/setting.json', 'r') as fp:
            js = json.load(fp)
            return js['filepath'], js['type']

    def __redraw(self):
        self.ui.tableView.repaint()
        self.ui.tableView.update()
        QApplication.processEvents()

    # ---------------槽函数--------------- #
    def __judge(self, cmb):
        if cmb.currentIndex() == -1 or cmb.count() == 1:
            return True

    def type_callback(self):
        if self.__judge(self.ui.cmb_type):
            return
        _type = self.ui.cmb_type.currentText()
        self._model = PandasModel(self._data[self._data[self._wtype] == _type])
        self.__load_data(self._model)
        self.__extra_filter()
        self.__redraw()

    def year_callback(self):
        if self.__judge(self.ui.cmb_year):
            return
        df = self._model.toDataFrame()
        mask = df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText()
        model = PandasModel(df[mask])
        self.__load_data(model)
        self.__reset_cmb(self.ui.cmb_month, sorted(df[mask].iloc[:, 1].unique().tolist()))
        self.__reset_cmb(self.ui.cmb_day, sorted(df[mask].iloc[:, 2].unique().tolist()))
        self.__redraw()

    def month_callback(self):
        if self.__judge(self.ui.cmb_month):
            return
        df = self._model.toDataFrame()
        mask = (df.iloc[:, 1].astype(str) == self.ui.cmb_month.currentText()) & \
               (df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText())
        model = PandasModel(df[mask])
        self.__load_data(model)
        self.__reset_cmb(self.ui.cmb_day, sorted(df[mask].iloc[:, 2].unique().tolist()))
        self.__redraw()

    def day_callback(self):
        if self.__judge(self.ui.cmb_day):
            return
        df = self._model.toDataFrame()
        mask = (df.iloc[:, 1].astype(str) == self.ui.cmb_month.currentText()) & \
               (df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText()) & \
               (df.iloc[:, 2].astype(str) == self.ui.cmb_day.currentText())
        model = PandasModel(df[mask])
        self.__load_data(model)
        self.__redraw()

    def view_callback(self, clickedIndex):
        row = clickedIndex.row()
        self.ui.tableView.selectRow(row)

    def draw_callback(self):
        if not self.ui.tableView.selectedIndexes():
            QMessageBox.warning(self, "提示", "请选择需要绘图的数据！")
            return
        index = self.ui.tableView.currentIndex().row()
        ser = self.ui.tableView.model().toDataFrame().iloc[index, 0:3]
        year, month, day = ser['年'], ser['月'], ser['日']
        draw = DrawWidget(self._datapath, year, month, day)
        draw.show()

    def reset(self):
        self._model = PandasModel(self._data)
        self.__load_data(self._model)
        self.ui.cmb_type.setCurrentIndex(-1)
        self.__extra_filter()
        self.__redraw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
